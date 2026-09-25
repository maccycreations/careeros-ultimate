from nicegui import ui
from sqlmodel import Session, select

from models import Resume, engine
from services.auth import get_current_user


def resume_page(c):
    user = get_current_user()
    if user is None:
        return

    with c:
        ui.label('AI, ATS & design resume builder').classes('text-3xl font-bold')
        ui.label('Create clean, text-first resumes that remain machine-readable.').classes('text-gray-600')

        name = ui.input('Resume name', value='My Career Resume').classes('w-full')
        content = ui.textarea('Resume content').classes('w-full h-64')
        score = ui.number('ATS score', value=0, min=0, max=100)

        def save():
            with Session(engine) as session:
                session.add(Resume(user_id=user.id, name=name.value, template='ATS Clean', content=content.value, ats_score=int(score.value or 0)))
                session.commit()
            ui.notify('Resume saved locally')

        ui.button('Save resume', on_click=save)
