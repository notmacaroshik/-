Q1 = '''
CREATE TABLE if not EXISTS quiz(
	id INTEGER PRIMARY key, 
    name TEXT
)
'''
Q2 = '''
    CREATE TABLE if not EXISTS questions(
	id INTEGER PRIMARY key, 
    question TEXT,
  	right_ans TEXT,
  	wrong_ans TEXT,
  	score INTEGER
)
'''
Q3 = '''
    CREATE TABLE if not EXISTS quiz_content(
	id INTEGER PRIMARY key, 
  	quiz_id INTEGER,
    question_id INTEGER,
  	FOREIGN key (question_id) REFERENCES questions (id),
  	FOREIGN key (quiz_id) REFERENCES quiz (id)
)
'''
NEXT_QUESTION_ID = """
SELECT quiz_content.id, 
       questions.question, questions.right_ans, questions.wrong_ans, questions.score
    FROM questions, quiz_content
    WHERE quiz_content.question_id == questions.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id"""

CHEK_RIGHTS = '''SELECT quiz_content.id, questions.question, questions.right_ans
    FROM questions, quiz_content
    WHERE quiz_content.id = ? AND (questions.right_ans LIKE ?)'''

GET_FIRST = '''SELECT question_id
    FROM quiz_content
    WHERE quiz_id = ?
    ORDER BY question_id
    LIMIT 1'''

COUNT_QS = '''SELECT COUNT(*)
FROM quiz_content
WHERE quiz_id = ?'''

TABLES = ['quiz', 'questions', 'quiz_content']

SELECT = 'SELECT * FROM '

DROP = 'DROP TABLE IF EXISTS '

INSERT = 'INSERT INTO '

QUIZ1 = [('Смешарики'),('Щенячий патруль')]
QUIZ2 = [('Какие цвета есть в радуге?', 'Красный, оранжевый, жёлтый, зелёный, салатовый, голубой, синий, фиолетовый, розовый', 'Оранжевый, жёлтый, зелёный, салатовый, голубой, синий, фиолетовый, розовый~Серый, черный, белый~RGB',1),
         ('Какой человек никода не сможет намочить волосы под дождем?', 'Лысый','С длинными волосами~С зонтиком~С дождевиком',1),
         ('Что означает ДНК?','Дезоксирибонуклеиновая кислота','Дон Кихот~Дерзкий но красивый~Деньги на кофе',1),
         ('Сколько зубов у взрослого человека?','32','30~34~28',1),
         ('Какой месяц самый короткий','май','август~февраль~январь',1),
         ('Сколько костей в теле человека?','206','204~208~202',1)]
QUIZ3 = [
    (1,1),
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (1,6),
    (2,1),
    (2,2),
    (2,3),
    (2,4),
    (2,5),
    (2,6),
]
COL1 = '(name)'
COL2 = '(question,right_ans,wrong_ans,score)'
COL3 = '(quiz_id, question_id)'
PRAGMA = "PRAGMA foreign_keys=on"