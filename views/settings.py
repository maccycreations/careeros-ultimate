from nicegui import ui

from services.auth import get_current_user, logout_user


def settings_page(c):
    user = get_current_user()
    if user is None:
        return

    with c:
        ui.label('Profile & settings').classes('text-3xl font-bold')
        ui.label(f'Developer: SAKET YADAV • Company: MACCY CREATIONS').classes('text-gray-600')
        ui.label(f'Logged in as: {user.email}').classes('text-sm')

        def do_logout():
            logout_user()
            ui.navigate.to('/')

        ui.button('Logout', on_click=do_logout)
        ui.button('Sync now', on_click=lambda: ui.notify('Sync queued. Configure Supabase credentials to enable remote synchronization.'))
