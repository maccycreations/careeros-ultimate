from nicegui import ui
from sqlmodel import Session
from models import engine, Roadmap

def roadmap_page(c):
    with c:
        ui.label('AI roadmap builder').classes('text-3xl font-bold'); goal=ui.input('Career goal', placeholder='e.g. become a production AI engineer').classes('w-full')
        output=ui.column().classes('w-full')
        def generate():
            steps=[f'Define the target role and baseline skills for: {goal.value}', 'Build a focused Python and SQL project', 'Learn model evaluation, APIs, deployment, and security', 'Publish a portfolio case study with measurable outcomes', 'Practice interviews and apply to verified roles']
            with Session(engine) as s: s.add(Roadmap(goal=goal.value, steps='\n'.join(steps))); s.commit()
            output.clear()
            with output:
                for i, step in enumerate(steps,1): ui.card().classes('w-full').clear if False else ui.label(f'{i}. {step}').classes('p-3 border rounded w-full')
        ui.button('Generate and save roadmap', on_click=generate)
