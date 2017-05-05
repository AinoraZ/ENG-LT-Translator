from pynput.keyboard import Key, Listener
import os
import requests
import json
import copy
import kivy
from random import randint
from pynput.keyboard import Key, Controller, Listener

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from functools import partial
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.uix.listview import ListItemLabel
from kivy.properties import *
from kivy.uix.actionbar import *
from kivy.uix.tabbedpanel import *
from kivy.uix.floatlayout import *
from kivy.uix.anchorlayout import *
from kivy.uix.checkbox import *
import itertools
import threading
import time
import sys
from kivy.uix.behaviors import FocusBehavior
from pynput.keyboard import Key, Controller, Listener

kivy.require('1.9.1')  # replace with your current kivy version !

count = 0

class Translate(object):
    def __init__(self):
        self.a = []
        with open(os.getcwd() + "/json/words.json") as file:
            self.perCopy = json.load(file)

    def clear(self):
        with open(os.getcwd() + "/json/wordsBack.json") as file:
            self.per = json.load(file)
        with open(os.getcwd() + "/json/words.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.per, sort_keys=True, indent=4, separators=(',', ': '))
            )
        self.open_translation()
        print("Works")

    def translate(self, word):
        r = requests.get("http://api.mymemory.translated.net/get?q=" + word + "!&langpair=en|lt")
        return r.json()["matches"]

    def open_translation(self):
        with open(os.getcwd() + "/json/words.json") as file:
            return json.load(file)

    def save_file(self):
        pass


class TranslatedWidget(Screen):
    def __init__(self, **kwargs):
        super(TranslatedWidget, self).__init__(**kwargs)
        self.update()

    def update(self):
        self.clear_widgets()

        with open(os.getcwd() + "/json/words.json") as file:
            self.perCopy = json.load(file)

        anchor = AnchorLayout()
        anchor.anchor_x = "center"
        anchor.anchor_y = "top"

        self.multi = GridLayout(cols=1, padding=10, size_hint_y=None)
        self.multi.padding = [0, 50, 0, 0]
        self.multi.bind(minimum_height=self.multi.setter('height'))

        self.word_objs = []
        self.count = 0
        for word in self.perCopy["words"]:
            word_obj = self.create_line(word, self.count)
            self.word_objs.append(word_obj)
            self.multi.add_widget(word_obj)
            self.count += 1
        root = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        root.add_widget(self.multi)
        anchor.add_widget(root)
        anchor.add_widget(self.top_widget())
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        self.add_widget(anchor)

    def create_line(self, line, count):
        return TranslatedWord(line, count)

    def top_widget(self):
        menu_view = ActionView()

        menu_bar = ActionBar(pos_hint={'top':1.3})
        menu_bar.add_widget(menu_view)

        menu_previous = ActionPrevious()
        menu_previous.bind(on_press=self.switch_screen)
        menu_view.add_widget(menu_previous)

        save_btn = ActionButton(text="Save")
        menu_view.add_widget(save_btn)
        save_btn.bind(on_press=self.clock_save)

        add_btn = ActionButton(text="Add")
        menu_view.add_widget(add_btn)
        add_btn.bind(on_press=self.add)

        check_btn = ActionButton(text="Check All")
        menu_view.add_widget(check_btn)
        check_btn.bind(on_press=self.check_all)

        translate_btn = ActionButton(text="Translate")
        menu_view.add_widget(translate_btn)
        translate_btn.bind(on_press=self.translate)

        delete_btn = ActionButton(text="Delete")
        menu_view.add_widget(delete_btn)
        delete_btn.bind(on_press=self.delete_checked)

        revert_btn = ActionButton(text="Revert")
        menu_view.add_widget(revert_btn)
        revert_btn.bind(on_press=self.revert)

        return menu_bar

    def switch_screen(self, instance):
        sm.transition.direction = "right"
        sm.current = "main"

    def add(self, instance):
        with open(os.getcwd() + "/json/wordsBack.json") as file:
            self.per = json.load(file)
        self.perCopy["words"].append(self.per["words"][0])
        with open(os.getcwd() + "/json/words.json", 'w') as json_data:
                json_data.write(
                    json.dumps(self.perCopy, sort_keys=True, indent=4, separators=(',', ': '))
                )
        word_obj = self.create_line(self.per["words"][0], self.count)
        self.word_objs.append(word_obj)
        self.multi.add_widget(word_obj)
        self.count += 1

    def save_json(self, instance):
        self.clear()
        with open(os.getcwd() + "/json/words.json") as file:
            self.perCopy = json.load(file)
        for obj in self.word_objs:
            temp = obj.save_new()
            if temp != None:
                self.perCopy["words"].append(temp)
        with open(os.getcwd() + "/json/words.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.perCopy, sort_keys=True, indent=4, separators=(',', ': '))
            )
        self.update()

    def delete_checked(self, instance):
        for obj in self.word_objs:
            if obj != None:
                if obj.check.active:
                    obj.remove()


    def clock_save(self, instance):
        Clock.schedule_once(self.save_json, 0.05)

    def clear(self):
        with open(os.getcwd() + "/json/wordsBack.json") as file:
            self.per = json.load(file)
        del self.per["words"][0]
        with open(os.getcwd() + "/json/words.json", 'w') as json_data:
            json_data.write(
                json.dumps(self.per, sort_keys=True, indent=4, separators=(',', ': '))
            )

    def revert(self, instance):
        for obj in self.word_objs:
            if obj != None:
                if obj.disabled:
                    obj.disabled = False

    def check_all(self, instance):
        for obj in self.word_objs:
            if obj != None:
                if not obj.checked_all:
                    obj.checked_all = True
                    if not obj.disabled:
                        obj.check.active = True
                else:
                    obj.checked_all = False
                    if not obj.disabled:
                        obj.check.active = False

    done = False
    #here is the animation
    def animate(self):
        self.popup = Popup(title='Please wait...', size_hint=(0.5, 0.1),
                           auto_dismiss=False)
        if self.in_translation != []:
            self.popup.open()
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if not self.in_translation[self.in_translation.__len__() - 1].in_translation:
                    self.popup.dismiss()
                    break
                self.popup.title = "Please wait... " + c
                time.sleep(0.1)


    def translate(self, instance):
        self.in_translation = []
        for obj in self.word_objs:
            if obj != None:
                if obj.check.active:
                    if not obj.disabled:
                        obj.in_translation = True
                        self.in_translation.append(obj)
                        t = threading.Thread(target = obj.translate)
                        t.start()
        a = threading.Thread(target = self.animate)
        a.start()


class TranslatedWord(BoxLayout, ListItemButton):
    def __init__(self, word, count, **kwargs):
        self.word = word
        self.orientation = "horizontal"
        self.size_hint_y=None
        self.height = 30
        self.background_normal = "bg.png"
        self.background_down = self.background_normal
        self.background_disabled_down = self.background_normal
        self.background_disabled_normal = self.background_normal

        super(TranslatedWord, self).__init__(**kwargs)

        self.in_translation = False

        self.match = 0
        self.count = count
        if self.count % 2 == 0:
            self.background_color=(0.22, 0.22, 0.22, 1)
        else:
            self.background_color=(0.15, 0.15, 0.15, 1)

        self.check = CheckBox(size=(50, self.height), size_hint=(None, 1))
        self.add_widget(self.check)

        self.input_word = TextInput(text=word["word"].capitalize())
        self.add_widget(self.input_word)
        self.input_word.write_tab = False

        self.translation = TextInput(text=self.fix().capitalize())
        self.add_widget(self.translation)
        self.translation.write_tab = False

        btn1 = Button(text="Next")
        btn1.bind(on_press=self.re_translate)
        self.add_widget(btn1)

        btn2 = Button(text="Del")
        btn2.bind(on_press=self.remove)
        self.add_widget(btn2)

        self.checked_all = False
        self.focus()

    def fix(self):
        if self.word["matches"].__len__() > 0:
            if not self.word["word"].endswith("!"):
                if self.word["matches"][self.match]["translation"].endswith("!"):
                    return self.word["matches"][self.match]["translation"][:-1]
            return self.word["matches"][self.match]["translation"].lower().capitalize()
        return ""

    def remove(self, instance=""):
        self.disabled = True

    def re_translate(self, instance):
        if self.word["matches"].__len__() - 1 != self.match:
            self.match += 1
        else:
            self.match = 0
        self.translation.text = self.fix().capitalize()

    def save_new(self):
        if(self.disabled):
            self.parent.remove_widget(self)
            return None
        self.word["word"] = self.input_word.text
        if(self.word["matches"][self.match]["translation"] != self.translation.text):
            match_template = copy.copy(self.word["matches"][self.match])
            match_template["translation"] = self.translation.text
            self.match = self.word["matches"].__len__()
            self.word["matches"].append(match_template)
        self.word["matches"][0], self.word["matches"][self.match] = self.word["matches"][self.match], self.word["matches"][0]
        self.match = 0
        return self.word

    def translate(self, instance=""):
        translation = Translate().translate(self.input_word.text)
        self.word["matches"] = []
        for match in translation:
            self.word["matches"].append(match)
        self.in_translation = False
        self.match = 0
        self.translation.text = self.fix()

    def focus(self):
        self.input_word.focus = True


class WordShower(Screen):
    def __init__(self, **kwargs):
        super(WordShower, self).__init__(**kwargs)
        Clock.schedule_interval(self.check_update, 1 / 30.)
        self.update()
        self.switch = False

    def update(self):
        self.clear_widgets()
        with open(os.getcwd() + "/json/words.json") as file:
            self.perCopy = json.load(file)
            self.perCopy = self.perCopy["words"]

        layout = BoxLayout(orientation="vertical", padding=[100,50,100,50])
        self.add_widget(layout)

        self.word = Label(text="", font_size=40, size_hint=(1, 0.5))
        self.translation = TextInput(text="", font_size=30, size_hint=(1, 0.2))
        self.translation.multiline = False
        self.translation.write_tab = False
        self.translation.padding_x = [self.translation.width / 2, self.translation.width / 2]
        self.current_text = ""
        self.match = 0
        self.match_word = ""
        self.next_word()

        layout.add_widget(self.word)
        layout.add_widget(self.translation)

        anchor = AnchorLayout()
        anchor.anchor_x = "center"
        anchor.anchor_y = "top"
        anchor.add_widget(self.top_widget())
        self.add_widget(anchor)
        self.translation.focus = True

    def check_update(self, instance):
        if not self.switch:
            if self.current_text != self.translation.text:
                self.current_text = self.translation.text
                if self.translation.foreground_color != (0, 0, 0, 1):
                    self.translation.foreground_color = (0, 0, 0, 1)

    def next_word(self, instance=""):
        if self.perCopy.__len__() <= 1:
            print("Sorry, no words")
            self.word.text = "[No Translations]"
            return None
        temp = randint(0, self.perCopy.__len__() - 1)
        while temp == self.match:
            temp = randint(0, self.perCopy.__len__() - 1)
        self.match = temp
        self.word.text = self.fix()
        self.match_word = self.perCopy[self.match]["word"].lower().capitalize()
        self.translation.text = ""
        self.translation.foreground_color = (0, 0, 0, 1)
        self.translation.focus = True

    def fix(self):
        if self.perCopy[self.match]["matches"].__len__() > 0:
            if not self.perCopy[self.match]["word"].endswith("!"):
                if self.perCopy[self.match]["matches"][0]["translation"].endswith("!"):
                    return self.perCopy[self.match]["matches"][00]["translation"][:-1]
            return self.perCopy[self.match]["matches"][0]["translation"].lower().capitalize()
        return ""

    def top_widget(self):
        menu_view = ActionView()

        menu_bar = ActionBar(pos_hint={'top':1.3})
        menu_bar.add_widget(menu_view)

        menu_previous = ActionPrevious()
        menu_previous.bind(on_press=self.switch_screen)
        menu_view.add_widget(menu_previous)

        save_btn = ActionButton(text="Show")
        menu_view.add_widget(save_btn)
        save_btn.bind(on_press=self.show)

        add_btn = ActionButton(text="Next")
        menu_view.add_widget(add_btn)
        add_btn.bind(on_press=self.next_word)

        check_btn = ActionButton(text="Check")
        menu_view.add_widget(check_btn)
        check_btn.bind(on_press=self.check)

        return menu_bar

    def start_switch(self):
        self.switch = True
        switch = threading.Thread(target=self._sleep_switch)
        switch.daemon = True
        switch.start()

    def start_focus_offset(self):
        focus_offset = threading.Thread(target=self._set_focus)
        focus_offset.daemon = True
        focus_offset.start()

    def show(self, instance):
        self.translation.text = self.match_word
        self.translation.foreground_color = (0.5, 0.5, 0, 1)
        self.start_switch()

    def check(self, instance=""):
        print(self.translation.text.strip().lower())
        if self.translation.text.strip().lower() == self.match_word.strip().lower():
            self.translation.foreground_color = (0, 0.8, 0, 1)
            self.start_switch()
        else:
            self.translation.foreground_color = (1, 0, 0, 1)
            self.start_focus_offset()

    def _set_focus(self):
        time.sleep(0.2)
        self.translation.focus = True

    def _sleep_switch(self):
        time.sleep(2)
        self.switch = False
        self.next_word()

    def switch_screen(self, instance):
        sm.transition.direction = "right"
        sm.current = "main"
        self.translation.foreground_color = (0, 0, 0, 1)


class MainWidget(Screen):

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        multi = GridLayout(cols=2, rows=2, padding=10, spacing=5)
        self.add_widget(multi)

        # Adding Buttons
        btn1 = Button(text='Input', font_size=50)
        btn1.bind(on_press=self.open)
        btn2 = Button(text='Translate', font_size=50)
        btn2.bind(on_press=self.translate)
        btn3 = Button(text='Show', font_size=50)
        btn3.bind(on_press=self.switch_screen)
        btn4 = Button(text="Learn", font_size=50)
        btn4.bind(on_press=self.switch_learn)
        multi.add_widget(btn1)
        multi.add_widget(btn2)
        multi.add_widget(btn3)
        multi.add_widget(btn4)

        # Content for popup
        content = BoxLayout(orientation='vertical', spacing=5)

        # TextBox
        self.input_english = TextInput(text='Paste\nyour\nwords\nlike this', size_hint=(0.8, 0.9),
                                     pos_hint={'center_x': 0.5})
        content.add_widget(self.input_english)

        # Save button
        save = Button(text='Save', size_hint=(0.5, 1))
        save.bind(on_press=self.save)

        # Close button
        close = Button(text='Close', size_hint=(0.5, 1))
        close.bind(on_press=self.dismiss)

        # BoxLayout for save and close buttons
        buttons = BoxLayout(orientation='horizontal', spacing=5, pos_hint={'center_x': 0.5}, size_hint=(0.8, 0.1))
        buttons.add_widget(save)
        buttons.add_widget(close)

        content.add_widget(buttons)

        #Create popup
        self.popup = Popup(title='Input', content=content, size_hint=(0.5, 0.8),
                           size=(400, 400), auto_dismiss=True)

    def switch_learn(self, instance):
        word_widget.update()
        sm.transition.direction = "left"
        sm.current = "words"
        word_widget.translation.focus = True

    def switch_screen(self, instance):
        translated_widget.update()
        sm.transition.direction = "left"
        sm.current = "translate"

    def open(self, instance):   # Open popup
        self.popup.open()

    def dismiss(self, instance):  # Dismiss popup
        self.popup.dismiss()

    def save(self, instance):   # Save input
        with open(os.getcwd() + '/words.txt', 'w') as data:
            data.write(self.input_english.text)
        self.popup.dismiss()

    def translate(self, instance):
        Translate().clear()
        self.read_file()
        with open(os.getcwd() + "/json/words.json") as file:
            self.perCopy = json.load(file)
        template = copy.copy(self.perCopy["words"][0])
        del self.perCopy["words"][0]
        self.add_progress()
        Clock.schedule_interval(partial(self.save_json, template=template), 1 / 30.)

    def add_progress(self):
        self.pb = ProgressBar(max=self.a.__len__())
        self.pb.value = 0
        self.progress_pop = Popup(title='Translating...', content=self.pb, size_hint=(0.5, 0.1), auto_dismiss=False)
        self.progress_pop.open()

    def read_file(self):
        f = open(os.getcwd() + "/words.txt", "r")
        self.a = []
        for line in f:
            self.a.append(line.strip('\n'))

    def save_json(self, dt, template):
        global count
        template["word"] = self.a[count]
        template["matches"] = Translate().translate(self.a[count])
        self.perCopy["words"].append(copy.copy(template))
        print("Done...")
        count += 1
        self.pb.value += 1
        if self.a.__len__() == count:
            with open(os.getcwd() + "/json/words.json", 'w') as json_data:
                json_data.write(
                    json.dumps(self.perCopy, sort_keys=True, indent=4, separators=(',', ': '))
                )
            count = 0
            self.progress_pop.dismiss()
            Clock.schedule_once(self.switch_screen, 0.1)
            return False


sm_transition = SlideTransition()
sm = ScreenManager(transition=sm_transition)
sm.add_widget(MainWidget(name="main"))
translated_widget = TranslatedWidget(name="translate")
sm.add_widget(translated_widget)
word_widget = WordShower(name="words")
sm.add_widget(word_widget)

def on_press(key):
    if sm.current == "words":
        if key == Key.enter:
            print("enter pressed")
            word_widget.check()
            d = threading.Thread(target = delay)
            d.daemon = True
            d.start()

def delay():
    time.sleep(0.2)
    if not word_widget.translation.text.strip().lower() == word_widget.match_word.strip().lower():
        word_widget.translation.focus = True

# Collect events until released
class Listen():
  def __init__(self):
        with Listener(on_press=on_press) as listener:
            listener.join()

t = threading.Thread(target=Listen)
t.daemon = True
t.start()

class MainApp(App):
    def build(self):
        return sm

MainApp().run()
