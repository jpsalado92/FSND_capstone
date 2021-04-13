# import os
# SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
# basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database
SQLALCHEMY_DATABASE_URI = \
    'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(user="postgres",
                                                                    password="1234",
                                                                    host="localhost",
                                                                    port=5432,
                                                                    db_name="movie_casting")

