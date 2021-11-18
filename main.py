from kivy.app import App
from kivy.config import Config
Config.set("graphics", "width", 640)
Config.set("graphics", "height", 960)

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.factory import Factory
from kivy.core.window import Window

import Backend


Window.clearcolor = (248/255, 215/255, 191/255, 1)

values = ('SlideTransition', 'SwapTransition', 'FadeTransition', 'WipeTransition')
ModeSwapScreens = values[0]
Color_Coffee = (81/255, 56/255, 42/255, 1)

FontSize = 25

Cart = []


class ScreenLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"

        self.layout = AnchorLayout(anchor_x="center", anchor_y="center")
        form_sign_in = BoxLayout(orientation="vertical", size_hint=(.8, .4), spacing=3)

        self.label_sign_in = Label(text="Вход", color=Color_Coffee, font_size=FontSize, size_hint=(1, 0.7))
        label_enter_number = Label(text="Номер:", color=Color_Coffee, size_hint=(1, 0.3))
        self.login_input = TextInput(multiline=False, size_hint=(1, 0.7))
        label_enter_password = Label(text="Пароль:", color=Color_Coffee, size_hint=(1, 0.3))
        self.password_input = TextInput(multiline=False, size_hint=(1, 0.7))
        box_buttons = BoxLayout(size_hint=(1, 0.7))
        self.button_sign_in = Button(text="Войти", size_hint=(.75, 1), font_size=FontSize)
        self.button_sign_in.bind(on_press=self.reflex_button1_press)
        self.button_register = Button(text="Регистрация", size_hint=(.25, 1))
        self.button_register.bind(on_press=self.reflex_button_register_press)
        self.label_password_invalid = Label(text="", color=(1, 0, 0, 1), font_size=FontSize, size_hint=(1, 0.7))

        box_buttons.add_widget(self.button_sign_in)
        box_buttons.add_widget(self.button_register)

        form_sign_in.add_widget(self.label_sign_in)
        form_sign_in.add_widget(label_enter_number)
        form_sign_in.add_widget(self.login_input)
        form_sign_in.add_widget(label_enter_password)
        form_sign_in.add_widget(self.password_input)
        form_sign_in.add_widget(box_buttons)
        form_sign_in.add_widget(self.label_password_invalid)

        self.layout.add_widget(form_sign_in)
        self.add_widget(self.layout)

    def reflex_button1_press(self, instance):
        login = self.login_input.text
        password = self.password_input.text

        log = Backend.LogInUser(login, password)
        if log is True:
            cookies_file = open('cookies', 'w')
            cookies_file.write(login)
            cookies_file.close()
            self.manager.transition.direction = 'left'
            self.manager.current = "main_screen"
        else:
            self.label_password_invalid.text = "Неверный логин или пароль"

    def reflex_button_register_press(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "register_screen"


class ScreenRegister(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register_screen'

        self.upper_curtain = AnchorLayout(anchor_x="left", anchor_y="top")
        button_back = Button(text='<', size_hint=[0.1, 0.05])
        button_back.bind(on_press=self.reflex_button_back_press)
        self.upper_curtain.add_widget(button_back)
        self.add_widget(self.upper_curtain)

        self.layout = AnchorLayout(anchor_x="center", anchor_y="center")
        form_sign_in = BoxLayout(orientation="vertical", size_hint=(.8, .4), spacing=3)

        self.label_sign_in = Label(text="Регистрация", color=Color_Coffee, font_size=FontSize, size_hint=(1, 0.7))
        label_enter_number = Label(text="Номер:", color=Color_Coffee, size_hint=(1, 0.3))
        self.login_input = TextInput(multiline=False, size_hint=(1, 0.7))
        self.password_input1 = TextInput(multiline=False, size_hint=(1, 0.7))
        self.password_input2 = TextInput(multiline=False, size_hint=(1, 0.7))
        self.button_register = Button(text="Регистрация", size_hint=(1, 0.7))
        self.button_register.bind(on_press=self.reflex_button_register_press)
        self.label_error = Label(text="", color=(1, 0, 0, 1), font_size=FontSize, size_hint=(1, 0.7))

        form_sign_in.add_widget(self.label_sign_in)
        form_sign_in.add_widget(label_enter_number)
        form_sign_in.add_widget(self.login_input)
        form_sign_in.add_widget(self.password_input1)
        form_sign_in.add_widget(self.password_input2)
        form_sign_in.add_widget(self.button_register)
        form_sign_in.add_widget(self.label_error)

        self.layout.add_widget(form_sign_in)
        self.add_widget(self.layout)

    def reflex_button_register_press(self, instance):
        if self.password_input1.text != self.password_input2.text:
            self.label_error.text = "Пароли не совпадают"
        else:
            number = self.login_input.text
            password = self.password_input1.text
            if 11 <= len(number) <= 12:
                log = Backend.RegisterUser(number, password)
                if log is True:
                    self.manager.transition.direction = 'left'
                    self.manager.current = "login"
                else:
                    self.label_error.text = "Пользователь с таким номером уже существует"
            else:
                self.label_error.text = "Номер введён неправильно"

    def reflex_button_back_press(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "login"


class ScreenMainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main_screen"

        self.layout = BoxLayout(orientation='vertical', spacing=5)

        self.scroll_panel_shall = BoxLayout(size_hint=[1, 1-0.15])
        self.scroll_panel = ScrollView()
        self.scroll_panel.do_scroll_x = False
        self.scroll_panel.do_scroll_y = True
        my_grid = GridLayout(cols=2, spacing=5)
        my_grid.size_hint_y = None
        count_menu = 3
        my_grid.height = int (Window.width * ((count_menu+1) // 2) * 2/3)
        for i in range(count_menu):
            my_grid.add_widget(Button(text=('Button ' + str(i)), background_color=(203/255, 170/255, 132/255, 1), background_normal=''))
        self.scroll_panel.add_widget(my_grid)

        self.bottom_panel = BoxLayout(size_hint=[1, 0.15], spacing=5)
        self.button1 = Button(text='Меню', background_color=(201/255, 149/255, 100/255, 1), background_normal='')
        self.button2 = Button(text='Акции', background_color=(201/255, 149/255, 100/255, 1), background_normal='')
        self.button3 = Button(text='Корзина', background_color=(201/255, 149/255, 100/255, 1), background_normal='')
        self.button4 = Button(text='Аккаунт', background_color=(201/255, 149/255, 100/255, 1), background_normal='')
        self.bottom_panel.add_widget(self.button1)
        self.bottom_panel.add_widget(self.button2)
        self.bottom_panel.add_widget(self.button3)
        self.bottom_panel.add_widget(self.button4)

        self.scroll_panel_shall.add_widget(self.scroll_panel)
        self.layout.add_widget(self.scroll_panel_shall)
        self.layout.add_widget(self.bottom_panel)

        self.add_widget(self.layout)

    def reflex_button1_press(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "login"


class ScreenCart(Screen):
    pass


class ScreenPromo(Screen):
    pass


class ScreenAccount(Screen):
    pass


class ScreenProduct(Screen):
    pass


class MyFirstApp(App):
    def build(self):
        '''
        self.layout = BoxLayout(orientation='vertical')
        self.label1 = Label(text="First", font_size=32)
        self.layout.add_widget(self.label1)

        self.button1 = Button(text="to next", font_size=32)
        self.button1.bind(on_press=lambda instance: print("Help"))
        self.layout.add_widget(self.button1)

        return self.layout
        '''
        self.sm = ScreenManager()
        self.sm.transition = Factory.get(ModeSwapScreens)()
        self.sm.add_widget(ScreenLogin())
        self.sm.add_widget(ScreenRegister())
        self.sm.add_widget(ScreenMainMenu())

        try:
            cookies_file = open('cookies', 'r')
            self.sm.current = 'main_screen'
        except Exception:
            pass
        return self.sm


'''if __name__ == '__main__':
    MyFirstApp().run()'''
MyFirstApp().run()
