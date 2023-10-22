from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.graphics import Line
from kivy.uix.widget import Widget

import webbrowser
import json
from datetime import date
import sys
import os

waste = {"landfill": {},
         "recycle": {},
         "compost": {}}

class WasteInput(Screen):
    def __init__(self, **kwargs):
        super(WasteInput, self).__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        # RGBA format, (R, G, B, A) same as rgb but a is opacity
        Window.clearcolor = (242/255, 240/255, 204/255, 1)

        # add widgets
        self.window.add_widget(Image(source="Placeholder.png"))

        self.wastegreeting = Label(text="Input your waste here: ", color = "000000", font_size = 18)
        self.window.add_widget(self.wastegreeting)

        # landfill
        self.landfill_lbl = Label(text="Landfill: ", font_size = 15, color = "000000")
        self.window.add_widget(self.landfill_lbl)
        self.landfill = TextInput(multiline = False, size_hint = (1, 0.5))
        self.window.add_widget(self.landfill)

        # recycle
        self.recycle_lbl = Label(text="Recycle: ", font_size = 15, color = "000000")
        self.window.add_widget(self.recycle_lbl)
        self.recycle = TextInput(multiline = False, size_hint = (1, 0.5))
        self.window.add_widget(self.recycle)

        # compost
        self.compost_lbl = Label(text="Compost: ", font_size = 15, color = "000000")
        self.window.add_widget(self.compost_lbl)
        self.compost = TextInput(multiline = False, size_hint = (1, 0.5))
        self.window.add_widget(self.compost)

    

        self.throw = Button(text="Throw Away", color = "000000", size_hint = (0.9, 0.5), bold = True, background_color = "99BB55", background_normal = "")
        self.throw.bind(on_release=self.throwAway)
        self.window.add_widget(self.throw)
        
        self.history = Button(text="Check History", color = "000000", size_hint = (0.9, 0.5), bold = True, background_color = "99BB55", background_normal = "")
        self.history.bind(on_release=self.checkHistory)
        self.window.add_widget(self.history)
        
        self.add_widget(self.window)
    
    def throwAway(self, instance):
        text = []
        # landfill
        if self.landfill.text:
            text.append(self.landfill.text)
            if self.landfill.text in waste["landfill"]:
                waste["landfill"][self.landfill.text] += 1
            else:
                waste["landfill"][self.landfill.text] = 1
            self.landfill.text = ""

        # recycle
        if self.recycle.text:
            text.append(self.recycle.text)
            if self.recycle.text in waste["recycle"]:
                waste["recycle"][self.recycle.text] += 1
            else:
                waste["recycle"][self.recycle.text] = 1
            self.recycle.text = ""

        # compost
        if self.compost.text:
            text.append(self.compost.text)
            if self.compost.text in waste["compost"]:
                waste["compost"][self.compost.text] += 1
            else:
                waste["compost"][self.compost.text] = 1
            self.compost.text = ""
        if text:
            self.wastegreeting.text = "You just threw away " + ', '.join(text) + "????? How could you!"

            data = json.dumps(waste, indent=4)
            f = open(currdate+".json", "w")
            f.write(data)
            f.close()

    def checkHistory(self, instance):
        app.root.current = 'WasteHistory'

class History(Screen):
    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        MainBox = BoxLayout(orientation='vertical', padding=50)

        toWasteInput = Button(text="Input Waste", color = "000000", bold = True, background_color = "BFDF8E", background_normal = "")
        toWasteInput.bind(on_release=self.toInput)
        moreInfoBtn = Button(text="Waste Disposal Info", color = "000000", bold = True, background_color = "BFDF8E", background_normal = "")
        moreInfoBtn.bind(on_release=self.moreInfo)

        btnlayout = BoxLayout(orientation='horizontal')
        btnlayout.add_widget(toWasteInput)
        btnlayout.add_widget(moreInfoBtn)
        MainBox.add_widget(btnlayout)

        label = Label(text="Today you have: ", color = "000000")
        MainBox.add_widget(label)

        # recycle
        r_box = BoxLayout(orientation='horizontal')
        recycle_lbl = Label(text="Recycled: ", color="1d4c00")
        r_box.add_widget(recycle_lbl)
        recycled_layout = BoxLayout(orientation='vertical')
        for k, v in waste["recycle"].items():
            item = Label(text=f"{k}: {v}", color = "1d4c00")
            recycled_layout.add_widget(item)
        r_box.add_widget(recycled_layout)
        
        # landfill
        l_box = BoxLayout(orientation='horizontal')
        landfill_lbl = Label(text="Trashed: ", color = "1d4c00")
        l_box.add_widget(landfill_lbl)
        landfill_layout = BoxLayout(orientation='vertical')
        for k, v in waste["landfill"].items():
            item = Label(text=f"{k}: {v}", color = "1d4c00")
            landfill_layout.add_widget(item)
        l_box.add_widget(landfill_layout)

        # compost
        c_box = BoxLayout(orientation='horizontal')
        compost_lbl = Label(text="Composted: ", color = "4B3D2A")
        c_box.add_widget(compost_lbl)
        composted_layout = BoxLayout(orientation='vertical')
        for k, v in waste["compost"].items():
            item = Label(text=f"{k}: {v}", color = "4B3D2A")
            composted_layout.add_widget(item)
        c_box.add_widget(composted_layout)
        
        # add to the main layout
        MainBox.add_widget(r_box)
        MainBox.add_widget(c_box)
        MainBox.add_widget(l_box)

        self.add_widget(MainBox)
    
    def toInput(self, instance):
        app.root.current = 'WasteInput'

    def moreInfo(self, instance):
        webbrowser.open("https://technica-2023.jlinx11.repl.co/")

class WasteTracker(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WasteInput(name='WasteInput'))
        sm.add_widget(History(name='WasteHistory'))
        return sm

if __name__ == '__main__':
    currdate = str(date.today())

    file_name = currdate+".json"
    if os.path.isfile(file_name):
        with open(file_name, "r") as file:
            waste = json.load(file)

    app = WasteTracker()

    try:
        sys.exit(app.run())
    except SystemExit:
        data = json.dumps(waste, indent=4)
        f = open(currdate+".json", "w")
        f.write(data)
        f.close()
