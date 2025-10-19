from flask import Flask, url_for, redirect, session
import os

def index():
    """ функция перенаправляет на URL, соответствующий файлу index.html"""
    session["counter"] = 0

    return '<a href = "/counter">дальше</a>'
def counter():
    session["counter"] += 1
    return f'<h1>{session ["counter"]}</h1>'

folder = os.getcwd() # запомнили текущую рабочую папку


# Создаём объект веб-приложения:
app = Flask(__name__, static_folder=folder) # первый параметр - имя модуля для веб-приложения, 
                        # параметр с именем static_folder определяет имя папки, содержащей статичные файлы 
app.config['SECRET_KEY'] = 'VeryStrongKey'
# создаём правило для URL '/': 
app.add_url_rule('/', 'index', index)
app.add_url_rule('/counter', 'counter', counter)


if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()
