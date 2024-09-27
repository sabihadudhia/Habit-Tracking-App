import click
from manager import Manager
from habit import Habit
from analytics import Analytics
import json
from datetime import datetime

manager = Manager()

@click.group()
def cli():
    """Habit Tracking App CLI."""
    pass

@cli.command()
@click.option('--name', required=True, help='The name of the habit.')
@click.option('--periodicity', required=True, type=click.Choice(['daily', 'weekly']), help='The periodicity of the habit.')
@click.option('--start-date', required=True, type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date of the habit (YYYY-MM-DD).')
def create_habit(name, periodicity, start_date):
    """Create a new habit."""
    habit = Habit(name, periodicity, start_date)
    manager.add_habit(habit)
    click.echo(f'Habit "{name}" created!')

@cli.command()
@click.option('--name', required=True, help='The name of the habit to check off.')
def check_off(name):
    """Check off a habit."""
    habit = manager.get_habit(name)
    if habit:
        habit.complete_task()
        click.echo(f'Habit "{name}" checked off!')
    else:
        click.echo(f'Habit "{name}" not found.')

@cli.command()
def list_habits():
    """List all habits."""
    habits = manager.list_all()
    click.echo("Tracked Habits:")
    for habit in habits:
        click.echo(f"- {habit}")

@cli.command()
def analyse_habits():
    """Analyze habits."""
    # Longest streak
    longest_streak = Analytics.get_longest_streak(manager.habits)
    click.echo(f'Longest Streak: {longest_streak} periods')
    
    # List all habits
    all_habits = manager.list_all()
    click.echo("Habit List:")
    for habit in all_habits:
        click.echo(f"- {habit}")

    # List habits by periodicity
    habits_by_periodicity = Analytics.list_habits_by_periodicity(manager.habits)
    click.echo("Habits by Periodicity:")
    for periodicity, habits in habits_by_periodicity.items():
        click.echo(f"{periodicity.capitalize()}: {', '.join(habits)}")


@cli.command()
@click.option('--name', required=True, help='The name of the habit to delete.')
def delete_habit(name):
    """Delete a habit."""
    manager.remove_habit(name)
    click.echo(f'Habit "{name}" deleted!')

@cli.command()
@click.option('--filename', required=True, help='File name to save habits.')
def save_habits(filename):
    """Save habits to a file."""
    manager.save_habits(filename)
    click.echo(f'Habits saved to {filename}.')

@cli.command()
@click.option('--filename', required=True, help='File name to load habits.')
def load_habits(filename):
    """Load habits from a file."""
    manager.load_habits(filename)
    click.echo(f'Habits loaded from {filename}.')

if __name__ == '__main__':
    cli()
