"""CareerX / Maccy Hub - native Python career acceleration hub."""
from nicegui import ui
from models import init_db
from services.sync import sync_pending
from views.dashboard import dashboard_page
from views.skills import skills_page
from views.career import career_page
from views.roadmap import roadmap_page
from views.resume import resume_page
from views.jobs import jobs_page
from views.applications import applications_page
from views.ai_hub import ai_hub_page
from views.settings import settings_page

init_db()


@ui.page('/')
def index():
    ui.colors(primary='#6750A4', secondary='#625B71', accent='#7D5260')

    with ui.header().classes('items-center justify-between px-6 bg-primary text-white'):
        ui.label('CareerX / Maccy Hub').classes('text-xl font-bold')
        ui.label('SAKET YADAV • MACCY CREATIONS').classes('text-xs opacity-80')

    with ui.left_drawer(value=True).classes('bg-slate-50'):
        ui.label('Career acceleration').classes('text-lg font-semibold p-4')
        pages = [
            ('Dashboard', dashboard_page),
            ('Skills', skills_page),
            ('Career paths', career_page),
            ('AI roadmap', roadmap_page),
            ('Resume builder', resume_page),
            ('Live jobs', jobs_page),
            ('Application tracker', applications_page),
            ('AI hub', ai_hub_page),
            ('Profile & settings', settings_page),
        ]
        content = ui.column().classes('w-full max-w-7xl mx-auto p-6')
        for label, page in pages:
            ui.button(label, on_click=lambda p=page, c=content: render_page(c, p)).props('flat align=left').classes('w-full')

    content = ui.column().classes('w-full max-w-7xl mx-auto p-6')
    dashboard_page(content)

    with ui.footer().classes('justify-center'):
        ui.label('CareerX is offline-first. Configure Supabase and AI providers through environment variables.')


def render_page(container, page):
    container.clear()
    page(container)


@ui.timer(60, once=False)
def background_sync():
    sync_pending()


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='CareerX / Maccy Hub', storage_secret='careerx-local-storage', reload=False, show=False)
