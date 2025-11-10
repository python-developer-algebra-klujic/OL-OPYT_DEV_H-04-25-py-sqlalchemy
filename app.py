from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, or_, and_

# 1. KORAK - Pripremiti strukturu baze i tablice

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
        return f"ID: {self.id} | Author: {self.first_name} {self.last_name}"


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
        return f"ID: {self.id} | Book: {self.title}"


# 2. KORAK - Kreiranje konekcije na s bazom pomocu objekta 'engine'
# engine je slicno kao i connection u sqlite3 modulu
engine = create_engine("sqlite:///library.db")

# 3. KORAK - Kreiranje baze i tablica na osnovu klasa koje naslijeduju Base klasu
Base.metadata.create_all(engine)


# 4. KORAK - Rad s podacima
# Za to koristimo Session klasu, odnosno session objekt te klase.
# session je slicno cusrosru u sqlite3 modulu
try:
    with Session(engine) as session:
        # C - CREATE - dodaj podatke u bazu
        # Dodan mehanizam zastite dodavanja duplih podataka!!!
        tolkien = Author(first_name="J.R.R.", last_name="Tolkien")

        the_hobit = Book(title="The Hobit", author=tolkien)
        the_fellowship_of_the_ring = Book(title="The Fellowship of the Ring", author=tolkien)

        author_from_db = session.query(Author).filter(
            and_(Author.first_name == tolkien.first_name,
                 Author.last_name == tolkien.last_name,)
        ).first()
        if author_from_db == None:
            session.add(tolkien)    # kao da smo napravili cursor.execute()
            session.commit()        # pohrani promjene u bazu
        else:
            print(f"Autor {tolkien.first_name} {tolkien.last_name} vec postoji u bazi")


        # R - READ - dohvati podatke iz baze
        # authors = session.query(Author).all()
        # for author in authors:
        #     print(author)

        # author = session.query(Author).filter_by(id=3).first()
        # print(author)

        # author = session.query(Author).filter_by(last_name="Mihajlovic Dostojevski").first()
        # print(author)

        # author = session.query(Author).filter(Author.last_name.like("Tol%")).first()
        # print(author)


        # books = session.query(Book).all()
        # for book in books:
        #     print(book)

        #       JOIN EKSPLICITNI - vracanje podataka iz obje baze
        # resut = session.query(Book).join(Author).all()
        # for book in resut:
        #     print(book, " | ", book.author)

        #       JOIN IMPLICITNI - vracanje podataka iz obje baze
        # resut = session.query(Book).all()
        # for book in resut:
        #     print(book, " | ", book.author)


        # U - UPDATE - azuriraj podatke iz baze
        # ili oznaci kao izbrisan u slucaju ako se koristi Soft Delete
        # author_from_db = session.query(Author).filter_by(id=4).first()
        # if author_from_db:
        #     author_from_db.first_name = "Jules"
        #     author_from_db.last_name = "Verne"
        #     session.commit()
        # else:
        #     print(f"Ne postoji trazeni autor u bazi!")

        # D - DELETE - izbrisi objek iz base
        # books_from_db = session.query(Book).filter(or_(Book.id==7, Book.id==8)).all()
        # if len(books_from_db) > 0:
        #     for book in books_from_db:
        #         session.delete(book)

        # author_from_db = session.query(Author).filter_by(id=4).first()
        # if author_from_db:
        #     session.delete(author_from_db)
        #     session.commit()
        # else:
        #     print(f"Ne postoji trazeni autor u bazi!")



except Exception as ex:
    print(f"Dogodila se greska {ex}.")
