from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

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
