from nicegui import ui
from sqlmodel import Session, select
from models import engine, Skill, Application, Resume, Job, Roadmap

def dashboard_page(c):
    with c:
        ui.label('Professional dashboard').classes('text-3xl font-bold')
        ui.label('Your career workspace, available online or in local sync mode.').classes('text-gray-600')
        with ui.row().classes('w-full gap-4 flex-wrap'):
            for label, query in [('Applications', Application), ('Resumes', Resume), ('Roadmaps', Roadmap), ('Skills tracked', Skill)]:
                with ui.card().classes('min-w-48 flex-1'): ui.label(label); ui.label(str(len(Session(engine).exec(select(query)).all()))).classes('text-3xl font-bold text-primary')
        ui.separator(); ui.label('Daily career actions').classes('text-xl font-semibold')
        ui.markdown('- Review one target role\n- Improve one measurable resume bullet\n- Apply to a relevant opportunity\n- Practice one interview answer')
