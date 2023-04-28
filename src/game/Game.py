import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file("src/game/game.kv")

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.tries = 20
        self.total_reward = 0
        self.target = 200
        self.rewards = [[],[],[],[],[]]

        

        self.update_info()       

    def update_info(self):

        completion = (self.total_reward / self.target)
        color = "#FF0000"
        if completion < 0.34:
            color = "#FF0000"
        elif completion < 0.66:
            color = "#FF7000"
        elif completion < 1:
            color = "#FFF000"
        else:
            color = "#00FF00"

        text = f"Tries left: {self.tries}" + \
        f"\n[size=50]Total Points: {self.total_reward}" + \
        f"\n[size=25]Target: [color={color}]{self.target}[/color][/size]"
        self.info_label.text = text

    def get_reward(self, min_reward, max_reward):
        reward = random.randint(min_reward, max_reward)
        self.total_reward += reward
        self.tries -= 1
        self.update_info()

        # Gray out all buttons except with id of restart_button if tries == 0
        if self.tries == 0:
            self.disable_buttons()
        
        return reward

    def disable_buttons(self):
        for child in reversed(self.ids.option_box.children):
            for kid in reversed(child.children):
                if isinstance(kid, Button):
                    child.disabled = True

    def enable_buttons(self):
        for child in reversed(self.ids.option_box.children):
            for kid in reversed(child.children):
                if isinstance(kid, Button):
                    child.disabled = False

    def select_option(self, button, option_number):
        if self.tries == 0:
            return

        reward = 0
        if option_number == 1:
            reward = self.get_reward(1, 20)
        elif option_number == 2:
            reward = self.get_reward(5, 15)
        elif option_number == 3:
            reward = self.get_reward(10, 12)
        elif option_number == 4:
            reward = self.get_reward(0, 25)
        elif option_number == 5:
            reward = self.get_reward(3, 18)
        
        index = option_number - 1
        self.rewards[index].append(reward)

        id = "result_label_" + str(option_number)
        self.ids[id].text = 'Average points/click: \n[b][size=25]' + str(round(sum(self.rewards[index]) / len(self.rewards[index]), 2)) + "[/size][/b]"

    def restart(self):
        for id in self.ids:
            if id.startswith("result_label_"):
                self.ids[id].text = ""

        self.tries = 20
        self.total_reward = 0
        self.enable_buttons()
        self.update_info()

class MABGame(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    Window.fullscreen = 'auto'
    MABGame().run()
