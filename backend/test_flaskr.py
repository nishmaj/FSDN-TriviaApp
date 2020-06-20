import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}@{}/{}".format('nishmajain','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['categories'])

    def test_retrieve_questions_pagination(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))


    def test_retrieve_questions_fail(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        #self.assertTrue(data[message], 'Questions not found')    

    def test_delete_questions(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 10)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(question, None)


    def test_delete_questions_fail(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 10000)

        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Question object data missing from request")


    def test_post_new_questions(self):
        post_data = {
            'question':'What is the capital of India?',
            'answer': 'Delhi',
            'difficulty': 2,
            'category': 1
        }
        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)    


    def test_post_new_questions_fail(self):
        post_data = {
            'question':'What is the capital of India?',
            'difficulty': 2,
            'category': 1
        }
        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Question data missing from request')


    def test_post_search_questions(self):
        post_data = {
            'searchTerm': 'a'
        }
        res = self.client().post('/searchQuestions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))


    def test_post_search_questions_fail(self):
        post_data = {
            'searchTerm1': '',
        }
        res = self.client().post('/searchQuestions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], 'Search data missing from request')


    def test_get_questions_with_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['category'])
  

    def test_get_questions_with_category_fail(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Category not found')


    def test_post_play_quiz(self):
        post_data = {
            'previous_questions':[],
            'quiz_category' : {
                'type': 'Science',
                'id': 1
            }
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    def test_post_play_quiz_fail(self):
        post_data = {
            'previous_questions':[]
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Required quiz keys missing from request body')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()