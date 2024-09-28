# test_analytics.py
import pytest
from habit import Habit
from analytics import Analytics
from datetime import datetime, timedelta


def test_get_longest_streak():
    habit1 = Habit(name="Habit 1", periodicity="daily", start_date=datetime.today().date())
    habit2 = Habit(name="Habit 2", periodicity="weekly", start_date=datetime.today().date())

    # Simulate daily completions for 28 days
    for i in range(28):
        habit1.complete_task(datetime.today().date() - timedelta(days=i))

    # Simulate weekly completions for 4 weeks
    for i in range(4):
        habit2.complete_task(datetime.today().date() - timedelta(weeks=i))

    habits = [habit1, habit2]

    # The longest streak should be from habit1 (28 days)
    assert Analytics.get_longest_streak(habits) == ("Habit 1", 28)
