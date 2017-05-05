__author__ = 'user'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.listview import ListView
from kivy.base import runTouchApp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MainView(ListView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(
            item_strings=[str(index) for index in range(100)])

if __name__ == '__main__':
    runTouchApp(MainView())