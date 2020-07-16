import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted = dict()
    for category in categories:
      formatted[category.id] = category.type

    return jsonify({'success': True, 'categories': formatted})

  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]

    categories = Category.query.all()
    formatted_categories = dict()
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': len(formatted_questions),
      'categories': formatted_categories
    })

  @app.route('/questions', methods=['POST'])
  def search_questions():
    search_term = request.get_json()['searchTerm']
    query = Question.query.filter(Question.question.contains(search_term)).all()
    formatted_questions = [question.format() for question in query]

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions)
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()
    return jsonify({'success': True})

  @app.route('/questions', methods=['POST'])
  def create_question():
    data = request.get_json()
    question = Question(question=data['question'],
                        answer=data['answer'],
                        difficulty=data['difficulty'],
                        category=data['category'])
    db.session.add(question)
    db.session.commit()
    return jsonify({'success': True})

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    query = Question.query.filter_by(category=category_id).all()
    formatted_questions = [question.format() for question in query]
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': category_id
    })

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

  return app
