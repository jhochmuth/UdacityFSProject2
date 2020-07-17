import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
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

    formatted_questions = [question.format() for question in questions[start:end]]
    
    if len(formatted_questions) == 0:
        abort(404)

    categories = Category.query.all()
    formatted_categories = dict()
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(questions),
      'categories': formatted_categories
    })

  @app.route('/questions', methods=['POST'])
  def search_questions():
    try:
      search_term = request.get_json()['searchTerm']
    except:
      abort(400)
    
    query = Question.query.filter(Question.question.contains(search_term)).all()
    formatted_questions = [question.format() for question in query]

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions)
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    print(question)

    if question is None:
      abort(404)

    question.delete()
    db.session.commit()
    return jsonify({'success': True})

  @app.route('/add', methods=['POST'])
  def create_question():
    try:
      data = request.get_json()
      question = Question(question=data['question'],
                          answer=data['answer'],
                          difficulty=data['difficulty'],
                          category=data['category'])
      db.session.add(question)
      db.session.commit()
    except:
      abort(400)

    return jsonify({'success': True})

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    query = Question.query.filter_by(category=category_id).all()
    
    if len(query) == 0:
      abort(404)
    
    formatted_questions = [question.format() for question in query]

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': category_id
    })

  @app.route('/quizzes', methods=['POST'])
  def quiz():
    print(request.get_json())
    try:
      category_id = request.get_json()['quiz_category']['id']
      previous_questions = request.get_json()['previous_questions']
    except:
      abort(400)

    if category_id == 0:
      question = Question.query.filter(~Question.id.in_(previous_questions)).first()
      if question is None:
        abort(404)
    else:
      question = Question.query.filter_by(category=category_id).filter(~Question.id.in_(previous_questions)).first()

    if question:
      question = question.format()

    return jsonify({'success': True, 'question': question})

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Bad request."
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Page not found."
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable entity."
    }), 422

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': "Internal server error."
    }), 500

  return app
