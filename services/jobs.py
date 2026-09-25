import httpx
from sqlmodel import Session, select
from models import Job, engine

async def fetch_public_jobs(query='python', remote_only=False):
    """Fetch genuine public listings from RemoteOK and Arbeitnow without credentials."""
    results = []
    headers = {'User-Agent': 'CareerX-MaccyHub/1.0'}
    async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
        for source, endpoint in [('RemoteOK', 'https://remoteok.com/api'), ('Arbeitnow', 'https://www.arbeitnow.com/api/job-board-api')]:
            try:
                data = (await client.get(endpoint)).json()
                rows = data.get('data', data) if isinstance(data, dict) else data
                for row in rows:
                    title = row.get('position') or row.get('title') or ''
                    if query.lower() not in title.lower() and query.lower() not in str(row.get('description','')).lower(): continue
                    results.append(Job(external_id=f"{source}:{row.get('id') or row.get('slug') or title}", title=title, company=row.get('company_name') or row.get('company') or 'Unknown', location=row.get('location') or 'Remote', url=row.get('url') or row.get('job_url') or '', source=source, remote=True, posted_at=row.get('date') or row.get('created_at')))
            except (httpx.HTTPError, ValueError, KeyError):
                continue
    with Session(engine) as session:
        for job in results:
            if not session.exec(select(Job).where(Job.external_id == job.external_id)).first(): session.add(job)
        session.commit()
    return results
