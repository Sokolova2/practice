<h1 align="center">Hadware Store API</h1>

API додаток для автоматизації бізнесу у магазині техніки.

## 🚀Features

### 👩‍💼Касир
- Переглядає список продуктів:
    - назва, ціна та дата створення;
- Після отримання замовлення від клієнта додає його в базу даних;
- Генерує рахунок:
    - назва, ціна та дата створення рахунку та створення замовлення;
- Приймає оплату від клієнта і змінює статус замовлення на "Сплачено";
### 🧑‍💻Продавець-консультант
- Переглядає це замовлення та змінює його статус на "Виконано"; 
### 👨‍💼Бухгалтер 
- У будь-який час переглядає замовлення з фільтрацією за датами: 
    - номер замовлення, назва продукту, статус, ціна, знижка, дата створення та оновлення замовлення;
###  ⚙️Система 
- Має механізм нарахування знижок для товарів, у яких дата стоврення більше одного місяця від поточної дати знижка 20%.

## 🛠 Tech Stack

* API: FastAPI
* Database: PostgreSQL
* Orm for database: Sqlalchemy

## 🚀 Installation & Setup

Клонуємо репозиторій та створюємо віртуальне середовище

```
git clone git@github.com:Sokolova2/practice.git 
python3 -m venv vevn
```

Запускаємо віртуальне середовище

for Windows 
```
venv\Scripts\activate
```

for Linux 
```
venv/bin/activate
```

Встановлюємо залежності
```
pip install -r requirements.txt
```

Перед запуском додатку треба зробити .env у якому будуть дані про базу та JWT_TOKEN
Обов`язково треба створити базу даних в pg admin 
Або у терміналі прописати 
psql -h localhost -U postgres -d your_database_name

.env

```
DB_HOST=localhost
DB_USER=username
DB_PASS=password
DB_PORT=port
DB_NAME=hardwarestore

JWT_SECRET = "my-secret-key"
JWT_ACCESS_COOKIE_NAME = "access_token"
```

Після того, як завантажено віртуальне середовище, усі залежності встановлені та створений .env з вашими даними, запускаємо додаток.

```
uvicorn src.main:app --reload
```

## ✅ Testing

Щоб протестувати застосунок, потрібно d pg admin створити нову базу даних test_db. Далі потрібно виконати такі команди

```
python -m pytest .\src\tests\test_accountant.py -s
python -m pytest .\src\tests\test_auth.py -s
python -m pytest .\src\tests\test_order.py -s
python -m pytest .\src\tests\test_product.py -s
python -m pytest .\src\tests\test_sales_consultant.py -s
```