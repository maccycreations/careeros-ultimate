from nicegui import ui
from sqlmodel import Session, select

from data.catalog import SKILL_GROUPS
from models import Skill, engine


def skills_page(c):
    with c:
        ui.label('Skills catalog & progress').classes('text-3xl font-bold')
        ui.label(f'{sum(len(v) for v in SKILL_GROUPS.values())} curated skills across communication, business, software, cloud, and IAM/security.').classes('text-gray-600')

        with ui.row().classes('w-full flex-wrap'):
            name = ui.input('Add skill')
            category = ui.select(list(SKILL_GROUPS.keys()), value=list(SKILL_GROUPS)[0], label='Category')
            progress = ui.number('Progress %', value=0, min=0, max=100)

            def add():
                if not name.value:
                    return
                with Session(engine) as session:
                    session.add(Skill(name=name.value.strip(), category=category.value, proficiency=int(progress.value or 0)))
                    session.commit()
                refresh()
                ui.notify('Skill added')

            ui.button('Add skill', on_click=add)

        listing = ui.column().classes('w-full')

        def refresh():
            listing.clear()
            with listing:
                with Session(engine) as session:
                    rows = session.exec(select(Skill).order_by(Skill.category, Skill.name)).all()
                for row in rows:
                    with ui.card().classes('w-full'):
                        ui.label(f'{row.name} · {row.category}').classes('font-semibold')
                        ui.linear_progress(row.proficiency / 100).props('color=primary')
                        ui.label(f'{row.proficiency}% proficiency')

        refresh()
