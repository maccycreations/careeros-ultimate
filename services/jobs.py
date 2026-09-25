import httpx
from sqlmodel import Session, select
from models import Job, engine

async def fetch_public_jobs(query='python', remote_only=False, company=None):
    """Fetch genuine public listings from supported no-key APIs only.

    Major job boards often prohibit automated scraping or require an approved API.
    They are therefore exposed as links in the UI rather than falsely represented as
    live integrations. This keeps imported data attributable and compliant.
    """
    results=[]; headers={'User-Agent':'CareerX-MaccyHub/1.0'}
    async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
        for source, endpoint in [('RemoteOK','https://remoteok.com/api'),('Arbeitnow','https://www.arbeitnow.com/api/job-board-api')]:
            try:
                response=await client.get(endpoint); response.raise_for_status(); data=response.json(); rows=data.get('data',data) if isinstance(data,dict) else data
                for row in rows:
                    title=row.get('position') or row.get('title') or ''; employer=row.get('company_name') or row.get('company') or 'Unknown'
                    searchable=f'{title} {employer} {row.get("description","")}'.lower()
                    if query.lower() not in searchable or (company and company.lower() not in employer.lower()): continue
                    results.append(Job(external_id=f'{source}:{row.get("id") or row.get("slug") or title}',title=title,company=employer,location=row.get('location') or 'Remote',url=row.get('url') or row.get('job_url') or '',source=source,remote=True,posted_at=row.get('date') or row.get('created_at')))
            except (httpx.HTTPError, ValueError, KeyError, TypeError): continue
    with Session(engine) as session:
        for job in results:
            if not session.exec(select(Job).where(Job.external_id==job.external_id)).first(): session.add(job)
        session.commit()
    return results
