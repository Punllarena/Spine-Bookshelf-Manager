from sqlalchemy import Integer, String, Float, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from flask_sqlalchemy import SQLAlchemy



class Base(DeclarativeBase):
    """
    Base class for declarative class definitions.

    To use this class, subclass it and add mapped columns with the
    ``mapped_column`` function.

    The class must have a ``__tablename__`` attribute with the name of a
    database table. The class must also have at least one mapped column
    with a primary key.

    See the SQLAlchemy documentation for more information on how to use
    this class.
    """
    pass
# db is defined here instead of main.py because it needs to be imported in models.py
# so that the declarative models can be defined. This is a common pattern in
# Flask applications.
db = SQLAlchemy(model_class=Base)

class Book(Base):
    """
    Model for a book.

    This model represents a book in the database. A book has a title, an
    author, a publisher, a series ID, and a series index. The series ID
    and series index are optional.

    Attributes:

        id (int): The ID of the book. This is a unique identifier for the
            book and is used to reference the book in other tables.

        title (str): The title of the book. This is a required field and
            must be unique.

        author (str): The author of the book. This is an optional field.

        publisher (str): The publisher of the book. This is an optional
            field.

        seriesID (str): The ID of the series the book belongs to. This is
            an optional field.

        seriesIndex (int): The index of the book in the series. This is an
            optional field.

    """
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(250))
    author: Mapped[str] = mapped_column(String(250), nullable=True)
    publisher: Mapped[str] = mapped_column(String(250), nullable=True)
    series_id: Mapped[str] = mapped_column(String(50), nullable=True)
    series_index: Mapped[int] = mapped_column(Integer, nullable=True)
    reading_tag: Mapped[str] = mapped_column(String(50), nullable=True) 
    # isSeries: Mapped[bool] = mapped_column(Boolean, nullable=True)
    release_date: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    # ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    g_volume_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    start_date: Mapped[str] = mapped_column(String(10), nullable=True)
    finish_date: Mapped[str] = mapped_column(String(10), nullable=True)
    hour_read: Mapped[int] = mapped_column(Integer, nullable=True)
    minutes_read: Mapped[int] = mapped_column(Integer, nullable=True)
    
