from database import Database


class Habit:

    def __init__(self, title=None, period=None, db=None):
        self.title = title
        self.period = period

        if db is None:
            self.db_conn = Database()
        else:
            self.db_conn = Database(db)


    def save_habit(self):
        """
        Save habit with defined title and period

        :return: Void
        """
        self.db_conn.save_habit(self.title, self.period)


    def edit_habit(self, habit_id):
        """
        Edit habit with title and period
        :param habit_id:
        :return: Void
        """
        self.db_conn.edit_habit(habit_id, self.title, self.period)


    def fetch_habit(self, habit_id):
        """
        Fetch habit according to habit id
        :param habit_id:
        :return: Void
        """
        retrieved_habit = self.db_conn.fetch_habit(habit_id)
        self.period = retrieved_habit[0][2]
        self.title = retrieved_habit[0][1]


    def fetch_all_habits(self):
        """
        Fetch all habit from db
        :return: Habits dictionary
        """
        return self.db_conn.fetch_all_habits()


    def fetch_habits_by_period(self, period):
        """
        Fetch all habit from db by period
        :return: Habits dictionary
        """
        return self.db_conn.fetch_habits_by_period(period)


    def delete_habit(self, habit_id):
        """
        Delete habit by id
        :param habit_id:
        :return: Void
        """
        self.db_conn.delete_habit(habit_id)