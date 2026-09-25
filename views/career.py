from nicegui import ui
from sqlmodel import Session, select

from models import Career, engine


def career_page(c):
    with c:
        ui.label('Career paths').classes('text-3xl font-bold')
        ui.label('Career paths aligned to the curated skill catalog, including Identity & Access Management (IAM).').classes('text-gray-600')

        with Session(engine) as session:
            careers = session.exec(select(Career)).all()

        for role in careers:
            with ui.expansion(f'{role.title} — {role.level}', icon='trending_up').classes('w-full'):
                ui.label(f'Skills: {role.skills}')
                ui.label(f'Salary reference: {role.salary_range} · Demand: {role.demand}')
                ui.label(f'Resources: {role.resources}')
