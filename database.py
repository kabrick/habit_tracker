import sqlite3
import pendulum


class Database:

    def __init__(self, db_name="habits.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.create_database()


    def save_habit(self, title, period):
        """
        Save habit to database
        :param title:
        :param period:
        :return: Void
        """
        self.open_conn()
        self.cursor.execute("INSERT INTO habits (title, period) VALUES (?, ?)", (title, period))
        self.close_conn()


    def edit_habit(self, habit_id, title, period):
        """
        Update habit title and period
        :param habit_id:
        :param title:
        :param period:
        :return: Void
        """
        self.open_conn()
        self.cursor.execute(
            "UPDATE habits SET title = ?, period = ? WHERE habit_id = ?",
            (title, period, habit_id)
        )
        self.close_conn()


    def fetch_habit(self, habit_id):
        """
        Fetch single habit from db by id
        :param habit_id:
        :return: Habit database row
        """
        self.open_conn()
        row = self.cursor.execute(
            "SELECT * FROM habits WHERE habit_id = ?",
            (habit_id,)
        ).fetchall()
        self.close_conn()

        return row


    def fetch_all_habits(self):
        """
        Fetch all habits from database
        :return: Dictionary with habit ids as keys and habit title and period as value
        """
        self.open_conn()
        rows = self.cursor.execute("SELECT * FROM habits").fetchall()
        self.close_conn()

        return_dict = {}

        for row in rows:
            return_dict[row[0]] = row[1] + " (" + row[2] + ")"

        return return_dict


    def fetch_habit_longest_streak(self, habit_id):
        """
        Fetch the longest streak for a habit
        :param habit_id:
        :return: Longest streak as numeric value
        """
        self.open_conn()
        rows = self.cursor.execute("SELECT * FROM habit_tasks WHERE habit_id = ?",
                                   (habit_id,)).fetchall()
        self.close_conn()

        longest_streak = 0
        current_streak = 0
        last_date = None
        habit_period = self.fetch_habit(habit_id)[0][2]

        for row in rows:
            if last_date is not None:
                last_date_obj = pendulum.parse(last_date)
                now_date_obj = pendulum.parse(row[2])

                diff_obj = now_date_obj - last_date_obj

                if habit_period == "Daily":
                    diff = diff_obj.days
                elif habit_period == "Weekly":
                    diff = diff_obj.weeks
                elif habit_period == "Monthly":
                    diff = diff_obj.months
                elif habit_period == "Yearly":
                    diff = diff_obj.years
                else:
                    return

                if diff == 0:
                    current_streak += 1

                    if current_streak > longest_streak:
                        longest_streak = current_streak
                else:
                    current_streak = 1
            else:
                longest_streak = 1
                current_streak = 1

            last_date = row[2]

        return longest_streak


    def fetch_habits_by_period(self, period):
        """
        Fetch habits from database according to a period
        :param period:
        :return: Dictionary with habit ids as keys and habit title and period as value
        """
        self.open_conn()
        rows = self.cursor.execute(
            "SELECT * FROM habits WHERE period = ?",
            (period,),
        ).fetchall()
        self.close_conn()

        return_dict = {}

        for row in rows:
            return_dict[row[0]] = row[1] + " (" + row[2] + ")"

        return return_dict


    def delete_habit(self, habit_id):
        """
        Delete habit from database according to id
        :param habit_id:
        :return: Void
        """
        self.open_conn()
        self.cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
        self.close_conn()


    def save_habit_task(self, habit_id):
        """
        Save completed habit task
        :param habit_id:
        :return: Void
        """
        self.open_conn()
        self.cursor.execute("INSERT INTO habit_tasks (habit_id) VALUES (?)", (habit_id,))
        self.close_conn()


    def open_conn(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()


    def close_conn(self):
        self.connection.commit()
        self.connection.close()


    def create_database(self):
        """
        Create database with initial data for testing
        :return: Void
        """
        self.open_conn()

        table_exists = self.cursor.execute("PRAGMA table_info(habits)").fetchall()

        if table_exists:
            return


        self.cursor.execute("""
        CREATE TABLE habits (
          habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          period TEXT NOT NULL,
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE habit_tasks (
          task_id INTEGER PRIMARY KEY AUTOINCREMENT,
          habit_id INTEGER NOT NULL,
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
        )
        """)

        self.cursor.execute("INSERT INTO habits (title, period) VALUES ('Drink Water', 'Daily')")
        self.cursor.execute("INSERT INTO habits (title, period) VALUES ('Write In Journal', 'Daily')")
        self.cursor.execute("INSERT INTO habits (title, period) VALUES ('Go Grocery Shopping', 'Weekly')")
        self.cursor.execute("INSERT INTO habits (title, period) VALUES ('Add Money To Saving Accounts', 'Monthly')")
        self.cursor.execute("INSERT INTO habits (title, period) VALUES ('Buy Christmas Gifts', 'Yearly')")

        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-01 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-12 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-13 08:11:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-14 08:10:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-17 08:09:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-22 08:14:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-23 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-24 08:11:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-25 08:10:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-26 08:09:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-27 08:08:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (1, '2024-08-29 08:07:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-01 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-09 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-10 08:11:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-11 08:10:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-12 08:09:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-13 08:08:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-14 08:07:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-17 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-20 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (2, '2024-08-24 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (4, '2024-06-23 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (4, '2024-07-22 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (4, '2024-08-21 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (5, '2023-12-23 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (5, '2022-12-24 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (3, '2024-07-23 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (3, '2024-07-26 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (3, '2024-07-30 08:12:32')")
        self.cursor.execute("INSERT INTO habit_tasks (habit_id, created_at) VALUES (3, '2024-08-02 08:12:32')")

        self.close_conn()
