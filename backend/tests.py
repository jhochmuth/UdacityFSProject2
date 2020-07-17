import unittest
from flaskr import create_app
from models import setup_db
import json


class TriviaTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = "postgresql://postgres:password@localhost:5432/trivia"

  def tearDown(self):
    pass

  def test_get_categories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(len(data['categories']))

  def test_get_questions(self):
    res = self.client().get('/questions?page=1')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(len(data['questions']))
  
  def test_get_questions_fail(self):
    res = self.client().get('/questions?page=100')
    self.assertEqual(res.status_code, 404)

  def test_search_questions(self):
    res = self.client().post('/questions', json={'searchTerm': 'the'})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(len(data['questions']))
  
  def test_search_questions_fail(self):
    res = self.client().post('/questions')
  
    self.assertEqual(res.status_code, 400)

  def test_create_question(self):
    question_data = {'question': '???', 'answer': 'No', 'difficulty': 1, 'category': 1}
    res = self.client().post('/add', json=question_data)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)

  def test_create_question_fail(self):
    question_data = {'question': '???', 'answer': 'No'}
    res = self.client().post('/add', json=question_data)

    self.assertEqual(res.status_code, 400)
  
  def test_delete_question(self):
    res = self.client().delete('/questions/1')

    self.assertEqual(res.status_code, 200)

  def test_delete_question_fail(self):
    res = self.client().delete('/questions/100000')

    self.assertEqual(res.status_code, 404)
  
  def test_get_questions_by_category(self):
    res = self.client().get('/categories/1/questions')
    data = json.loads(res.data)
    
    self.assertEqual(res.status_code, 200)
    self.assertTrue(len(data['questions']))

  def test_get_questions_by_category_fail(self):
    res = self.client().get('/categories/100/questions')

    self.assertEqual(res.status_code, 404)

  def test_quiz(self):
    req = {'quiz_category': {'id': 0}, 'previous_questions': []}
    res = self.client().post('/quizzes', json=req)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['question']['question'])
    self.assertTrue(data['question']['answer'])

  def test_quiz_fail(self):
    res = self.client().post('/quizzes', json={'previous_questions': []})

    self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
  unittest.main()
