import click
from manager import Manager
from habit import Habit
from analytics import Analytics
from datetime import datetime

# Initialize a global manager instance
manager = Manager('habits.json')  # Load habits from the specified file at startup

@click.group()
@click.pass_context
def cli(ctx):
    """Habit Tracking App CLI."""
    ctx.obj = manager  # Pass the manager instance to the context
    pass

@cli.command()
@click.option('--name', required=True, help='The name of the habit.')
@click.option('--periodicity', required=True, type=click.Choice(['daily', 'weekly']), help='The periodicity of the habit.')
@click.option('--start-date', required=True, type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date of the habit (YYYY-MM-DD).')
def create_habit(name, periodicity, start_date):
    """Create a new habit."""
    habit = Habit(name, periodicity, start_date)
    manager.add_habit(habit)
    manager.save_habits('habits.json')  # Save habits after creating
    click.echo(f'Habit "{name}" created!')

@cli.command()
@click.option('--name', required=True, help='The name of the habit to check off.')
@click.pass_context
def check_off(ctx, name):
    """Check off a habit."""
    habit = ctx.obj.get_habit(name)  # Use context to get manager instance
    if habit:
        habit.complete_task()
        manager.save_habits('habits.json')  # Save habits after checking off
        click.echo(f'Habit "{name}" checked off!')
    else:
        click.echo(f'Habit "{name}" not found.')

@cli.command()
@click.pass_context
def analyse_habits(ctx):
    """Analyze habits."""
    if not ctx.obj.habits:
        click.echo("No habits to analyze.")
        return

    # Longest streak
    longest_streak = Analytics.get_longest_streak(ctx.obj.habits)
    click.echo(f'Longest Streak: {longest_streak} periods')

    # List all habits
    click.echo("\nHabit List:")
    all_habits = ctx.obj.list_all()
    for habit in all_habits:
        click.echo(f"- {habit.name} (Periodicity: {habit.periodicity})")

    # List habits by periodicity
    habits_by_periodicity = Analytics.list_habits_by_periodicity(ctx.obj.habits)
    click.echo("\nHabits by Periodicity:")
    for periodicity in ['daily', 'weekly']:
        habits = habits_by_periodicity.get(periodicity, [])
        click.echo(f"{periodicity.capitalize()}: {', '.join([habit.name for habit in habits]) if habits else 'None'}")

@cli.command()
@click.option('--name', required=True, help='The name of the habit to delete.')
def delete_habit(name):
    """Delete a habit."""
    manager.remove_habit(name)
    manager.save_habits('habits.json')  # Save habits after deletion
    click.echo(f'Habit "{name}" deleted!')

@cli.command()
def list_habits():
    """List all tracked habits."""
    habits = manager.list_all()
    if not habits:
        click.echo("No habits found.")
    else:
        click.echo("Tracked Habits:")
        for habit in habits:
            click.echo(f"- {habit.name}")

@cli.command()
@click.option('--filename', required=True, type=str, help='File to save habits')
def save_habits(filename):
    """Save habits to a specified file."""
    manager.save_habits(filename)
    click.echo(f'Habits saved to {filename}')

@cli.command()
@click.option('--filename', required=True, type=str, help='File to load habits from')
def load_habits(filename):
    """Load habits from a specified file."""
    manager.load_habits(filename)
    click.echo(f'Habits loaded from {filename}')

if __name__ == '__main__':
    cli()
