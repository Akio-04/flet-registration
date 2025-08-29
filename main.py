import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "My App"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 400
    page.window.height = 550
    page.window.resizable = False

    def register(e):
        db = sqlite3.connect('Data')

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT
        )""")
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}')")

        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'Added'
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True

        page.update()

    def auth_user(e):
        db = sqlite3.connect('Data')

        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND '{user_pass.value}'")
        if cur.fetchone() != None:
            user_login.value = ''
            user_pass.value = ''
            btn_auth.text = 'Authorized'
            page.update()
        else:
            page.open(ft.SnackBar(ft.Text('Incorrectly entered data!')))
            page.update()

        db.commit()
        db.close()

    user_login = ft.TextField(label='Login', width=200, on_change=validate)
    user_pass = ft.TextField(label='Password', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Add', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Authorize', width=200, on_click=auth_user, disabled=True)

    panel_register = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text('Registration'),
                        user_login,
                        user_pass,
                        btn_reg
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    panel_auth = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text('Authorization'),
                        user_login,
                        user_pass,
                        btn_auth
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0: page.add(panel_register)
        elif index == 1: page.add(panel_auth)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER, label='Registration'),
            ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER_OUTLINED, label='Authorization')
        ],
        on_change=navigate
    )

    page.add(panel_register)

ft.app(target=main)
