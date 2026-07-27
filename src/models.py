from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
        }


class People(db.Model):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20))
    height: Mapped[Optional[str]] = mapped_column(String(20))
    eye_color: Mapped[Optional[str]] = mapped_column(String(50))

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color
        }


class Planet(db.Model):
    __tablename__ = 'planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(50))
    terrain: Mapped[Optional[str]] = mapped_column(String(50))
    population: Mapped[Optional[int]] = mapped_column(BigInteger)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    people_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('planet.id'), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped[Optional["People"]] = relationship(
        back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(
        back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,

            "people": self.people.serialize() if self.people else None,
            "planet": self.planet.serialize() if self.planet else None
        }
