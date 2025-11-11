import mysql.connector
import os
import time

def get_db_connection():
    """Функція для підключення до БД з кількома спробами."""
    conn = None
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
            if conn.is_connected():
                print("Успішно підключено до бази даних.")
                return conn
        except mysql.connector.Error as e:
            print(f"Помилка підключення до MySQL: {e}")
            retries -= 1
            print(f"Повторна спроба підключення... Залишилось спроб: {retries}")
            time.sleep(5) # Чекаємо 5 секунд перед наступною спробою
    return None

def main():
    """Головна функція застосунку."""
    print("Застосунок на Python запускається...")
    conn = get_db_connection()

    if not conn:
        print("Не вдалося встановити з'єднання з базою даних. Завершення роботи.")
        return

    cursor = conn.cursor()

    try:
        # Створюємо таблицю
        table_name = "users"
        print(f"Створення таблиці '{table_name}', якщо вона не існує.")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255)
            )
        """)
        print("Перевірка/створення таблиці завершено.")

        # Додаємо кілька записів, лише якщо таблиця порожня
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        if cursor.fetchone()[0] == 0:
            print("Додавання записів...")
            insert_query = f"INSERT INTO {table_name} (name, email) VALUES (%s, %s)"
            users_to_add = [
                ("Ivan Franko", "franko@example.com"),
                ("Taras Shevchenko", "shevchenko@example.com")
            ]
            cursor.executemany(insert_query, users_to_add)
            conn.commit() # Зберігаємо зміни
            print(f"Було додано {cursor.rowcount} записів.")
        else:
            print("Записи вже існують, пропуск додавання.")

        # Показуємо повний вміст таблиці
        print(f"\n--- Повний вміст таблиці '{table_name}' ---")
        cursor.execute(f"SELECT id, name, email FROM {table_name}")
        rows = cursor.fetchall()

        if not rows:
            print("Таблиця порожня.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Ім'я: {row[1]}, Email: {row[2]}")
        print("-----------------------------------------\n")

    except mysql.connector.Error as e:
        print(f"Сталася помилка: {e}")
    finally:
        # Закриваємо з'єднання
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("З'єднання з базою даних закрито.")

if __name__ == "__main__":
    main()