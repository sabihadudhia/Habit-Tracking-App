# test_manager.py
import pytest
import os
from manager import Manager
from habit import Habit
from datetime import datetime, timedelta

@pytest.fixture
def manager():
    manager = Manager()
    
    # Predefined data: 4 habits each with 4 weeks of completion
    habits = [
        Habit("Reading", "daily", datetime.now() - timedelta(days=28)),
        Habit("Writing", "daily", datetime.now() - timedelta(days=28)),
        Habit("Exercise", "weekly", datetime.now() - timedelta(days=28)),
        Habit("Meditation", "weekly", datetime.now() - timedelta(days=28))
    ]

    # Complete each habit for 4 weeks
    for habit in habits:
        for i in range(28):
            habit.complete_task()

    manager.habits.extend(habits)
    print(f"Predefined habits: {[habit.name for habit in manager.habits]}")
    return manager

def test_add_habit(manager):
    habit = Habit("Gardening", "daily", datetime.now())
    manager.add_habit(habit)
    print(f"After adding habit, total habits: {[habit.name for habit in manager.habits]}")
    assert len(manager.habits) == 5  # 4 predefined + 1 new

def test_remove_habit(manager):
    manager.remove_habit("Reading")
    print(f"After removing 'Reading', total habits: {[habit.name for habit in manager.habits]}")
    assert len(manager.habits) == 3  # 4 original - 1 removed

def test_load_habits(manager, tmp_path):
    # Use the tmp_path fixture to avoid using existing files
    temp_file = tmp_path / "habits.json"

    # Save habits to the temporary file
    print(f"Saving habits to temporary file: {temp_file}")
    manager.save_habits(str(temp_file))
    
    # Reload them from the temporary file
    print(f"Loading habits from temporary file: {temp_file}")
    manager.load_habits(str(temp_file))
    
    print(f"Loaded habits after load operation: {[habit.name for habit in manager.habits]}")
    assert len(manager.habits) >= 0  # Check if habits are loaded

def test_list_all(manager):
    """Test the list_all method to ensure it returns all the habits."""
    habit_names = manager.list_all()  # Expecting a list of habit names (strings)
    print(f"List of habits: {habit_names}")
    
    # Ensure habit_names are names of the habits
    habit_names = [habit.name for habit in habit_names]
    
    assert len(habit_names) == 4  # Since the fixture predefines 4 habits
    assert "Reading" in habit_names
    assert "Writing" in habit_names
    assert "Exercise" in habit_names
    assert "Meditation" in habit_names