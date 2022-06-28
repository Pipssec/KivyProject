import psycopg2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config
import asyncio
import json
import methods
import hashlib

Config.set('kivy', 'keyboard_mode', 'systemanddock')
switch_auth = []
profile_name = []


def switch_on():
    switch_auth.append(1)


def switch_off():
    switch_auth.clear()
    profile_name.clear()


class MenuScreen(Screen):
    pass


class AboutUs(Screen):
    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class FullInformation(Screen):
    name_order = StringProperty()
    town = StringProperty()
    full_text = StringProperty()
    order_obl = StringProperty()
    order_car = StringProperty()
    order_car_model = StringProperty()
    order_car_year = StringProperty()
    order_car_fuel = StringProperty()
    order_car_username = StringProperty()
    order_phone = StringProperty()

    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class ListOrders(Screen):
    data = ListProperty()

    def on_pre_enter(self):
        json_listorders = asyncio.run(methods.listorders())
        result = json.loads(json_listorders)
        for x in range(len(result)):
            self.data.append(
                {
                    "text": f'{result[x]["order_name"]} {result[x]["town_name"]}',
                    "on_release": lambda x=(result[x]["order_name"]): self.show_full_information(x)
                }
            )

    def show_full_information(self, full_information):
        full_information_screen = sm.get_screen('fullinformation')
        json_fullinformation = asyncio.run(methods.fullinformation(full_information))
        result = json.loads(json_fullinformation)
        full_information_screen.name_order = result['name_order']
        full_information_screen.town = result['town']
        full_information_screen.full_text = result['full_text']
        full_information_screen.order_obl = result['order_obl']
        full_information_screen.order_car = result['order_car']
        full_information_screen.order_car_model = result['order_car_model']
        full_information_screen.order_car_year = result['order_car_year']
        full_information_screen.order_car_fuel = result['order_car_fuel']
        full_information_screen.order_car_username = result['order_car_username']
        full_information_screen.order_phone = result['order_phone']
        sm.current = 'fullinformation'

    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"

    def on_leave(self):
        self.data.clear()


class RegBad(Screen):
    pass


class Registration(Screen):
    def reg(self):
        login = (str(self.ids.name.text)).casefold()
        name_sto = str(self.ids.name_STO.text)
        oblast = (str(self.ids.name_obl.text)).capitalize()
        town_STO = (str(self.ids.name_town.text)).capitalize()
        phone_number = (str(self.ids.number_phone.text))
        passw = self.ids.name_pwd.text
        passw2 = self.ids.name_pwd2.text
        json_registration = asyncio.run(
            methods.registration(login, name_sto, oblast, town_STO, phone_number, passw, passw2))
        result = json.loads(json_registration)
        if result[0]['answer'] == 'regbad':
            return 'regbad'
        if result[0]['answer'] == 'reggood':
            self.ids.name.text = ''
            self.ids.name_pwd.text = ''
            self.ids.name_pwd2.text = ''
            self.ids.name_STO.text = ''
            self.ids.name_obl.text = ''
            self.ids.name_town.text = ''
            self.ids.number_phone.text = ''
            return 'reggood'
        if result[0]['answer'] == 'badlog':
            return 'badlog'
        if result[0]['answer'] == 'badobltown':
            return 'badobltown'


class RegGood(Screen):
    pass


class BadLogin(Screen):
    pass


class BadOblastOrTown(Screen):
    pass


class BadOblastOrTown2(Screen):
    pass


class Authorization(Screen):
    def auth(self):
        auth_name = (str(self.ids.auth_name.text)).casefold()
        auth_pass = hashlib.sha224((self.ids.auth_pwd.text).encode('utf-8')).hexdigest()
        json_authorization = asyncio.run(methods.authorization(auth_name, auth_pass))
        result = json.loads(json_authorization)
        if result[0]['answer'] == 'authgood':
            switch_on()
            profile_name.append(auth_name)
            self.ids.auth_name.text = ''
            self.ids.auth_pwd.text = ''
            return 'authgood'
        if result[0]['answer'] == 'authbad':
            return 'authbad'


class ListSto(Screen):
    data = ListProperty()

    def on_pre_enter(self, *args):
        json_liststo = asyncio.run(methods.liststo())
        result = json.loads(json_liststo)
        for x in range(len(result)):
            self.data.append(result[x])

    def menu(self):
        self.data.clear()
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class CreateOrder(Screen):

    def create(self):
        name_ord = (str(self.ids.name_order.text)).capitalize()
        text_order = (str(self.ids.text_order.text)).casefold()
        order_town = (str(self.ids.order_town.text)).capitalize()
        order_obl = (str(self.ids.order_obl.text)).capitalize()
        order_car = (str(self.ids.order_car.text)).casefold()
        order_car_model = (str(self.ids.order_car_model.text)).casefold()
        order_car_year = (str(self.ids.order_car_year.text)).casefold()
        order_car_fuel = (str(self.ids.order_car_fuel.text)).casefold()
        order_username = (str(self.ids.order_username.text))
        order_phone = (str(self.ids.order_username_phone.text))
        json_createorder = asyncio.run(
            methods.createorder(name_ord, text_order, order_town, order_obl, order_car, order_car_model, order_car_year,
                                order_car_fuel, order_username, order_phone))
        result = json.loads(json_createorder)
        if result[0]['answer'] == 'ordergood':
            self.ids.name_order.text = ''
            self.ids.text_order.text = ''
            self.ids.order_town.text = ''
            self.ids.order_obl.text = ''
            self.ids.order_car.text = ''
            self.ids.order_car_model.text = ''
            self.ids.order_car_year.text = ''
            self.ids.order_car_fuel.text = ''
            self.ids.order_username.text = ''
            self.ids.order_username_phone.text = ''
            return 'ordergood'
        if result[0]['answer'] == 'badobltown2':
            return 'badobltown2'

    def back(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class AuthGood(Screen):
    pass


class AuthBad(Screen):
    pass


class AuthMenu(Screen):
    def exit(self):
        switch_off()
        return "menu"


class OrderGood(Screen):
    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class MyProfile(Screen):
    sto_name = StringProperty()
    sto_town = StringProperty()
    sto_phone = StringProperty()

    def on_pre_enter(self):
        json_profile = asyncio.run(methods.myprofile(profile_name[0]))
        mess = json.loads(json_profile)
        self.sto_name = mess['sto_name']
        self.sto_town = mess['sto_town']
        self.sto_phone = mess['sto_phone']


class NoSignal(Screen):
    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


kv = Builder.load_file("My.kv")

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AboutUs(name='about_us'))
sm.add_widget(ListOrders(name='list_orders'))
sm.add_widget(Registration(name='registration'))
sm.add_widget(RegBad(name='regbad'))
sm.add_widget(RegGood(name='reggood'))
sm.add_widget(BadLogin(name='badlog'))
sm.add_widget(BadOblastOrTown(name='badobltown'))
sm.add_widget(BadOblastOrTown2(name='badobltown2'))
sm.add_widget(Authorization(name='authorization'))
sm.add_widget(ListSto(name='liststo'))
sm.add_widget(CreateOrder(name='createorder'))
sm.add_widget(AuthGood(name='authgood'))
sm.add_widget(AuthBad(name='authbad'))
sm.add_widget(AuthMenu(name='authmenu'))
sm.add_widget(OrderGood(name='ordergood'))
sm.add_widget(MyProfile(name='myprofile'))
sm.add_widget(FullInformation(name='fullinformation'))
sm.add_widget(NoSignal(name='notsignal'))


class MyApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
