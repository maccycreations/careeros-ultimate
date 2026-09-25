from nicegui import ui
from sqlmodel import Session, select
from models import engine, Resume

def resume_page(c):
    with c:
        ui.label('AI, ATS & design resume builder').classes('text-3xl font-bold')
        ui.label('Create clean, text-first resumes that remain machine-readable.')
        name=ui.input('Resume name', value='My Career Resume').classes('w-full'); content=ui.textarea('Resume content').classes('w-full h-64'); score=ui.number('ATS score (validated manually)', value=0, min=0, max=100)
        def save():
            with Session(engine) as s: s.add(Resume(name=name.value, template='ATS Clean', content=content.value, ats_score=int(score.value or 0))); s.commit(); ui.notify('Resume saved locally')
        ui.button('Save resume', on_click=save); ui.label('Integrations are configured in Profile & settings; credentials are read from environment variables.')
