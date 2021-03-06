import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r'/*': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def set_headers(response):
      
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods',
                            'GET, PATCH, POST, DELETE, OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories' , methods=['GET'])
  def retrieve_categories():
    # Create a list of categories
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    if len(formatted_categories):
      return jsonify({
          'success': True,
          'categories': formatted_categories,
      })
    else:
      return jsonify({
          'success': False,
          'message': 'Categories not found'
      })  
      

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def retrieve_questions():
    # Create a list of questions using pagination
    page = request.args.get('page', 1, type=int)
    upper_limit = page*QUESTIONS_PER_PAGE
    lower_limit = upper_limit - QUESTIONS_PER_PAGE

    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    print(len(questions))

    if len(formatted_questions[lower_limit :upper_limit]) == 0:
      return abort(400, 'Questions not found')

    result = {
        'success': True,
        'questions': formatted_questions[lower_limit :upper_limit],
        'total_questions': len(formatted_questions),
        'categories': formatted_categories,
        'current_category': None
    }

    return jsonify(result)


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>' , methods=['DELETE'] )
  def delete_question(question_id):
    # Delete a question of given id
      
    question_query = Question.query.get(question_id)
      
    if question_query:
      Question.delete(question_query)
      result = {
        'success': True,
        'deleted': question_id  
      }
    else:
      return abort(400, 'Question object data missing from request')
      
    return jsonify(result)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=["POST"])
  def add_question():
    # Adds a new question n the db
    if request.data:
      body = request.get_json()
      question = body.get('question', None)
      answer = body.get('answer', None)
      category = body.get('category', None)
      difficulty = body.get('difficulty', None)

      if (question is None) or (answer is None) or (category is None) or (difficulty is None):
        return abort(400, 'Required question object data missing from request')

      try:
        new_question = Question(question, answer, category, difficulty)
        Question.insert(new_question)  
      
        return jsonify({
          'success': True,
          'question': new_question.format()
        })
      except:
        return abort(400, 'Question data missing from request')

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/searchQuestions', methods=['POST'])
  def search_questions():
    # Search thru questions using search criteria
    if request.data:
      body = request.get_json()
      searchTerm = body.get('searchTerm', None)
      
      if (searchTerm is None):
        return abort(400, 'Search data missing from request')

      try:
        questions = Question.query.filter(
                Question.question.ilike('%' + searchTerm + '%')).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': len(formatted_questions)
        })
      except:
        return abort(400, 'Search data missing from request')

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_with_category(category_id):

    # Gets a question basesd on a category
    category_query = Category.query.get(category_id)

    question_query = Question.query.filter_by(category=str(category_id)).all()
    questions = list(map(Question.format, question_query))

    if len(questions) > 0:
      return jsonify({
          'success': True,
          'questions': questions,
          'category': Category.format(category_query),
      })
    else:
      return jsonify({
          "success": False,
          "message": "Category not found"
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
  @app.route("/quizzes", methods=['POST'])
  def get_question_for_quiz():

    if request.data:

      previous_questions = request.json.get('previous_questions')
      quiz_category = request.json.get('quiz_category')

      if not quiz_category:
          return abort(400, 'Required quiz keys missing from request body')

      category_id = int(quiz_category.get('id'))

      # load questions all questions if "ALL" is selected
      if (category_id == 0):
          questions_q = Question.query.all()
      # load questions for given category
      else:

        questions_q = Question.query.filter_by(
                category=str(category_id)
            ).filter(
                Question.id.notin_(previous_questions)
            ).all()

      #print(questions_q)

      length_question = len(questions_q)
      if length_question > 0:
          result = {
              "success": True,
              "question": Question.format(
                  questions_q[random.randrange(
                      0,
                      length_question
                  )]
              )
          }
      else:
        result = {
            "success": False,
            "question": None
        }

      return jsonify(result)

    return abort(400, 'Quiz data missing from request')


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def not_found(error):
      error_data = {
          "success": False,
          "error": 400,
          "message": "Bad Request : {error}"
      }
      return jsonify(error_data)

  @app.errorhandler(404)
  def not_found(error):
      error_data = {
          "success": False,
          "error": 404,
          "message": "Resource not found : {error}"
      }
      return jsonify(error_data)

  @app.errorhandler(422)
  def unprocessable(error):
      error_data = {
          "success": False,
          "error": 422,
          "message": "Unprocessable : {error}"
      }
      return jsonify(error_data)

  @app.errorhandler(405)
  def method_not_allowed(error):
      error_data = {
          "success": False,
          "error": 405,
          "message": "The method is not allowed for the requested URL : {error}"
      }
      return jsonify(error_data)

  
  return app

    