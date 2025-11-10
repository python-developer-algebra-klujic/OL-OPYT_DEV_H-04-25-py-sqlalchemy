from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

# 1. KORAK - Pripremiti bazu, tablice i konekciju na bazu

# Base klasa je klasa koju svaki model mora naslijediti
# i zahvaljujuci toj klasi, SQL Alchemy 'zna' koja klasa predstavlja koju tablicu u bazi
# te dodatno koje tablice treba kreirati u bazi i s kojim kolonama
Base = declarative_base()

# Umjesto da koristimo SQL za kreiranje tablice, te zasebnu Python klasu za model,
# ovdje koristimo jednu klasu koja je model i opis tablice u jednom
class Author(Base):
    __tablename__ = "author"    # definira naziv tablice u bazi

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=150), nullable=False, default="John")
    last_name = Column(String(length=150), nullable=False, default="Doe")
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"Author: {self.first_name} {self.last_name}"


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=250), nullable=False)
    description = Column(String(length=1500), nullable=True)
    year = Column(Integer, nullable=True)

    # Foreign Key koji gleda na stupac 'id' u tablici 'author'.
    # Vazno je da obje kolone imaju isti tip podatka u ovom slucaju Integer
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"Book: {self.title}"


































the_hobit = Book('The Hobit')
the_hobit.title
the_hobit.author

tolkien = Author(last_name="Tolkine", first_name="J.R.R.")
tolkien.books
