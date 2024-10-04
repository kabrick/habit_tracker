import unittest

import constants
from Habit import Habit


class MyTestCase(unittest.TestCase):


    def test_habit_creation(self):
        habit = Habit('Test Title', constants.PERIODS[0], 'test.db')
        habit.save_habit()

        # fetch habits to check if inserted
        habits = habit.fetch_all_habits()

        self.assertEqual('Test Title (' + constants.PERIODS[0] + ')' , habits[len(habits)])


    def test_habit_editing(self):
        habit = Habit(db='test.db')
        habit.fetch_habit(1)

        previous_title = habit.title
        habit.title = 'Edited Title'
        habit.edit_habit(1)

        new_habit = Habit(db='test.db')
        new_habit.fetch_habit(1)

        self.assertNotEqual(previous_title, new_habit.title)
        self.assertEqual('Edited Title', new_habit.title)


    def test_habit_deletion(self):
        habit = Habit(db='test.db')
        all_habits_count = len(habit.fetch_all_habits())

        habit.delete_habit(2)

        current_habits_count = len(habit.fetch_all_habits())

        self.assertNotEqual(all_habits_count, current_habits_count)
        self.assertLess(current_habits_count, all_habits_count)


if __name__ == '__main__':
    unittest.main()
