from nicegui import ui
from sqlmodel import Session

from data.catalog import COMPANIES, JOB_PLATFORMS
from models import Application, engine
from services.jobs import fetch_public_jobs


def jobs_page(c):
    with c:
        ui.label('Live job seeking platform').classes('text-3xl font-bold')
        ui.label('Public-source connectors and an MNC career-site directory. Protected portals require their approved API or user-authorized integration.').classes('text-gray-600')

        with ui.expansion(f'Configured sources ({len(JOB_PLATFORMS)})', icon='public').classes('w-full'):
            for name, url in JOB_PLATFORMS.items():
                ui.link(name, url, new_tab=True)

        company_filter = ui.select(sorted(COMPANIES), label=f'Company directory ({len(COMPANIES)} companies)', with_input=True).classes('w-full')
        query = ui.input('Search public listings', value='python')
        rows = ui.column().classes('w-full')

        async def search():
            rows.clear()
            jobs = await fetch_public_jobs(query.value, company=company_filter.value)
            with rows:
                if not jobs:
                    ui.label('No matching public listings returned. Try a different keyword or verify the selected company connection.').classes('text-sm text-gray-600')
                    return
                for job in jobs[:50]:
                    with ui.card().classes('w-full'):
                        ui.link(job.title, job.url, new_tab=True).classes('text-lg font-semibold')
                        ui.label(f'{job.company} · {job.location} · {job.source}')
                        ui.button('Apply & track', on_click=lambda j=job: track(j))

        def track(job):
            with Session(engine) as session:
                session.add(Application(company=job.company, title=job.title, stage='Saved'))
                session.commit()
            ui.notify('Added to Application Tracker')

        ui.button('Fetch genuine public listings', on_click=search)
        ui.label('RemoteOK and Arbeitnow are active no-key connectors. Other portals and company sites are directory links until an approved API/feed is configured.').classes('text-sm text-gray-600')
