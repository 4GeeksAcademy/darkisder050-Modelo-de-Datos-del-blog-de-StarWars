from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    favorite_people: Mapped[List["FavoritePeople"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    favorite_planets: Mapped[List["FavoritePlanet"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class People(db.Model):
    __tablename__ = 'people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20))
    height: Mapped[Optional[str]] = mapped_column(String(20))
    eye_color: Mapped[Optional[str]] = mapped_column(String(50))

    favorites: Mapped[List["FavoritePeople"]] = relationship(back_populates="people", cascade="all, delete-orphan")


class Planet(db.Model):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(50))
    terrain: Mapped[Optional[str]] = mapped_column(String(50))
    population: Mapped[Optional[int]] = mapped_column(BigInteger)

    favorites: Mapped[List["FavoritePlanet"]] = relationship(back_populates="planet", cascade="all, delete-orphan")


class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=False)

    
    user: Mapped["User"] = relationship(back_populates="favorite_people")
    people: Mapped["People"] = relationship(back_populates="favorites")


class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=False)

    
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
