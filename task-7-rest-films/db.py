from sqlalchemy import create_engine, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = "postgresql+psycopg2://users_rate_films:thebesticancomeupwith@postgres:5432/filmsAPI"
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, unique=True, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    registration_date = Column("registration_date", Date, nullable=False)

    def __init__(self, username, email, registration_date):
        self.username = username
        self.email = email
        self.registration_date = registration_date

    def toJSON(self):
        return {
            "User": {
                "username": self.username,
                "email": self.email,
                "registration_date": self.registration_date,
            }
        }


class Movie(Base):
    __tablename__ = "movies"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, unique=True, nullable=False)
    year = Column("year", Integer, nullable=False)
    country = Column("country", String, nullable=False)

    def __init__(self, name, year, country):
        self.name = name
        self.year = year
        self.country = country

    def toJSON(self):
        return {
            "Movie": {"name": self.name, "year": self.year, "country": self.country}
        }


class Rating(Base):
    __tablename__ = "ratings"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column("movie_id", Integer, ForeignKey("movies.id"), nullable=False)
    value = Column("value", Float, nullable=False)

    def __init__(self, user_id, movie_id, value):
        self.user_id = user_id
        self.movie_id = movie_id
        self.value = value

    def toJSON(self):
        return {
            "Rating": {
                "user_id": self.user_id,
                "movie_id": self.movie_id,
                "value": self.value,
            }
        }


engine = create_engine(url)
Session = sessionmaker(bind=engine)


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
