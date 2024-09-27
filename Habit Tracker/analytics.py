class Analytics:
    @staticmethod
    def list_all(habits): # Returns a list of all habits
        return [habit.name for habit in habits]

    @staticmethod 
    def list_habits_by_periodicity(habits, periodicity): # Returns a list of habits for a certain period
        return [habit for habit in habits if habit.periodicity == periodicity]

    @staticmethod
    def get_longest_streak(habits): # Returns the habit with the longest streak currently
        max_streak = 0
        for habit in habits:
            streak = habit.get_streak()
            if streak > max_streak:
                max_streak = streak
        return max_streak
