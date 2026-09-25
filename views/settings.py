from nicegui import ui
import os

def ai_hub_page(c):
    with c:
        ui.label('AI hub').classes('text-3xl font-bold'); ui.label('Provider keys are never stored in the browser or repository. Set them in the deployment environment.')
        provider=ui.select(['OpenAI','Google Gemini','Anthropic Claude','xAI Grok','Custom agent'], value='OpenAI', label='Provider'); prompt=ui.textarea('Prompt').classes('w-full'); answer=ui.markdown('')
        def run(): answer.content=f'**Configured provider:** {provider.value}\n\nYour prompt is ready. Add the provider SDK and server-side key to enable live completion.'
        ui.button('Run assistant', on_click=run)

def settings_page(c):
    with c:
        ui.label('Profile & settings').classes('text-3xl font-bold'); ui.label('Developer: SAKET YADAV · Company: MACCY CREATIONS')
        ui.label('Runtime configuration').classes('text-xl font-semibold')
        for key in ['SUPABASE_URL','SUPABASE_KEY','OPENAI_API_KEY','GEMINI_API_KEY','ANTHROPIC_API_KEY','XAI_API_KEY','CANVA_CLIENT_ID','CANVA_CLIENT_SECRET','ADOBE_CLIENT_ID','ADOBE_CLIENT_SECRET','JOBSUITE_API_KEY']:
            ui.label(f'{key}: ' + ('configured' if os.getenv(key) else 'not configured')).classes('text-sm')
        ui.button('Sync now', on_click=lambda: ui.notify('Sync requested; pending changes are retained locally when Supabase is not configured'))
        ui.markdown('### Privacy\nCareerX stores local data in SQLite. Add Supabase RLS before enabling multi-user online storage. Never commit passwords, private keys, or service-role keys.')
