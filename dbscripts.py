from queries import *
from contextlib import contextmanager
import sqlite3
class DB:
    def __init__(self, db_name = 'quiz.db',table_name = 'quiz', columns = COL1):
        self.db_name = db_name
        self.table_name = table_name
        self.columns = columns
    def set_table(self,table_name = 'quiz', columns = COL1):
        self.table_name = table_name
        self.columns = columns
    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для управления соединением."""
        conn = sqlite3.connect(self.db_name)
        # тип а-ля словарь
        #conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    def create_table(self, query=Q1):
        query = query.replace('--','')
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(PRAGMA)
            cursor.execute(query)
            conn.commit()
    def drop_table(self,table):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DROP+table)
            conn.commit()
    #INSERT INTO demo (Name, Hint) VALUES ('ГТА','Прохождение')
    def insert(self,table, columns, data):
        s = len(columns.split(',')) * '?, '
        if type(data) == str:
            data = [data]
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT+table + f' {columns} VALUES ({s[:-2]})', data)
            conn.commit()
    def select(self,table, query = SELECT):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query+table)
            conn.commit()
            return cursor.fetchall()
    def execute(self,query, data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return cursor.fetchall()
def setup_base(db):
    for table in TABLES:
        db.drop_table(table)
    db.create_table(Q1)
    db.create_table(Q2)
    db.create_table(Q3)
    for quiz in QUIZ1:
        db.insert('quiz',COL1, quiz)
    for questions in QUIZ2:
        db.insert('questions',COL2, questions)
    for quiz_content in QUIZ3:
        db.insert('quiz_content',COL3, quiz_content)
    res = db.select('quiz')
    res = db.select('questions')
    
if __name__ == "__main__":
    db = DB()
    for table in TABLES:
        db.drop_table(table)
    db.create_table(Q1)
    db.create_table(Q2)
    db.create_table(Q3)
    for quiz in QUIZ1:
        db.insert('quiz',COL1, quiz)
    for questions in QUIZ2:
        db.insert('questions',COL2, questions)
    for quiz_content in QUIZ3:
        db.insert('quiz_content',COL3, quiz_content)
    res = db.select('quiz')
    res = db.select('questions')
    res = db.execute(NEXT_QUESTION_ID, (1,1))
    res = db.execute(CHEK_RIGHTS, ('1'))
    print(res)