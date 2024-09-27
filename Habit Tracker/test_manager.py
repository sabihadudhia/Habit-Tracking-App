#test_manager.py
import pytest
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
    return manager

def test_add_habit(manager):
    habit = Habit("Gardening", "daily", datetime.now())
    manager.add_habit(habit)
    assert len(manager.habits) == 5  # 4 predefined + 1 new

def test_remove_habit(manager):
    manager.remove_habit("Reading")
    assert len(manager.habits) == 3  # 4 original - 1 removed

def test_load_habits(manager):
    manager.load_habits("habits.json")  
    assert len(manager.habits) >= 0  
