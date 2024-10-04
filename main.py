import questionary
import constants
from Habit import Habit
from database import Database
from analytics import analytics


def initial_screen():
    """
    Show main screen options for user to interact with the app
    :return:
    """
    selected_option = questionary.select("Welcome to your habit tracker app. What would you like to do?",
                                choices=constants.MAIN_MENU).ask()

    if selected_option == constants.MAIN_OPTION_ONE:
        add_habit()
    elif selected_option == constants.MAIN_OPTION_TWO:
        manage_habits()
    elif selected_option == constants.MAIN_OPTION_THREE:
        analytics()
        initial_screen()
    else:
        print("Thank you for using my habits tracker")


def add_habit():
    """
    Prompt user to enter new habit details and save to the database
    :return:
    """
    answers = questionary.form(
        title=questionary.text("Enter habit title"),
        period=questionary.select("Choose habit period", choices=constants.PERIODS)
    ).ask()

    habit = Habit(answers.get('title'), answers.get('period'))
    habit.save_habit()

    print("Habit has been saved")

    initial_screen()


def manage_habits():
    """
    Menu to manage a habit through prompting user input for editing, deletion or completing habit
    :return:
    """
    database = Database()
    habits = database.fetch_all_habits()

    if not habits:
        print("Please add a habit to track")
    else:
        selected_habit = questionary.select("Choose habit from list",
                                             choices=habits.values()).ask()

        habit_key = list(habits.keys())[list(habits.values()).index(selected_habit)]

        selected_habit_option = questionary.select(selected_habit, choices=constants.MANAGE_HABIT_MENU).ask()

        if selected_habit_option == constants.EDIT_OPTION:
            edit_habit(habit_key, selected_habit)
        elif selected_habit_option == constants.DELETE_OPTION:
            delete_habit(habit_key, selected_habit)
        elif selected_habit_option == constants.CHECK_OPTION:
            complete_habit(habit_key)

    initial_screen()


def edit_habit(habit_id, habit_title):
    """
    Prompt user to enter new details for already existing habit
    :param habit_id:
    :param habit_title:
    :return:
    """
    answers = questionary.form(
        title=questionary.text("Enter habit title - " + habit_title),
        period=questionary.select("Choose habit period - " + habit_title, choices=constants.PERIODS)
    ).ask()

    habit = Habit(answers.get('title'), answers.get('period'))
    habit.edit_habit(habit_id)


def delete_habit(habit_id, habit_title):
    """
    Delete habit from the database
    :param habit_id:
    :param habit_title:
    :return:
    """
    answer = questionary.confirm("Are you sure you want to delete " + habit_title + "?").ask()

    if answer:
        habit = Habit()
        habit.delete_habit(habit_id)


def complete_habit(habit_id):
    """
    Mark a habit as complete for the registered period
    :param habit_id:
    :return:
    """
    database = Database()
    database.save_habit_task(habit_id)

    print("Task has checked off")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initial_screen()
