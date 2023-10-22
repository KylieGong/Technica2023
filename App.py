from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from datetime import date
import re
import sys
import os

waste = {}

class WasteInput(Screen):
    def __init__(self, **kwargs):
        super(WasteInput, self).__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        # RGBA format, (R, G, B, A) same as rgb but a is opacity
        Window.clearcolor = (170/255, 170/255, 136/255, 1)

        # add widgets
        self.window.add_widget(Image(source="Placeholder.png"))

        self.wastegreeting = Label(text="Input your waste here: ")
        self.window.add_widget(self.wastegreeting)

        # landfill
        self.landfill_lbl = Label(text="Landfill: ", font_size = 15, color = "4B3D2A")
        self.window.add_widget(self.landfill_lbl)
        self.landfill = TextInput(multiline = False, size_hint = (1, 0.5))
        self.window.add_widget(self.landfill)

        # recycle
        self.recycle_lbl = Label(text="Recycle: ", font_size = 15, color = "4B3D2A")
        self.window.add_widget(self.recycle_lbl)
        self.recycle = TextInput(multiline = False, size_hint = (1, 0.5))
        self.window.add_widget(self.recycle)

        # compost
        self.compost_lbl = Label(text="Compost: ", font_size = 15, color = "4B3D2A")
        self.window.add_widget(self.compost_lbl)
        self.compost = TextInput(multiline = False, size_hint = (1, 0.5))
        self.window.add_widget(self.compost)

        self.throw = Button(text="Throw Away", color = "000000", size_hint = (1, 0.5), bold = True, background_color = "BFDF8E", background_normal = "")
        self.throw.bind(on_press=self.throwAway)
        self.window.add_widget(self.throw)
        
        self.history = Button(text="Check History", color = "000000", size_hint = (1, 0.5), bold = True, background_color = "BFDF8E", background_normal = "")
        self.history.bind(on_press=self.checkHistory)
        self.window.add_widget(self.history)
        
        self.add_widget(self.window)
    
    def throwAway(self, instance):
        text = []
        currdate = str(date.today())
        if currdate in waste:
            today = waste[currdate]
            if "recycle" in today:
                if self.recycle.text in today["recycle"]:
                    today["recycle"][self.waste.text] += 1
            else:
                today["recycle"][self.recycle.text] = 1
        else:
            if self.landfill.text:
                text.append(self.landfill.text)
                waste[currdate] = {"landfill": {self.landfill.text:1}}
            if self.recycle.text:
                text.append(self.recycle.text)
                waste[currdate] = {"recycle": {self.recycle.text:1}}
            if self.compost.text:
                text.append(self.compost.text)
                waste[currdate] = {"compost": {self.compost.text:1}}
        if text:
            print(text)
            self.wastegreeting.text = "You just threw away " + ', '.join(text) + "????? How could you!"

    def checkHistory(self, instance):
        app.root.current = 'WasteHistory'

class History(Screen):
    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        label = Label(text="idk")
        self.add_widget(label)

class WasteTracker(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WasteInput(name='WasteInput'))
        sm.add_widget(History(name='WasteHistory'))
        return sm

if __name__ == '__main__':
    app = WasteTracker()

    try:
        sys.exit(app.run())
    except SystemExit:
        f = open("history.txt", "a")
        for i in waste.keys():
            f.write(i+"\n")
            for key, val in waste[i].items():
                f.write("\t" + key + ": " + str(val) + "\n")
        f.close()
