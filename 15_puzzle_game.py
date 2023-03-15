from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
import random


class StartMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text='Menu', font_size=dp(50), bold=True,
                            color=(1, 1, 1, 1), size_hint=(1, 0.4),
                            pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.add_widget(title_label)

        start_button = Button(text="Start Game", font_size=dp(30),
                              size_hint=(0.4, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        start_button.bind(on_press=self.switch_to_game)
        self.add_widget(start_button)

    def switch_to_game(self, instance):
        self.manager.current = 'select'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class Select(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text='Select board size:', font_size=dp(50), bold=True,
                            color=(1, 1, 1, 1), size_hint=(1, 0.4),
                            pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.add_widget(title_label)

        size_button_3 = Button(text="3x3", font_size=dp(30),size_hint=(0.4, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        size_button_3.bind(on_press=self.switch_to_game_3x3)
        self.add_widget(size_button_3)

        size_button_4 = Button(text="4x4", font_size=dp(30),size_hint=(0.4, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        size_button_4.bind(on_press=self.switch_to_game_4x4)
        self.add_widget(size_button_4)

        size_button_5 = Button(text="5x5", font_size=dp(30),size_hint=(0.4, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        size_button_5.bind(on_press=self.switch_to_game_5x5)
        self.add_widget(size_button_5)
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)
        
    def go_back(self, instance):
        self.manager.current = "menu"

    def switch_to_game_3x3(self, instance):
        self.manager.current = '3x3'

    def switch_to_game_4x4(self, instance):
        self.manager.current = '4x4'

    def switch_to_game_5x5(self, instance):
        self.manager.current = '5x5'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class NinePuzzle(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.di = self.cols * self.rows
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
        nums = random.sample(range(1, self.di), self.di-1)
        while not self.is_solvable(nums):
            nums = random.sample(range(1, self.di), self.di-1)
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
                    # Create a Victory popup
                    victory_popup = Popup(title='', size_hint=(None, None), size=(400, 400),)
                    victory_popup_content = Label(text='You won!', font_size=50, color=(1, 1, 1, 1))  # set text color to black
                    victory_popup_content.background_color = (145, 99, 46, 0.8) # set background color to white
                    victory_popup.add_widget(victory_popup_content)
                    victory_popup.bind(on_dismiss=self.reset_tiles)
                    victory_popup.open()

            
    def check_win(self):
        nums = [int(tile.text) if tile.text else None for tile in self.tiles]
        return nums == list(range(1, self.di)) + [None]

    def reset_tiles(self, instance):
        self.clear_widgets()
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()

class FifteenPuzzle(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 4
        self.di = self.cols * self.rows
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
        nums = random.sample(range(1, self.di), self.di-1)
        while not self.is_solvable(nums):
            nums = random.sample(range(1, self.di), self.di-1)
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
                    victory_popup = Popup(title='', size_hint=(None, None), size=(400, 400),)
                    victory_popup_content = Label(text='You won!', font_size=50, color=(1, 1, 1, 1))  # set text color to black
                    victory_popup_content.background_color = (145, 99, 46, 0.8) # set background color to white
                    victory_popup.add_widget(victory_popup_content)
                    victory_popup.bind(on_dismiss=self.reset_tiles)
                    victory_popup.open()

            
    def check_win(self):
        nums = [int(tile.text) if tile.text else None for tile in self.tiles]
        return nums == list(range(1, self.di)) + [None]

    def reset_tiles(self, instance):
        self.clear_widgets()
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()

class TwentyFivePuzzle(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.rows = 5
        self.di = self.cols * self.rows
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
        nums = random.sample(range(1, self.di), self.di-1)
        while not self.is_solvable(nums):
            nums = random.sample(range(1, self.di), self.di-1)
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
                    # Create a Victory popup
                    victory_popup = Popup(title='', size_hint=(None, None), size=(400, 400),)
                    victory_popup_content = Label(text='You won!', font_size=50, color=(1, 1, 1, 1))  # set text color to black
                    victory_popup_content.background_color = (145, 99, 46, 0.8) # set background color to white
                    victory_popup.add_widget(victory_popup_content)
                    victory_popup.bind(on_dismiss=self.reset_tiles)
                    victory_popup.open()

            
    def check_win(self):
        nums = [int(tile.text) if tile.text else None for tile in self.tiles]
        return nums == list(range(1, self.di)) + [None]

    def reset_tiles(self, instance):
        self.clear_widgets()
        self.tiles = []
        self.generate_tiles()
        self.add_tiles()

class GameScreen3x3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(NinePuzzle())
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def go_back(self, instance):
        self.manager.current = "select"
class GameScreen4x4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FifteenPuzzle())
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)
    def go_back(self, instance):
        self.manager.current = "select"
class GameScreen5x5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TwentyFivePuzzle())
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)
    def go_back(self, instance):
        self.manager.current = "select"
        
class MyGame(App):
    def build(self):
        # Create a screen manager and add the start and game screens
        sm = ScreenManager()
        sm.add_widget(StartMenu(name='menu'))
        sm.add_widget(Select(name='select'))
        sm.add_widget(GameScreen3x3(name='3x3'))
        sm.add_widget(GameScreen4x4(name='4x4'))
        sm.add_widget(GameScreen5x5(name='5x5'))
        return sm

MyGame().run()
