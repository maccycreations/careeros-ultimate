"""Minimal AI hub provider interface for live model calls."""
import os
from nicegui import ui

PROVIDERS = ['OpenAI', 'Google Gemini', 'Anthropic Claude', 'xAI Grok', 'Custom agent']


def _provider_key(provider: str) -> str:
    mapping = {
        'OpenAI': 'OPENAI_API_KEY',
        'Google Gemini': 'GEMINI_API_KEY',
        'Anthropic Claude': 'ANTHROPIC_API_KEY',
        'xAI Grok': 'XAI_API_KEY',
        'Custom agent': 'CUSTOM_AGENT_API_KEY',
    }
    return mapping.get(provider, 'OPENAI_API_KEY')


def ai_hub_page(c):
    with c:
        ui.label('AI hub').classes('text-3xl font-bold')
        ui.label('Manage multi-model career support for interview prep, cold email drafting, and roadmap planning.').classes('text-gray-600')

        provider = ui.select(PROVIDERS, value='OpenAI', label='Provider')
        prompt = ui.textarea('Prompt', value='Act as a career coach and help me prepare for a System Design or IAM interview.').classes('w-full')
        answer = ui.markdown('')

        def run_assistant():
            key_name = _provider_key(provider.value)
            key_value = os.getenv(key_name)
            if not key_value:
                answer.content = (
                    f'**{provider.value}** is not configured.\n\n'
                    f'Add `{key_name}` to your environment variables before running a live AI request.'
                )
                return

            answer.content = (
                f'**Provider:** {provider.value}\n\n'
                f'**Prompt:** {prompt.value}\n\n'
                'This app is ready for a live model integration. The environment key is detected, and the provider adapter can now be connected to the actual SDK or HTTP API.'
            )

        ui.button('Run assistant', on_click=run_assistant)
