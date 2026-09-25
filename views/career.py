from nicegui import ui
from sqlmodel import Session, select
from models import engine, Career

def career_page(c):
    with c:
        ui.label('Career paths').classes('text-3xl font-bold'); ui.label('Role skeletons mapped to practical skill areas.')
        with Session(engine) as s: careers=s.exec(select(Career)).all()
        for role in careers:
            with ui.expansion(f'{role.title} — {role.level}', icon='trending_up').classes('w-full'):
                ui.label(f'Skills: {role.skills}'); ui.label(f'Salary reference: {role.salary_range} · Demand: {role.demand}'); ui.label(f'Resources: {role.resources}')
