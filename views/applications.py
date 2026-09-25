from nicegui import ui
from sqlmodel import Session, select

from models import Application, engine
from services.auth import get_current_user


STAGES = ['Saved', 'Applied', 'Interviewing', 'Offer', 'Rejected']


def applications_page(c):
    user = get_current_user()
    if user is None:
        return

    with c:
        ui.label('Application tracker').classes('text-3xl font-bold')
        board = ui.row().classes('w-full items-start gap-3 flex-wrap')

        def render():
            board.clear()
            with Session(engine) as session:
                apps = session.exec(select(Application).where(Application.user_id == user.id)).all()
            with board:
                for stage in STAGES:
                    with ui.card().classes('min-w-56 flex-1 bg-slate-50'):
                        ui.label(stage).classes('font-bold')
                        for app in [a for a in apps if a.stage == stage]:
                            with ui.card().classes('w-full bg-white'):
                                ui.label(app.title).classes('font-semibold')
                                ui.label(app.company)
                                ui.select(STAGES, value=app.stage, label='Move stage', on_change=lambda e, a=app: move(a, e.value))

        def move(app, stage):
            with Session(engine) as session:
                fresh = session.get(Application, app.id)
                if fresh:
                    fresh.stage = stage
                    session.add(fresh)
                    session.commit()
            render()

        render()
