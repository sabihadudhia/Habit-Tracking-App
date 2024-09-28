import json
from datetime import datetime
from habit import Habit

class Manager:
    def __init__(self, filename=None):
        self.habits = []
        print("Initialized Manager with an empty habits list.")
        if filename:
            self.load_habits(filename)  # Load habits if filename is provided

    def add_habit(self, habit):
        """Adds a new habit to the manager."""
        self.habits.append(habit)
        print(f"Added habit: {habit.name}")

    def remove_habit(self, habit_name):
        """Removes a habit by name."""
        original_count = len(self.habits)
        self.habits = [habit for habit in self.habits if habit.name != habit_name]
        new_count = len(self.habits)
        print(f"Removed habit: {habit_name}. Total habits changed from {original_count} to {new_count}.")

    def get_habit(self, habit_name):
        """Retrieves a habit by name."""
        for habit in self.habits:
            if habit.name == habit_name:
                print(f"Retrieved habit: {habit.name}")
                return habit
        print(f"Habit {habit_name} not found.")
        return None

    def save_habits(self, filename):
        """Saves the habits to a JSON file."""
        with open(filename, 'w') as file:
            print(f"Saving habits to {filename}")
            json.dump([habit.convert_dictionary() for habit in self.habits], file)
            print(f"Saved data: {[habit.convert_dictionary() for habit in self.habits]}")

    def list_all(self):
        """Return all tracked habits."""
        print(f"Listing all habits: {[habit.name for habit in self.habits]}")
        return self.habits

    def load_habits(self, filename):
        print(f"Loading habits from {filename}")
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                print(f"Loaded data: {data}")
                for habit_data in data:
                    habit = Habit.from_dict(habit_data)
                    if not self.get_habit(habit.name):  # Avoid adding duplicates
                        self.add_habit(habit)
                        print(f"Added habit: {habit.name}")
                    else:
                        print(f"Habit {habit.name} already exists, skipping addition.")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty habits list.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file {filename}. Starting with an empty habits list.")
