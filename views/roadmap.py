from nicegui import ui
from sqlmodel import Session, select

from models import Roadmap, engine
from services.auth import get_current_user


def roadmap_page(c):
    user = get_current_user()
    if user is None:
        return

    with c:
        ui.label('AI roadmap builder').classes('text-3xl font-bold')
        goal = ui.input('Career goal', placeholder='e.g. become a production AI engineer').classes('w-full')
        output = ui.column().classes('w-full')

        def generate():
            if not goal.value:
                return
            steps = [
                f'Define the target role and baseline skills for: {goal.value}',
                'Build a focused Python and SQL project',
                'Learn model evaluation, APIs, deployment, and security',
                'Publish a portfolio case study with measurable outcomes',
                'Practice interviews and apply to verified roles',
            ]
            with Session(engine) as session:
                session.add(Roadmap(user_id=user.id, goal=goal.value, steps='\n'.join(steps)))
                session.commit()
            output.clear()
            with output:
                for idx, step in enumerate(steps, 1):
                    ui.label(f'{idx}. {step}').classes('p-3 border rounded w-full')

        ui.button('Generate and save roadmap', on_click=generate)
