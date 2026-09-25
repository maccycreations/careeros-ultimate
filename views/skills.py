from nicegui import ui
from sqlmodel import Session, select
from models import engine, Skill
from data.catalog import SKILL_GROUPS, all_skills

def skills_page(c):
    with c:
        ui.label('Skills catalog & progress').classes('text-3xl font-bold')
        ui.label(f'{len(all_skills())} curated skills across communication, business, software, cloud, data, and IAM/security.').classes('text-gray-600')
        with ui.row().classes('w-full flex-wrap'):
            name=ui.input('Add skill'); category=ui.select(list(SKILL_GROUPS), value=list(SKILL_GROUPS)[0], label='Category'); progress=ui.number('Progress %', value=0, min=0, max=100)
            def add():
                if not name.value: return
                with Session(engine) as s: s.add(Skill(name=name.value.strip(), category=category.value, proficiency=int(progress.value or 0))); s.commit()
                refresh(); ui.notify('Skill added')
            ui.button('Add skill', on_click=add)
        listing=ui.column().classes('w-full')
        def refresh():
            listing.clear()
            with listing:
                with Session(engine) as s: rows=s.exec(select(Skill).order_by(Skill.category, Skill.name)).all()
                for x in rows:
                    with ui.card().classes('w-full'):
                        ui.label(f'{x.name} · {x.category}').classes('font-semibold'); ui.linear_progress(x.proficiency/100).props('color=primary'); ui.label(f'{x.proficiency}% proficiency')
        refresh()
