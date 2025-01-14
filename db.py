import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('Database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM daily_params WHERE user_id = {user_id}").fetchall()
            return len(result) != 0

    def get_location_by_chat_id(self, id):
        with self.connection:
            result = self.cursor.execute(f"SELECT latitude, longitude FROM user WHERE chat_id = {id}").fetchall()
            return result[0]

    def set_location_by_chat_id(self, id, latitude, longitude):
        with self.connection:
            query = "UPDATE user SET latitude = ?, longitude = ? WHERE chat_id = ?"
            self.cursor.execute(query, (latitude, longitude, id))

    def add_user(self, name, chat_id):
        if self.user_exists(chat_id):
            return
        with self.connection:
            query = "INSERT INTO user (name, chat_id) VALUES (?, ?)"
            self.cursor.execute(query, (name, chat_id))
            query = f"INSERT INTO daily_params (user_id) VALUES ({chat_id})"
            self.cursor.execute(query)
            query = f"INSERT INTO period_params (user_id) VALUES ({chat_id})"
            self.cursor.execute(query)

    def get_daily_params_by_user(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM daily_params WHERE user_id = {user_id}").fetchall()
            return result[0][1:]

    def update_daily_parameters(self, user_id, params : list[int]):
        with self.connection:
            query = f"UPDATE daily_params SET temperature=?, apparent_temperature=?, sunrise_sunset=?, uv_index=?, precipitation_sum=?, precipitation_probability=?, wind_speed=? WHERE user_id={user_id}"
            self.cursor.execute(query, tuple(params))

    def get_period_params_by_user(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM period_params WHERE user_id = {user_id}").fetchall()
            return result[0][1:]

    def update_period_parameters(self, user_id, params : list[int]):
        with self.connection:
            query = f"UPDATE period_params SET temperature=?, apparent_temperature=?, precipitation=?, precipitation_probability=?, pressure_msl=?, visibility=?, wind=? WHERE user_id={user_id}"
            self.cursor.execute(query, tuple(params))
