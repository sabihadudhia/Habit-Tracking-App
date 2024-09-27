import json
from datetime import datetime, timedelta, date
from habit import Habit


class Manager:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit):
        """Adds a new habit to the manager."""
        self.habits.append(habit)

    def remove_habit(self, habit_name):
        """Removes a habit by name."""
        self.habits = [habit for habit in self.habits if habit.name != habit_name]

    def get_habit(self, habit_name):
        """Retrieves a habit by name."""
        for habit in self.habits:
            if habit.name == habit_name:
                return habit
        return None
    
    def list_all(self):
        return self.habits  


    def save_habits(self, filename):
        """Saves the habits to a JSON file."""
        with open(filename, 'w') as file:
            json.dump([habit.convert_dictionary() for habit in self.habits], file)

    def load_habits(self, filename):
        """Loads habits from a JSON file."""
        try:
            with open(filename, 'r') as file:
                habits_data = json.load(file)
                for habit_data in habits_data:
                    habit = Habit(
                        name=habit_data['name'],
                        periodicity=habit_data['periodicity'],
                        start_date=datetime.fromisoformat(habit_data['start_date'])
                    )
                    habit.completion_dates = [datetime.fromisoformat(date) for date in habit_data['completion_dates']]
                    habit.streak = habit_data['streak']
                    habit.history = [datetime.fromisoformat(date) for date in habit_data['history']]
                    self.add_habit(habit)
        except FileNotFoundError:
            print("File not found, starting with an empty habit list.")
