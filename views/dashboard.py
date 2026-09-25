from nicegui import ui
from sqlmodel import Session, select

from models import Application, Resume, Roadmap, Skill, engine
from services.auth import get_current_user


def dashboard_page(c):
    user = get_current_user()
    if user is None:
        return

    with c:
        ui.label('Professional dashboard').classes('text-3xl font-bold')
        ui.label('Your career workspace, available online or in local sync mode.').classes('text-gray-600')

        with ui.row().classes('w-full gap-4 flex-wrap'):
            with Session(engine) as session:
                app_count = session.exec(select(Application).where(Application.user_id == user.id)).all()
                resume_count = session.exec(select(Resume).where(Resume.user_id == user.id)).all()
                roadmap_count = session.exec(select(Roadmap).where(Roadmap.user_id == user.id)).all()
                skill_count = session.exec(select(Skill).where(Skill.user_id == user.id)).all()

            for label, count in [('Applications', len(app_count)), ('Resumes', len(resume_count)), ('Roadmaps', len(roadmap_count)), ('Skills tracked', len(skill_count))]:
                with ui.card().classes('min-w-48 flex-1'):
                    ui.label(label)
                    ui.label(str(count)).classes('text-3xl font-bold text-primary')

        ui.separator()
        ui.label('Daily career actions').classes('text-xl font-semibold')
        ui.markdown('- Review one target role\n- Improve one measurable resume bullet\n- Apply to a relevant opportunity\n- Practice one interview answer')
