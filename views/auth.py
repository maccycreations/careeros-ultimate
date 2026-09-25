"""Authentication views for login and signup."""
from nicegui import ui

from services.auth import authenticate_user, create_user, get_current_user, logout_user, set_current_user


def auth_page(c):
    with c:
        ui.label('CareerX / Maccy Hub').classes('text-3xl font-bold')
        ui.label('Sign in to continue').classes('text-gray-600')

        tabs = ui.tabs().classes('w-full')
        with tabs:
            login_tab = ui.tab('Login')
            signup_tab = ui.tab('Sign up')

        with ui.tab_panels(tabs, value=login_tab).classes('w-full'):
            with ui.tab_panel(login_tab):
                email = ui.input('Email').classes('w-full')
                password = ui.password('Password').classes('w-full')

                def do_login():
                    user = authenticate_user(email.value, password.value)
                    if user is None:
                        ui.notify('Invalid email or password.', color='negative')
                        return
                    set_current_user(user)
                    ui.navigate.to('/')

                ui.button('Login', on_click=do_login).classes('w-full')

            with ui.tab_panel(signup_tab):
                name = ui.input('Full name').classes('w-full')
                signup_email = ui.input('Email').classes('w-full')
                signup_password = ui.password('Password').classes('w-full')

                def do_signup():
                    if not signup_email.value or not signup_password.value:
                        ui.notify('Email and password are required.', color='negative')
                        return
                    user = create_user(signup_email.value, name.value or 'User', signup_password.value)
                    set_current_user(user)
                    ui.navigate.to('/')

                ui.button('Create account', on_click=do_signup).classes('w-full')


def logout_button():
    def do_logout():
        logout_user()
        ui.navigate.to('/')

    return ui.button('Logout', on_click=do_logout)


def ensure_authenticated():
    user = get_current_user()
    if user is None:
        return False
    return True
