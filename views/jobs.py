from nicegui import ui
from sqlmodel import Session, select
from models import engine, Job, Application
from services.jobs import fetch_public_jobs

def jobs_page(c):
    with c:
        ui.label('Live job seeking platform').classes('text-3xl font-bold'); query=ui.input('Search public listings', value='python'); rows=ui.column().classes('w-full')
        async def search():
            rows.clear(); jobs=await fetch_public_jobs(query.value)
            with rows:
                for j in jobs[:30]:
                    with ui.card().classes('w-full'):
                        ui.link(j.title, j.url, new_tab=True).classes('text-lg font-semibold'); ui.label(f'{j.company} · {j.location} · {j.source}')
                        ui.button('Apply & track', on_click=lambda job=j: track(job))
        def track(job):
            with Session(engine) as s: s.add(Application(company=job.company,title=job.title,stage='Saved')); s.commit()
            ui.notify('Added to Application Tracker')
        ui.button('Fetch genuine public listings', on_click=search); ui.label('Sources: RemoteOK and Arbeitnow public job-board APIs. Always verify a listing on the employer site before applying.')
