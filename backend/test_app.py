import configparser
import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Actor, Appearance, Movie

config = configparser.ConfigParser()
config_file = "secrets.cfg"
config.read(config_file)


class UnauthorizedTestCase(unittest.TestCase):
    """This class represents the Unauthorized test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test_config')
        self.client = self.app.test_client
        self.new_actor = {'name': 'TestActor', 'gender': 'Male', 'birth_date': '2000-01-01'}
        self.patched_actor = {'name': 'TestPatchedActor'}
        self.new_movie = {'title': 'TestMovie', 'release_date': '2000-01-01'}
        self.patched_movie = {'title': 'TestPatchedMovie'}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    # UN-AUTHORIZED ACTOR TESTS
    def test_unauthorized_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_unauthorized_post_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_unauthorized_patch_actor(self):
        res = self.client().patch('/actors/1',
                                  json=self.patched_actor)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_unauthorized_delete_actor(self):
        res = self.client().delete(f'/actors/1')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    # UN-AUTHORIZED MOVIE TESTS
    def test_unauthorized_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_unauthorized_post_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_unauthorized_patch_movie(self):
        res = self.client().patch('/movies/1',
                                  json=self.patched_movie)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_unauthorized_delete_movie(self):
        res = self.client().delete(f'/movies/1')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    # UN-AUTHORIZED APPEARANCES TESTS
    def test_unauthorized_post_appearance(self):
        res = self.client().post('/appearances', json={'actor_id': 1, 'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def test_authorized_delete_appearance(self):
        res = self.client().delete('/appearances', json={'actor_id': 1, 'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header was not found.')

    def tearDown(self):
        """Executed after all tests"""
        [appearance.delete() for appearance in Appearance.query.all()]
        [movie.delete() for movie in Movie.query.all()]
        [actor.delete() for actor in Actor.query.all()]


class ExecutiveProducerTestCase(unittest.TestCase):
    """This class represents the ExecutiveProducer test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test_config')
        self.client = self.app.test_client
        self.new_actor = {'name': 'TestActor', 'gender': 'Male', 'birth_date': '2000-01-01'}
        self.patched_actor = {'name': 'TestPatchedActor'}
        self.new_movie = {'title': 'TestMovie', 'release_date': '2000-01-01'}
        self.patched_movie = {'title': 'TestPatchedMovie'}
        self.auth_token = ' '.join(('Bearer', config['JWT']['EXECUTIVE_PRODUCER_JWT']))
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    # AUTHORIZED ACTOR TESTS
    def test_authorized_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']) >= 0, True)

    def test_authorized_post_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['new_actor']['name'], 'TestActor')

    def test_authorized_patch_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.patched_actor,
                                  headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['patched_actor']['name'], 'TestPatchedActor')

    def test_authorized_delete_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        res = self.client().delete(f'/actors/{actor_id}',
                                   headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], str(actor_id))

    # AUTHORIZED MOVIE TESTS
    def test_authorized_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']) >= 0, True)

    def test_authorized_post_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['new_movie']['title'], 'TestMovie')

    def test_authorized_patch_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        movie_id = data['new_movie']['id']

        res = self.client().patch(f'/movies/{movie_id}',
                                  json=self.patched_movie,
                                  headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['patched_movie']['title'], 'TestPatchedMovie')

    def test_authorized_delete_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        movie_id = data['new_movie']['id']

        res = self.client().delete(f'/movies/{movie_id}',
                                   headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], str(movie_id))

    # AUTHORIZED APPEARANCES TESTS
    def test_authorized_post_appearance(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        movie_id = data['new_movie']['id']

        res = self.client().post('/appearances',
                                 json={'actor_id': actor_id, 'movie_id': movie_id},
                                 headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['new_appearance']['movie']['id'], movie_id)
        self.assertEqual(data['new_appearance']['movie']['title'], 'TestMovie')
        self.assertEqual(data['new_appearance']['actor']['id'], actor_id)
        self.assertEqual(data['new_appearance']['actor']['name'], 'TestActor')

    def test_authorized_delete_appearance(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        movie_id = data['new_movie']['id']

        res = self.client().post('/appearances',
                                 json={'actor_id': actor_id, 'movie_id': movie_id},
                                 headers={'Authorization': self.auth_token})

        res = self.client().delete('/appearances',
                                   json={'actor_id': actor_id, 'movie_id': movie_id},
                                   headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['delete']['actor_id'], actor_id)
        self.assertEqual(data['delete']['movie_id'], movie_id)

    def tearDown(self):
        """Executed after all tests"""
        [appearance.delete() for appearance in Appearance.query.all()]
        [movie.delete() for movie in Movie.query.all()]
        [actor.delete() for actor in Actor.query.all()]


class CastingDirectorTestCase(unittest.TestCase):
    """This class represents the CastingDirector test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test_config')
        self.client = self.app.test_client
        self.new_actor = {'name': 'TestActor', 'gender': 'Male', 'birth_date': '2000-01-01'}
        self.patched_actor = {'name': 'TestPatchedActor'}
        self.new_movie = {'title': 'TestMovie', 'release_date': '2000-01-01'}
        self.patched_movie = {'title': 'TestPatchedMovie'}
        self.auth_token = ' '.join(('Bearer', config['JWT']['CASTING_DIRECTOR_JWT']))
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    # AUTHORIZED ACTOR TESTS
    def test_authorized_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']) >= 0, True)

    def test_authorized_post_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['new_actor']['name'], 'TestActor')

    def test_authorized_patch_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.patched_actor,
                                  headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['patched_actor']['name'], 'TestPatchedActor')

    def test_authorized_delete_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        res = self.client().delete(f'/actors/{actor_id}',
                                   headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], str(actor_id))

    # AUTHORIZED MOVIE TESTS
    def test_authorized_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']) >= 0, True)

    # UN-AUTHORIZED MOVIE TESTS
    def test_unauthorized_post_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_unauthorized_patch_movie(self):
        res = self.client().patch(f'/movies/1',
                                  json=self.patched_movie,
                                  headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_unauthorized_delete_movie(self):
        res = self.client().delete(f'/movies/1',
                                   headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # AUTHORIZED APPEARANCES TESTS
    def test_authorized_post_appearance(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': self.auth_token})
        data = json.loads(res.data)
        actor_id = data['new_actor']['id']

        Movie(title=self.new_movie['title'], release_date=self.new_movie['release_date']).insert()
        movie_id = Movie.query.first().id

        res = self.client().post('/appearances',
                                 json={'actor_id': actor_id, 'movie_id': movie_id},
                                 headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['new_appearance']['movie']['id'], movie_id)
        self.assertEqual(data['new_appearance']['movie']['title'], 'TestMovie')
        self.assertEqual(data['new_appearance']['actor']['id'], actor_id)
        self.assertEqual(data['new_appearance']['actor']['name'], 'TestActor')

    # UN-AUTHORIZED APPEARANCES TESTS
    def test_unauthorized_delete_appearance(self):
        res = self.client().delete('/appearances',
                                   json={'actor_id': 1, 'movie_id': 1},
                                   headers={'Authorization': self.auth_token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def tearDown(self):
        """Executed after all tests"""
        [appearance.delete() for appearance in Appearance.query.all()]
        [movie.delete() for movie in Movie.query.all()]
        [actor.delete() for actor in Actor.query.all()]


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
