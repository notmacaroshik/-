from dbscripts import DB, setup_base
from queries import *
""" Программа использует flask и запускает веб-сервер. 
При запросе к этому серверу он возвращает содержимое файла index.html """
from flask import Flask, url_for, redirect, render_template, request, session
import os
from random import shuffle

def start_quiz(quiz_id):
    session['quiz_id'] = quiz_id
    session['last_question'] = 1
    session['answer'] = 0
    session['total'] = 0
def question_form(question):
    # question - строчка из базы данных, кортеж
    print(question)
    q_id = question[0]
    text = question[1]
    right = question[2]
    wrongs = question[3].split('~')
    wrongs.append(right)
    shuffle(wrongs)
    print(wrongs)
    return render_template('test.html', q_id = q_id, question = text, answers=wrongs)

def save_answers():
    answer = request.form.get('ans_text')
    q_id = request.form.get('q_id')
    print(db.execute(CHEK_RIGHTS, (q_id)))
    print(q_id)
    right_ans = db.execute(CHEK_RIGHTS, (q_id))[0][0]
    if right_ans == answer:
        session['total'] += 1
    session['last_question'] += 1
def end_quiz():
    session.clear()

def index():
    if request.method == 'GET':
        quizes = db.select(TABLES[0])
        """ функция перенаправляет на URL, соответствующий файлу index.html"""
        return render_template('index.html', quizes = quizes)
    else:
        quiz_id = request.form.get('викторина')
        print(quiz_id)
        start_quiz(quiz_id)
        questoin = db.execute(NEXT_QUESTION_ID, (quiz_id, 1))
        return redirect(url_for('test'))
            
def test():
    if request.method == 'POST':
        save_answers()
    next_question = db.execute(NEXT_QUESTION_ID, (session['quiz_id'],session['last_question']))
    print(next_question)
    if next_question is None or len(next_question) == 0:
        return redirect(url_for('test'))
    else:
        return question_form(next_question[0])
def result():
        return render_template('result.html', result = session['total'])
        # url_for с первым параметром 'static' создаёт URL для статичного файла
        # redirect возвращает объект, который при вызове перенаправляет клиента на указанный адрес
        # (адрес для перенаправления указывается параметром функции redirect)

folder = os.getcwd() # запомнили текущую рабочую папку
db = DB()
setup_base(db)

# Создаём объект веб-приложения:
app = Flask(__name__, static_folder=folder,template_folder=folder ) # первый параметр - имя модуля для веб-приложения, 
                        # параметр с именем static_folder определяет имя папки, содержащей статичные файлы 
app.config['SECRET_KEY']='privet'
# создаём правило для URL '/': 
app.add_url_rule('/', 'index', index, methods=['get', 'post'])
app.add_url_rule('/test', 'test', test, methods=['get', 'post'])
app.add_url_rule('/result', 'result', result, methods=['get', 'post'])

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()
