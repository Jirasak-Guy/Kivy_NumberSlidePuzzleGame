from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class SlidingPuzzle(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 4
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()

    def generate_tiles(self):
        nums = list(range(1, 16))
        nums.append(None)
        for num in nums:
            button = Button(text=str(num) if num else "", font_size=50)
            self.tiles.append(button)

    def add_tiles(self):
        for tile in self.tiles:
            self.add_widget(tile)


class MyGame(App):
    def build(self):
        return SlidingPuzzle()

MyGame().run()