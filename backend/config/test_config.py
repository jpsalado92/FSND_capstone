# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database
SQLALCHEMY_DATABASE_URI = \
    'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(user="postgres",
                                                                    password="1234",
                                                                    host="localhost",
                                                                    port=5432,
                                                                    db_name="movie_casting_test")
