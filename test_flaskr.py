#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import unittest
from flaskr.database.models import setup_db, Movie, Actor, \
    create_and_drop_all
from flaskr import create_app
from flask_sqlalchemy import SQLAlchemy

DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')

TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')


class CastingAgencyTestCase(unittest.TestCase):

    """This class represultents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, TEST_DATABASE_URI)

        self.executive_producer_token = PRODUCER_TOKEN
        self.casting_assistant_token = ASSISTANT_TOKEN
        self.casting_director_token = DIRECTOR_TOKEN

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables

            create_and_drop_all()

            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

        pass

    def test_get_movies(self):
        result = self.client().get('/movies',
                                headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)})
        data = json.loads(result.data)
        if result.status_code == 200:
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['movies']), 0)

    def test_get_movies_fail_401(self):
        result = self.client().get('/movies')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_movies(self):
        movie = {'title': 'Skyfall', 'release_date': '2015-03-02',
                 'genre': 'SuperHero'}

        result = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)},
                                 json=movie)
        data = json.loads(result.data)
        self.assertTrue(data['success'])
        movie_db = Movie.query.get(data['movie_id'])
        movie['id'] = data['movie_id']
        self.assertEqual(movie_db.get_formatted_json(), movie)

    def test_post_movies_fail_401(self):
        movie = {'title': 'Skyfall', 'release_date': '2015-03-02'}
        result = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)},
                                 json=movie)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 401)

    def test_post_movies_fail_400(self):
        movie = {'title': 'Skyfall', 'release_date': '2015-03-02'}
        result = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)},
                                 json=movie)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(400, result.status_code)
        self.assertNotEqual('Bad request',len(data['message']))

    def test_patch_movie(self):
        updated_movie = {'title': 'Skyfall 2',
                       'release_date': '2015-03-02'}
        movie = Movie.query.order_by(Movie.id).first()

        result = self.client().patch('/movies/' + str(movie.id),
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)},
                                  json=updated_movie)
        data = json.loads(result.data)
        self.assertEqual(200, result.status_code)
        self.assertTrue(data['success'])
        movie = Movie.query.get(data['movie']['id'])
        movie_formatted_json = movie.get_formatted_json()
        for key in updated_movie.keys():
            self.assertEqual(updated_movie[key], movie_formatted_json[key])

    def test_patch_movie_fail_404(self):
        movie = {'title': 'Skyfall', 'release_date': '2015-03-02'}
        result = self.client().patch('/movies/234523',
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)},
                                  json=movie)
        data = json.loads(result.data)
        self.assertEqual(404, result.status_code)
        self.assertFalse(data['success'])

    def test_patch_movie_fail_401(self):
        movie = {'title': 'Skyfall', 'release_date': '2015-03-02'}
        result = self.client().patch('/movies/345234',
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)},
                                  json=movie)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 401)

    def test_delete_movie(self):
        movie = Movie.query.order_by(Movie.id).first()
        result = self.client().delete('/movies/' + str(movie.id),
                                   headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(result.data)
        self.assertTrue(data['success'])
        movie = Movie.query.get(data['deleted'])
        self.assertEqual(movie, None)

    def test_delete_movie_fail_401(self):
        result = self.client().delete('/movies/2345234')
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 401)

    def test_delete_movie_fail_404(self):
        result = self.client().delete('/movies/23452345',
                                   headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(404, result.status_code)

    def test_get_actors(self):
        result = self.client().get('/actors',
                                headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)})
        data = json.loads(result.data)
        if result.status_code == 200:
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['actors']), 0)

    def test_get_actors_fail_401(self):
        result = self.client().get('/actors')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_actor(self):
        actor = {'name': 'Daniel Kraig', 'gender': 'male', 'age': 50}

        result = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)},
                                 json=actor)
        data = json.loads(result.data)
        self.assertTrue(data['success'])
        actor_db = Actor.query.get(data['actor_id'])
        actor['id'] = data['actor_id']
        self.assertEqual(actor, actor_db.get_formatted_json())

    def test_post_actors_fail_401(self):
        actor = {'name': 'Daniel Kraig', 'gender': 'male', 'age': 50}
        result = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)},
                                 json=actor)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 401)

    def test_post_actors_fail_400(self):
        actor = {'name': 'Daniel Kraig', 'gender': 'male'}
        result = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)},
                                 json=actor)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(400, result.status_code)
        self.assertNotEqual('Bad request',len(data['message']))

    def test_patch_actor(self):
        actor = {'name': 'Nina Dobrev', 'gender': 'female'}
        actor_db = Actor.query.order_by(Actor.id).first()
        result = self.client().patch('/actors/' + str(actor_db.id),
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)},
                                  json=actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        actor_db = Actor.query.get(data['actor']['id'])
        actor_json = actor_db.get_formatted_json()
        for key in actor.keys():
            self.assertEqual(actor[key], actor_json[key])

    def test_patch_actor_fail_404(self):
        actor = {'name': 'Nina Dobrev', 'gender': 'female'}
        result = self.client().patch('/actors/234234',
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)},
                                  json=actor)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(404, result.status_code)

    def test_patch_actor_fail_401(self):
        actor = {'name': 'Nina Dobrev', 'gender': 'female'}
        result = self.client().patch('/actors/435435',
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)},
                                  json=actor)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 401)

    def test_delete_actors(self):
        actor = Actor.query.order_by(Actor.id).first()
        result = self.client().delete('/actors/' + str(actor.id),
                                   headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(result.data)
        self.assertTrue(data['success'])
        actor = Actor.query.get(data['deleted'])
        self.assertEqual(actor, None)

    def test_delete_actor_fail_404(self):
        result = self.client().delete('/actors/24332',
                                   headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(404, result.status_code)

    def test_delete_actor_fail_401(self):
        result = self.client().delete('/actors/99239')
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 401)


if __name__ == '__main__':
    unittest.main()
