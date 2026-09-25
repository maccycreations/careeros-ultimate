from nicegui import ui
import os
from services.sync import sync_pending


def settings_page(c):
    with c:
        ui.label('Profile & settings').classes('text-3xl font-bold')
        ui.label('Developer: SAKET YADAV · Company: MACCY CREATIONS').classes('text-gray-600')

        ui.label('Runtime configuration').classes('text-xl font-semibold')
        keys = [
            'SUPABASE_URL', 'SUPABASE_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY',
            'ANTHROPIC_API_KEY', 'XAI_API_KEY', 'CANVA_CLIENT_ID', 'CANVA_CLIENT_SECRET',
            'ADOBE_CLIENT_ID', 'ADOBE_CLIENT_SECRET', 'JOBSUITE_API_KEY'
        ]
        for key in keys:
            state = 'configured' if os.getenv(key) else 'not configured'
            ui.label(f'{key}: {state}').classes('text-sm')

        def sync_now():
            count = sync_pending()
            ui.notify(f'Sync completed: {count} queued item(s) processed.')

        ui.button('Sync now', on_click=sync_now)
        ui.button('Purge local cache', on_click=lambda: ui.notify('Local cache purge is available after the application is connected to a persistent storage adapter.'))

        ui.markdown('''
### Privacy
CareerX stores local data in SQLite and keeps provider keys in environment variables only.

Never commit passwords, service-role keys, or secrets to source control. Configure Supabase RLS and server-side encryption before multi-user deployment.
''')
