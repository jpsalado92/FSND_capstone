import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
db = SQLAlchemy()


def setup_db(app):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    db.app = app
    Migrate(app, db)
    db.init_app(app)


def calculate_current_age(dob):
    """
    Calculates the age of anything given a reference date.
    :param dob: Date of birth
    :return: Current age
    """
    today = datetime.date.today()
    years = today.year - dob.year
    if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
        years -= 1
    return years


class Actor(db.Model):
    """
    Actor
    a persistent actor entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'actors'

    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    birth_date = Column(DateTime(), nullable=False)
    gender = Column(String(120), nullable=False)
    filmography = relationship("Appearance", backref=db.backref("actors", lazy=True),
                               cascade="all,delete-orphan")

    def describe(self):
        """
        describe()
            representation of the Movie model
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': calculate_current_age(self.birth_date),
            'gender': self.gender,
            'filmography': [appearance.movies.title for appearance in
                            Appearance.query.filter(Appearance.actor_id == self.id).all()]
        }

    def insert(self):
        """
        insert()
            inserts a new model into the database
            the model must have a unique id or null id
            EXAMPLE
                actor = Actor(name=req_name, birth_date=req_birth_date, gender=req_gender)
                actor.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes an existing model from the database
            EXAMPLE
                actor = Actor.query.get(id)
                actor.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates an existing model from the database
            EXAMPLE
                actor = Actor.query.get(id)
                actor.name = 'Leonardo DiCaprio'
                actor.update()
        """
        db.session.commit()


class Movie(db.Model):
    """
    Movie
    a persistent movie entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'movies'

    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(DateTime(), nullable=False)
    cast = relationship("Appearance", backref=db.backref("movies", lazy=True),
                        cascade="all,delete-orphan")

    def describe(self):
        """
        describe()
            representation of the Movie model
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': [appearance.actors.name for appearance in
                     Appearance.query.filter(Appearance.movie_id == self.id).all()]
        }

    def insert(self):
        """
        insert()
            inserts a new model into the database
            the model must have a unique id or null id
            EXAMPLE
                movie = Movie(title=req_title, release_date=req_release_date)
                movie.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes an existing model from the database
            EXAMPLE
                movie = Movie.query.get(id)
                movie.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates an existing model from the database
            EXAMPLE
                movie = Movie.query.get(id)
                movie.title = 'Sharknado'
                movie.update()
        """
        db.session.commit()


class Appearance(db.Model):
    __tablename__ = 'appearances'
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)

    def insert(self):
        """
        insert()
            inserts a new model into the database
            the model must have a unique id or null id
            EXAMPLE
                appearance = Appearance(actor_id=req_actor_id, movie_id=req_movie_id)
                appearance.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes an existing model from the database
        """
        db.session.delete(self)
        db.session.commit()

    def describe(self):
        """
        describe()
            representation of the Appearance model
        """
        return {
            'movie': {'id': self.movie_id, 'title': self.movies.title},
            'actor': {'id': self.actor_id, 'name': self.actors.name}
        }
