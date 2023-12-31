# Благотворительный фонд поддержки кошек :coin:

## Используемые технологии
- :snake: Python 3.8.10
- :incoming_envelope: FastAPI 0.78.0
- :busts_in_silhouette: FastAPI-Users 10.0.4
- :recycle: Pydantic 1.9.1
- :package: SQLAlchemy 1.4.36
- :notebook: aiosqlite 0.17.0
- :memo: Alembic 1.7.7

## Описание проекта
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

**Проекты**

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других;
когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

**Пожертвования**

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект.
Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму.
Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта.
При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

**Пользователи**

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы.
Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

<details>
<summary>Подробнее о проекте:</summary>
<p>

### Процесс инвестирования

Сразу после создания нового проекта или пожертвования запускается процесс **«инвестирования»** (увеличение ``invested_amount`` как в пожертвованиях, так и в проектах, установка значений ``fully_invested`` и ``close_date``, при необходимости).

Если создан новый проект, а в базе были **«свободные»** (не распределённые по проектам) суммы пожертвований — они автоматически инвестируются в новый проект, и в ответе API эти суммы учитываются. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования автоматически зачисляются на их счета.

Функция, отвечающая за инвестирование, вызывается непосредственно из API-функций, отвечающих за создание пожертвований и проектов. Сама функция инвестирования расположена в директории ``app/services/`` в файле ``invest.py``.

</p>
</details>

## Запуск проекта
1. Клонировать репозиторий:
```bash
git clone git@github.com:Kaydalova/cat_charity_fund.git
```

2. Создать и активировать виртуальное окружение:
```bash
python3 -m venv venv

. venv/bin/activate

```

3. Обновить pip и установить зависимости из ```requirements.txt```
```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Создать и заполнить файл **.env** (пример заполнения в файле .env.example) :

```bash
touch .env
```

5. Выполнить миграции:
```bash
alembic upgrade head
```

6. Запустить проект:
```bash
uvicorn app.main:app --reload 
```

После запуска проект будет доступен по адресу: http://127.0.0.1:8000

Документация к API досупна по адресам:
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc


**Автор проекта:** [Александра Кайдалова](https://github.com/Kaydalova)
