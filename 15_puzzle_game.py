from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
import random

class SlidingPuzzle(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 4
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()
        # Set the background color of the grid
        with self.canvas.before:
            Color(225, 223, 208, 0.4)  # background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def generate_tiles(self):
        nums = random.sample(range(1, 16), 15)
        while not self.is_solvable(nums):
            nums = random.sample(range(1, 16), 15)
        nums.append(None)
        for num in nums:
            button = Button(text=str(num) if num else "", font_size=100, background_color=(225, 223, 208, 0.8), color=(0, 0, 0, 0.6))
            button.bind(on_press=self.move_tile)
            self.tiles.append(button)

    def is_solvable(self, nums):
        inversion_count = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] and nums[j] and nums[i] > nums[j]:
                    inversion_count += 1
        return inversion_count % 2 == 0

    def add_tiles(self):
        for tile in self.tiles:
            self.add_widget(tile)

    def move_tile(self, button):
        index = self.tiles.index(button)
        row, col = divmod(index, self.cols)
        adjacent_indices = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        for row, col in adjacent_indices:
            if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                continue
            index = row*self.cols + col
            if not self.tiles[index].text:
                self.tiles[index].text = button.text
                button.text = ""
                if self.check_win():
                # Create a Victory popup
                    victory_popup = Popup(title='', size_hint=(None, None), size=(400, 400),)
                    victory_popup_content = Label(text='You won!', font_size=50, color=(1, 1, 1, 1))  # set text color to black
                    victory_popup_content.background_color = (145, 99, 46, 0.8) # set background color to white
                    victory_popup.add_widget(victory_popup_content)
                    victory_popup.open()

            
    def check_win(self):
        nums = [int(tile.text) if tile.text else None for tile in self.tiles]
        return nums == list(range(1, 16)) + [None]

class MyGame(App):
    def build(self):
        return SlidingPuzzle()

MyGame().run()
