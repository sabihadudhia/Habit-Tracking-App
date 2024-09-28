#test_habit.py
import datetime
import pytest
from habit import Habit

# Test completing tasks and checking streaks
def test_complete_task():
    habit = Habit(name="Test Habit", periodicity="daily", start_date=datetime.date.today())
    
    # Simulate completing the task every day for 28 days
    for i in range(28):
        habit.complete_task(datetime.date.today() - datetime.timedelta(days=i))
    
    assert len(habit.completion_dates) == 28
    assert habit.get_streak() == 28

def test_get_streak():
    habit = Habit(name="Test Habit", periodicity="daily", start_date=datetime.date.today())

    # Complete tasks for 29 consecutive days
    for i in range(29):
        habit.complete_task(datetime.date.today() - datetime.timedelta(days=i))

    assert habit.get_streak() == 29

@pytest.mark.parametrize("periodicity, expected_streak", [
    ('daily', 28),
    ('weekly', 4),
])
def test_streak_with_different_periodicities(periodicity, expected_streak):
    habit = Habit(name="Test Habit", periodicity=periodicity, start_date=datetime.date.today())

    # Complete the task for 4 weeks, with appropriate intervals
    for i in range(28):
        if periodicity == 'daily':
            habit.complete_task(datetime.date.today() - datetime.timedelta(days=i))
        elif periodicity == 'weekly' and i % 7 == 0:
            habit.complete_task(datetime.date.today() - datetime.timedelta(days=i))

    assert habit.get_streak() == expected_streak
