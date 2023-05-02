import sqlite3

class BotDB:

    def __init__(self, db_file):
        """"Инициализация соединения с БД"""
        self.connect = sqlite3.connect('list.db', check_same_thread = False)
        self.cursor = self.connect.cursor()


    def add_record(self, name, link, mark):
        """Создаем запись о расходе/доходе"""
        self.cursor.execute("INSERT INTO 'literature'('names', 'link', 'mark') VALUES (?, ?, ?)",
                            (name,
                             link,
                             mark))
        return self.connect.commit()


    def get_records(self):
        result = self.cursor.execute("SELECT * FROM literature WHERE mark = (SELECT MAX(mark) FROM literature) LIMIT 4")
        result = self.cursor.fetchall()
        return result

    #
    # def close(self):
    #      """Закрытие соединения с БД"""
    #      self.connect.close()