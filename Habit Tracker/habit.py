from datetime import datetime, timedelta, date

class Habit:
    def __init__(self, name, periodicity, start_date):
        self.name = name
        self.periodicity = periodicity  # 'daily' or 'weekly'
        self.start_date = start_date
        self.completion_dates = []  # Store task completion dates
        self.streak = 0  # Current streak count
        self.history = []  # List to store completion history

    def is_broken(self):
        """Checks if the habit was broken since the last completion date."""
        if not self.history:
            return False  # No completions yet, habit can't be broken

        last_completion = self.history[-1]  # Get last completed date
        current_date = datetime.now().date()  # Today's date

        if self.periodicity == 'daily':
            return (current_date - last_completion).days > 1
        elif self.periodicity == 'weekly':
            return (current_date - last_completion).days > 7
        return False  # In case of invalid periodicity

    def get_streak(self):
        """Returns the current streak."""
        return self.streak

    def update_streak(self):
        """Updates the streak count based on the completion dates."""
        if not self.history:
            self.streak = 0
            return

        # Sort history to ensure chronological order
        self.history.sort()

        consecutive_streak = 1  # Start with 1 for the first completion

        for i in range(1, len(self.history)):
            days_diff = (self.history[i] - self.history[i - 1]).days

            if self.periodicity == 'daily' and days_diff == 1:
                consecutive_streak += 1
            elif self.periodicity == 'weekly' and 0 < days_diff <= 7:
                consecutive_streak += 1
            else:
                # Streak is broken, reset the streak counting
                break

        self.streak = consecutive_streak


    def complete_task(self, completion_date=None):
        """
        Marks the task as completed. If no date is provided, it defaults to the current date.
        :param completion_date: Optional, the date the task was completed.
        """
        if completion_date is None:
            completion_date = date.today()  # Default to today's date

        self.completion_dates.append(completion_date)
        self.history.append(completion_date)  # Add to history for streak tracking
        self.update_streak()  # Update the streak

    def convert_dictionary(self):
        """Converts the habit instance to a dictionary for JSON storage."""
        return {
            'name': self.name,
            'periodicity': self.periodicity,
            'start_date': self.start_date.isoformat(),
            'completion_dates': [date.isoformat() for date in self.completion_dates],
            'streak': self.streak,
            'history': [date.isoformat() for date in self.history],
        }
