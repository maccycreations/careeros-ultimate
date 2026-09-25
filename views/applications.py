from nicegui import ui
from sqlmodel import Session, select
from models import engine, Application
STAGES=['Saved','Applied','Interviewing','Offer','Rejected']

def applications_page(c):
    with c:
        ui.label('Application tracker').classes('text-3xl font-bold'); board=ui.row().classes('w-full items-start gap-3 flex-wrap')
        def render():
            board.clear()
            with Session(engine) as s: apps=s.exec(select(Application)).all()
            with board:
                for stage in STAGES:
                    with ui.card().classes('min-w-56 flex-1 bg-slate-50'):
                        ui.label(stage).classes('font-bold');
                        for app in [a for a in apps if a.stage==stage]:
                            with ui.card().classes('w-full bg-white'):
                                ui.label(app.title).classes('font-semibold'); ui.label(app.company); ui.select(STAGES, value=app.stage, label='Move stage', on_change=lambda e,a=app: move(a,e.value))
        def move(app, stage):
            with Session(engine) as s: fresh=s.get(Application, app.id); fresh.stage=stage; s.add(fresh); s.commit()
            render()
        render()
