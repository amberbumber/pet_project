from flask import Blueprint

# конструктор blueprint пакета errors

# если добавить аргумент template_folder= 'templates' в конструктор Blueprint(),
# можно сохранить шаблоны схемы элементов в app/errors/templates.

bp = Blueprint('errors', __name__)

from app.errors import handlers