import pandas as pd
from sqlalchemy import create_engine, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.sqlite import insert

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String, primary_key=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_status: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[str] = mapped_column(String, nullable=False)


def load_data_to_sqlite(csv_path="parsed_data.csv", db_path="sqlite:///books.db"):
    engine = create_engine(db_path)

    Base.metadata.create_all(engine)

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_path} не найден")
        return

    records = df.to_dict(orient="records")
    print(f"Подготовка к загрузке {len(records)} записей в базу данных SQLite...")

    with Session(engine) as session:
        stmt = insert(Book).values(records)

        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=['title'],
            set_={
                'price': stmt.excluded.price,
                'stock_status': stmt.excluded.stock_status,
                'rating': stmt.excluded.rating
            }
        )

        session.execute(upsert_stmt)
        session.commit()

if __name__ == "__main__":
    load_data_to_sqlite()