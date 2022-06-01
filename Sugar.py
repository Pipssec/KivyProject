from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')


class Menu(Screen):
    pass


class K1K1(Screen):
    sugar = StringProperty()
    water = StringProperty()

    def rasschet(self):
        try:
            V = int(self.ids.sirop.text)
            V1 = float(V / 100)
            self.sugar = 'Сахар: ' + str(int(V1 * 62.5)) + ' г'
            self.water = 'Вода: ' + str(int(V1 * 62.5)) + ' мл'
        except:
            pass

    def on_leave(self, *args):
        self.ids.sirop.text = '0'
        self.sugar = ''
        self.water = ''


class K2K1(Screen):
    sugar = StringProperty()
    water = StringProperty()

    def rasschet(self):
        try:
            V = int(self.ids.sirop.text)
            V1 = float(V / 100)
            self.sugar = 'Сахар: ' + str(int(V1 * 90)) + ' г'
            self.water = 'Вода: ' + str(int(V1 * 45)) + ' мл'
        except:
            pass

    def on_leave(self, *args):
        self.ids.sirop.text = '0'
        self.sugar = ''
        self.water = ''


class K15K1(Screen):
    sugar = StringProperty()
    water = StringProperty()

    def rasschet(self):
        try:
            V = int(self.ids.sirop.text)
            V1 = float(V / 100)
            water = int(V1 * 52.5)
            self.sugar = 'Сахар: ' + str(int(water * 1.5)) + ' г'
            self.water = 'Вода: ' + str(water) + ' мл'
        except:
            pass

    def on_leave(self, *args):
        self.ids.sirop.text = '0'
        self.sugar = ''
        self.water = ''


class K1K15(Screen):
    sugar = StringProperty()
    water = StringProperty()

    def rasschet(self):
        try:
            V = int(self.ids.sirop.text)
            V1 = float(V / 100)
            sugar = int(V1 * 46)
            self.sugar = 'Сахар: ' + str(sugar) + ' г'
            self.water = 'Вода: ' + str(int(sugar * 1.5)) + ' мл'
        except:
            pass

    def on_leave(self, *args):
        self.ids.sirop.text = '0'
        self.sugar = ''
        self.water = ''


kv = Builder.load_file("Sugar.kv")

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(Menu(name='menu'))
sm.add_widget(K1K1(name='1k1'))
sm.add_widget(K2K1(name='2k1'))
sm.add_widget(K15K1(name='15k1'))
sm.add_widget(K1K15(name='1k15'))


class SugarApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    SugarApp().run()
