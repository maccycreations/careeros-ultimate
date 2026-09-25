from nicegui import ui
from sqlmodel import Session, select

from models import Skill, engine
from services.auth import get_current_user


def skills_page(c):
    user = get_current_user()
    if user is None:
        return

    with c:
        ui.label('Skills catalog & progress').classes('text-3xl font-bold')
        ui.label('Track the skills most relevant to your target roles and career progress.').classes('text-gray-600')

        with ui.row().classes('w-full flex-wrap'):
            name = ui.input('Add skill')
            category = ui.select(['Communication & workplace', 'Delivery & business', 'Software & data', 'Cloud & infrastructure', 'Cybersecurity & identity'], value='Software & data', label='Category')
            progress = ui.number('Progress %', value=0, min=0, max=100)

            def add():
                if not name.value:
                    return
                with Session(engine) as session:
                    session.add(Skill(user_id=user.id, name=name.value.strip(), category=category.value, proficiency=int(progress.value or 0)))
                    session.commit()
                refresh()
                ui.notify('Skill added')

            ui.button('Add skill', on_click=add)

        listing = ui.column().classes('w-full')

        def refresh():
            listing.clear()
            with listing:
                with Session(engine) as session:
                    rows = session.exec(select(Skill).where(Skill.user_id == user.id).order_by(Skill.category, Skill.name)).all()
                for row in rows:
                    with ui.card().classes('w-full'):
                        ui.label(f'{row.name} · {row.category}').classes('font-semibold')
                        ui.linear_progress(row.proficiency / 100).props('color=primary')
                        ui.label(f'{row.proficiency}% proficiency')

        refresh()
