from nicegui import ui
from sqlmodel import Session, select
from models import engine, Skill

def skills_page(c):
    with c:
        ui.label('Skills catalog & progress').classes('text-3xl font-bold')
        with ui.row().classes('w-full'):
            name=ui.input('Skill name'); category=ui.input('Category', value='Software Engineering'); progress=ui.number('Progress %', value=0, min=0, max=100)
            def add():
                with Session(engine) as s: s.add(Skill(name=name.value, category=category.value, proficiency=int(progress.value or 0))); s.commit(); refresh()
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
