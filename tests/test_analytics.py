import unittest

from analytics import Analytics


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.analytics = Analytics('test.db')

    def test_show_all_habits(self):
        habits = self.analytics.show_all_habits()

        self.assertEqual(5, len(habits))

    def test_show_habits_by_period(self):
        daily_habits = self.analytics.show_habits_by_period("Daily")
        self.assertEqual(2, len(daily_habits))

        weekly_habits = self.analytics.show_habits_by_period("Weekly")
        self.assertEqual(1, len(weekly_habits))

        monthly_habits = self.analytics.show_habits_by_period("Monthly")
        self.assertEqual(1, len(monthly_habits))

        yearly_habits = self.analytics.show_habits_by_period("Yearly")
        self.assertEqual(1, len(yearly_habits))

    def test_show_habit_longest_streak(self):
        streak_list = self.analytics.show_habit_longest_streak("Drink Water (Daily)")

        self.assertEqual(6, streak_list[1])

    def test_show_all_longest_streaks(self):
        streak_list = self.analytics.show_all_longest_streaks()

        self.assertEqual("Drink Water (Daily) has a longest streak of 6", streak_list[0])


if __name__ == '__main__':
    unittest.main()
