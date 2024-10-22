from mysql import connector


class DataBase:
    def __init__(self, db_host: str, db_database: str, db_user: str, db_password: str):
        self.__connection = connector.connect(host=db_host, database=db_database, user=db_user, password=db_password)
        self.__verify_connection()

    def __del__(self):
        self.__connection.close()

    def consult(self, query: str):
        cursor = self.__connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert(self, query: str):
        cursor = self.__connection.cursor()
        cursor.execute(query)
        self.__connection.commit()
        cursor.close()

    def __verify_connection(self):
        if not self.__connection.is_connected():
            raise Exception("Failed to connect to the database.")
