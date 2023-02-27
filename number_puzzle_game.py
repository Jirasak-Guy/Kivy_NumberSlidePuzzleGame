from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class SlidingPuzzle(GridLayout):
    pass


class MyGame(App):
    def build(self):
        return SlidingPuzzle()

MyGame().run()