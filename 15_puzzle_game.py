from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.uix.floatlayout import FloatLayout

import random

class MainMenu(FloatLayout):
    def __init__(self, start_callback, level_callback, **kwargs):
        super().__init__(**kwargs)
        self.start_callback = start_callback
        self.level_callback = level_callback
        self.add_start_button()
        self.add_level_button()

    def add_start_button(self):
        start_button = Button(text="Start Game", size_hint=(0.5, 0.2), pos_hint={'x': 0.25, 'y': 0.5})
        start_button.bind(on_press=self.start_callback)
        self.add_widget(start_button)

    def add_level_button(self):
        level_button = Button(text="Select Level", size_hint=(0.5, 0.2), pos_hint={'x': 0.25, 'y': 0.3})
        level_button.bind(on_press=self.level_callback)
        self.add_widget(level_button)


class SlidingPuzzle(GridLayout):
    def __init__(self, rows, cols, **kwargs):
        super().__init__(**kwargs)
        self.cols = cols
        self.rows = rows
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()
        # Set the background color of the grid
        with self.canvas.before:
            Color(225, 223, 208, 0.4)  # background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    # rest of the code remains the same


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def generate_tiles(self):
        nums = random.sample(range(1, 9), 8)
        while not self.is_solvable(nums):
            nums = random.sample(range(1, 9), 8)
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
                    victory_popup.bind(on_dismiss=self.reset_tiles)
                    victory_popup.open()

    def check_win(self):
        nums = [int(tile.text) if tile.text else None for tile in self.tiles]
        return nums == list(range(1, 9)) + [None]

    def reset_tiles(self, instance):
        self.clear_widgets()
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()


class MyGame(App):
    def build(self):
        main_menu = MainMenu(self.start_game, self.select_level)
        return main_menu

    def start_game(self, instance):
        # Create the game with default settings (4x4 grid)
        game = SlidingPuzzle(rows=4, cols=4)
        self.root = game

    def select_level(self, instance):
        # Create a level selection popup
        level_popup = Popup(title='Select Level', size_hint=(None, None), size=(400, 200))
        level_layout = FloatLayout()
        level_popup.add_widget(level_layout)

        # Add level selection buttons
        level_3_button = Button(text='3x3', size_hint=(0.3, 0.3), pos_hint={'x': 0.1, 'y': 0.5})
        level_3_button.bind(on_press=lambda _: self.create_game(3, 3))
        level_layout.add_widget(level_3_button)

        level_4_button = Button(text='4x4', size_hint=(0.3, 0.3), pos_hint={'x': 0.4, 'y': 0.5})
        level_4_button.bind(on_press=lambda _: self.create_game(4, 4))
        level_layout.add_widget(level_4_button)

        level_5_button = Button(text='5x5', size_hint=(0.3, 0.3), pos_hint={'x': 0.7, 'y': 0.5})
        level_5_button.bind(on_press=lambda _: self.create_game(5, 5))
        level_layout.add_widget(level_5_button)

        # Add a cancel button to close the popup
        cancel_button = Button(text='Cancel', size_hint=(0.3, 0.3), pos_hint={'x': 0.35, 'y': 0.1})
        cancel_button.bind(on_press=level_popup.dismiss)
        level_layout.add_widget(cancel_button)

        level_popup.open()

    def create_game(self, rows, cols):
        # Create the game with the selected number of rows and columns
        game = SlidingPuzzle(rows=rows, cols=cols)
        self.root = game


MyGame().run()
