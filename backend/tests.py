import unittest
from flaskr import create_app
from models import db, Question
import json


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

class TriviaTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = 'postgresql://{}:{}@localhost:5432/trivia'.format(DB_USER, DB_PASS)

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
    table_size = len(Question.query.all())
    
    question_data = {'question': '???', 'answer': 'No', 'difficulty': 1, 'category': 1}
    res = self.client().post('/add', json=question_data)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
  
    new_table_size = len(Question.query.all())
    self.assertEqual(new_table_size, table_size + 1)

  def test_create_question_fail(self):
    question_data = {'question': '???', 'answer': 'No'}
    res = self.client().post('/add', json=question_data)

    self.assertEqual(res.status_code, 400)
  
  def test_delete_question(self):
    question = Question(question="blah", answer="blah", difficulty=1, category=1)
    db.session.add(question)
    db.session.commit()
  
    id = question.id
    table_size = len(Question.query.all())
    
    res = self.client().delete('/questions/{}'.format(id))

    self.assertEqual(res.status_code, 200)
    
    new_table_size = len(Question.query.all())
    self.assertEqual(table_size - 1, new_table_size)

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
