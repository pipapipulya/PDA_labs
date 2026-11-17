import pandas as pd
from sqlalchemy import create_engine, text

def run_analytics(db_path="sqlite:///books.db"):
    engine = create_engine(db_path)

    print("--АНАЛИТИКА ПО ДАННЫМ ИЗ SQLITE--")

    with engine.connect() as conn:
        # запрос 1 общая стата (количество, средняя, мин и макс цена)
        query1 = text("""
            SELECT 
                COUNT(title) as total_books,
                ROUND(AVG(price), 2) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price
            FROM books;
        """)
        df1 = pd.read_sql_query(query1, conn)
        print("\n1. Общая статистика по ценам на книги:")
        print(df1.to_string(index=False))

        # запрос 2 распределение книг по рейтингу
        query2 = text("""
            SELECT 
                rating,
                COUNT(title) as books_count,
                ROUND(AVG(price), 2) as avg_price
            FROM books
            GROUP BY rating
            ORDER BY books_count DESC;
        """)
        df2 = pd.read_sql_query(query2, conn)
        print("\n2. Статистика книг в зависимости от их рейтинга (звезд):")
        print(df2.to_string(index=False))

        # запрос 3 топ-5 самых дорогих книг с высшим рейтингом
        query3 = text("""
            SELECT title, price, rating
            FROM books
            WHERE rating = 'Five'
            ORDER BY price DESC
            LIMIT 5;
        """)
        df3 = pd.read_sql_query(query3, conn)
        print("\n3. Топ-5 самых дорогих книг с рейтингом 5 звезд:")
        print(df3.to_string(index=False))

        # запрос 4 анализ наличия (stock_status)
        query4 = text("""
            SELECT 
                stock_status,
                COUNT(title) as count_status,
                ROUND(AVG(price), 2) as avg_price
            FROM books
            GROUP BY stock_status;
        """)
        df4 = pd.read_sql_query(query4, conn)
        print("\n4. Статистика по наличию книг на складе:")
        print(df4.to_string(index=False))

        # запрос 5 поиск потенциально недооцененных книг
        # 4 или 5 звезд, но цена ниже средней по всей базе
        query5 = text("""
            SELECT title, price, rating
            FROM books
            WHERE rating IN ('Four', 'Five') 
              AND price < (SELECT AVG(price) FROM books)
            ORDER BY price ASC
            LIMIT 5;
        """)
        df5 = pd.read_sql_query(query5, conn)
        print("\n5. Топ-5 самых дешевых книг с высоким рейтингом (выгодные покупки):")
        print(df5.to_string(index=False))


if __name__ == "__main__":
    run_analytics()