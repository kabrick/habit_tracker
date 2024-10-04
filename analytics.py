import questionary
import constants
from database import Database

def analytics():
    selected_option = questionary.select("Analytics",
                                         choices=constants.ANALYTICS_MENU).ask()

    analytic = Analytics()

    if selected_option == constants.ANALYTICS_ALL_HABITS:
        habits = analytic.show_all_habits()

        if len(habits) > 0:
            print("You have " + str(len(habits)) + " habits in the system")
            analytic.display_rows(habits)
        else:
            print("Please add a habit to track")
    elif selected_option == constants.ANALYTICS_HABITS_BY_PERIOD:
        habits = analytic.show_habits_by_period()

        if len(habits) > 0:
            print("You have " + str(len(habits)) + " habits in the system")
            analytic.display_rows(habits)
        else:
            print("No habits found with specified period")
    elif selected_option == constants.ANALYTICS_LONGEST_RUN_ALL:
        habits = analytic.show_all_longest_streaks()

        if len(habits) > 0:
            analytic.display_rows(habits)
        else:
            print("No habits found with specified period")
    elif selected_option == constants.ANALYTICS_LONGEST_RUN_ONE:
        selected_habit, streak = analytic.show_habit_longest_streak()

        if selected_habit is not None:
            print(selected_habit + " has a longest streak of " + str(streak))

class Analytics:
    def __init__(self, db=None):
        if db is None:
            self.database = Database()
        else:
            self.database = Database(db)

    def display_rows(self, rows):
        """
        Print all rows in a list
        :param rows:
        :return: Void
        """
        for row in rows:
            print(row)

    def show_all_habits(self):
        """
        Fetch all habits from database
        :return: Empty list or list of habits by titles
        """
        habits = self.database.fetch_all_habits()

        if not habits:
            return []
        else:
            return habits.values()

    def show_habits_by_period(self, period=None):
        """
        Select period from list and fetch all habits from database which correspond to this period
        :param period:
        :return: Empty list or list of habits by titles
        """
        if period is None:
            period = questionary.select("Select Period", choices=constants.PERIODS).ask()

        habits = self.database.fetch_habits_by_period(period)

        if not habits:
            return []
        else:
            return habits.values()

    def show_habit_longest_streak(self, selected_habit=None):
        """
        Show the longest streak according to selected habit
        :param selected_habit:
        :return: Empty list or list with first value as selected habit and second value the streak
        """
        habits = self.database.fetch_all_habits()

        if not habits:
            return []
        else:
            if selected_habit is None:
                selected_habit = questionary.select("Choose habit", choices=habits.values()).ask()

            habit_key = list(habits.keys())[list(habits.values()).index(selected_habit)]
            streak = self.database.fetch_habit_longest_streak(habit_key)

            return [selected_habit, streak]

    def show_all_longest_streaks(self):
        """
        Show the longest streaks for each habit registered in the system
        :return: Empty list or list of streaks for all habits
        """
        habits = self.database.fetch_all_habits()

        if not habits:
            return []
        else:
            return_list = []
            for habit in habits.values():
                habit_key = list(habits.keys())[list(habits.values()).index(habit)]
                streak = self.database.fetch_habit_longest_streak(habit_key)
                return_list.append(habit + " has a longest streak of " + str(streak))

            return return_list