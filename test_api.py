import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from api import app
from models import setup_db, Movie, Actor, db_drop_and_create_all


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        self.assistant_header = os.environ['AS_HEAD']
        self.director_header = os.environ['DR_HEAD']
        self.producer_header = os.environ['PR_HEAD']
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Tests
    """

    def test_get_actors(self):
        '''
        test get /actors
        '''
        res = self.client().get(
            '/actors', headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        '''
        test get /movies
        '''
        res = self.client().get(
            '/movies', headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))
    ##

    def test_post_actor_unauth(self):
        '''
        test post /actors without correct permission
        '''
        res = self.client().post(
            '/actors', json={
                "name": "A", "age": 1, "gender": "m"
            }, headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 401)

    def test_post_movie_unauth(self):
        '''
        test post /movies without correct permission
        '''
        res = self.client().post(
            '/movies', json={
                "title": "A", "release": "2000-01-01"
            }, headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 401)

    def test_post_actor(self):
        '''
        test post /actors with correct permission
        '''
        res = self.client().post(
            '/actors', json={
                "name": "A", "age": 1, "gender": "m"
            }, headers={"Authorization": self.producer_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)

    def test_post_movie(self):
        '''
        test post /movies with correct permission
        '''
        res = self.client().post(
            '/movies', json={
                "title": "A", "release": "2000-01-01"
            }, headers={"Authorization": self.producer_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)

    ##

    def test_patch_actor_unauth(self):
        '''
        test patch /actors/2 without correct permission
        '''
        res = self.client().patch(
            '/actors/2', json={
                "name": "A", "age": 2, "gender": "m"
            }, headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 401)

    def test_patch_movie_unauth(self):
        '''
        test patch /movies/2 without correct permission
        '''
        res = self.client().patch(
            '/movies/2', json={
                "title": "A", "release": "2000-02-01"
            }, headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 401)

    def test_patch_actor(self):
        '''
        test patch /actors/2 with correct permission
        '''
        res = self.client().patch(
            '/actors/2', json={
                "name": "B", "age": 2, "gender": "m"
            }, headers={"Authorization": self.producer_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)

    def test_patch_movie(self):
        '''
        test patch /movies/2 with correct permission
        '''
        res = self.client().patch(
            '/movies/2', json={
                "title": "B", "release": "2000-02-01"
            }, headers={"Authorization": self.producer_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)

    ##
    def test_delete_actor_unauth(self):
        '''
        test delete /actors/1 without correct permission
        '''
        res = self.client().delete(
            '/actors/1', headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 401)

    def test_delete_movie_unauth(self):
        '''
        test delete /movies/1 without correct permission
        '''
        res = self.client().delete(
            '/movies/1', headers={"Authorization": self.assistant_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 401)

    def test_delete_actor(self):
        '''
        test delete /actors/1 with correct permission
        '''
        res = self.client().delete(
            '/actors/1', headers={"Authorization": self.producer_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)

    def test_delete_movie(self):
        '''
        test delete /actors with correct permission
        '''
        res = self.client().delete(
            '/movies/1', headers={"Authorization": self.producer_header})
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
