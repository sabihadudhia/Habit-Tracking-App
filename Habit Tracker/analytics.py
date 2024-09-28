class Analytics:
    @staticmethod
    def list_all(habits):  # Returns a list of all habits
        print("Listing all habits.")
        return [habit.name for habit in habits]

    @staticmethod
    def list_habits_by_periodicity(habits, periodicity):  # Returns a list of habits for a certain period
        print(f"Listing habits by periodicity: {periodicity}.")
        filtered_habits = [habit for habit in habits if habit.periodicity == periodicity]
        print(f"Found habits: {', '.join(habit.name for habit in filtered_habits)}")
        return filtered_habits

    @staticmethod
    def get_longest_streak(habits):  # Returns the habit with the longest streak currently
        max_streak = 0
        habit_name = None
        for habit in habits:
            streak = habit.get_streak()
            print(f'Checking habit "{habit.name}" with streak: {streak}')
            if streak > max_streak:
                max_streak = streak
                habit_name = habit.name
        print(f'Longest streak found: "{habit_name}" with {max_streak} periods.')
        return habit_name, max_streak
