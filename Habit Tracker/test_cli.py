#test_cli.py
import pytest
from click.testing import CliRunner
from cli import cli
from manager import Manager
from habit import Habit
from datetime import datetime, timedelta

@pytest.fixture
def setup_manager():
    return Manager()


# Helper function to create habits and simulate 4 weeks of data
def setup_habits(manager):
    # Create some daily habits
    habit1 = Habit(name="Exercise", periodicity="daily", start_date=datetime.now() - timedelta(weeks=4))
    habit2 = Habit(name="Reading", periodicity="daily", start_date=datetime.now() - timedelta(weeks=4))

    # Create some weekly habits
    habit3 = Habit(name="Cleaning", periodicity="weekly", start_date=datetime.now() - timedelta(weeks=4))
    habit4 = Habit(name="Laundry", periodicity="weekly", start_date=datetime.now() - timedelta(weeks=4))

    # Simulate task completion for 4 weeks
    for i in range(28):  # 28 days for daily habits
        habit1.complete_task(datetime.now() - timedelta(days=28 - i))
        habit2.complete_task(datetime.now() - timedelta(days=28 - i))

    for i in range(4):  # 4 weeks for weekly habits
        habit3.complete_task(datetime.now() - timedelta(weeks=4 - i))
        habit4.complete_task(datetime.now() - timedelta(weeks=4 - i))

    # Add habits to manager
    manager.add_habit(habit1)
    manager.add_habit(habit2)
    manager.add_habit(habit3)
    manager.add_habit(habit4)

# Fixture to set up Manager and CliRunner
@pytest.fixture
def setup_manager():
    manager = Manager()
    # Create some daily habits
    habit1 = Habit(name="Exercise", periodicity="daily", start_date=datetime.now() - timedelta(weeks=4))
    habit2 = Habit(name="Reading", periodicity="daily", start_date=datetime.now() - timedelta(weeks=4))

    # Create some weekly habits
    habit3 = Habit(name="Cleaning", periodicity="weekly", start_date=datetime.now() - timedelta(weeks=4))
    habit4 = Habit(name="Laundry", periodicity="weekly", start_date=datetime.now() - timedelta(weeks=4))

    # Simulate task completion for 4 weeks
    for i in range(28):  # 28 days for daily habits
        habit1.complete_task(datetime.now() - timedelta(days=28 - i))
        habit2.complete_task(datetime.now() - timedelta(days=28 - i))

    for i in range(4):  # 4 weeks for weekly habits
        habit3.complete_task(datetime.now() - timedelta(weeks=4 - i))
        habit4.complete_task(datetime.now() - timedelta(weeks=4 - i))

    # Add habits to manager
    manager.add_habit(habit1)
    manager.add_habit(habit2)
    manager.add_habit(habit3)
    manager.add_habit(habit4)

    return manager

@pytest.fixture
def runner():
    return CliRunner()


# Test creating a new habit
def test_create_habit(runner, setup_manager):
    result = runner.invoke(cli, ['create-habit', '--name', 'Meditation', '--periodicity', 'daily', '--start-date', '2023-09-01'], obj=setup_manager)
    assert result.exit_code == 0
    assert 'Habit "Meditation" created!' in result.output

# Test checking off a habit
def test_check_off_habit(runner):
    # Setup test data
    result = runner.invoke(cli, ['create-habit', '--name', 'Exercise', '--periodicity', 'daily', '--start-date', '2023-08-01'])
    print(f'Create habit result: {result.output}')
    
    # Check off the habit
    result = runner.invoke(cli, ['check-off', '--name', 'Exercise'])
    print(f'Check off habit result: {result.output}')
    
    # Verify habit was checked off
    assert 'Habit "Exercise" checked off!' in result.output


# Test listing habits
def test_list_habits(runner):
    # Setup test data
    runner.invoke(cli, ['create-habit', '--name', 'Exercise', '--periodicity', 'daily', '--start-date', '2023-08-01'])
    runner.invoke(cli, ['create-habit', '--name', 'Reading', '--periodicity', 'weekly', '--start-date', '2023-08-01'])

    # List habits
    result = runner.invoke(cli, ['list-habits'])
    print(f'List habits result: {result.output}')
    
    # Verify habits are listed correctly
    assert 'Exercise' in result.output
    assert 'Reading' in result.output


# Test analyzing habits
def test_analyse_habits(runner):
    # Setup test data
    runner.invoke(cli, ['create-habit', '--name', 'Exercise', '--periodicity', 'daily', '--start-date', '2023-08-01'])
    runner.invoke(cli, ['create-habit', '--name', 'Reading', '--periodicity', 'weekly', '--start-date', '2023-08-01'])
    
    # Complete some tasks to generate streaks
    runner.invoke(cli, ['check-off', '--name', 'Exercise'])
    
    # Analyse habits
    result = runner.invoke(cli, ['analyse-habits'])
    print(f'Analyse habits result: {result.output}')
    
    # Verify analysis results
    assert 'Longest Streak' in result.output
    assert 'Exercise' in result.output

# Test deleting a habit
def test_delete_habit(runner):
    # Setup test data
    runner.invoke(cli, ['create-habit', '--name', 'Exercise', '--periodicity', 'daily', '--start-date', '2023-08-01'])

    # Delete habit
    result = runner.invoke(cli, ['delete-habit', '--name', 'Exercise'])
    print(f'Delete habit result: {result.output}')
    
    # Verify habit is deleted
    assert 'Habit "Exercise" deleted!' in result.output
    
    # Verify it's no longer in the list
    result = runner.invoke(cli, ['list-habits'])
    print(f'List habits after deletion: {result.output}')
    assert 'Exercise' not in result.output

# Test saving habits to a file
def test_save_habits(runner, setup_manager, tmp_path):
    save_file = tmp_path / "habits.json"
    
    # Pass the manager instance to the CLI context
    result = runner.invoke(cli, ['save-habits', '--filename', str(save_file)], obj=setup_manager)
    
    assert result.exit_code == 0  # Check if the command executed successfully
    assert f'Habits saved to {save_file}' in result.output  # Check for success message

# Test loading habits from a file
def test_load_habits(runner):
    # Reset the manager instance or start fresh
    manager = Manager()
    manager.habits = []  # Clear any pre-existing habits

    # Setup test data by saving habits first
    runner.invoke(cli, ['create-habit', '--name', 'Exercise', '--periodicity', 'daily', '--start-date', '2023-08-01'])
    runner.invoke(cli, ['save-habits', '--filename', 'test_habits.json'])

    # Load habits from file
    result = runner.invoke(cli, ['load-habits', '--filename', 'test_habits.json'], obj=manager)
    print(f'Load habits result: {result.output}')

    # Verify habits are loaded
    result = runner.invoke(cli, ['list-habits'], obj=manager)
    print(f'List habits after loading: {result.output}')

    assert 'Exercise' in result.output
    assert len(result.output.splitlines()) == 8
