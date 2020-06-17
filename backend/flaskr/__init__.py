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

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def retrieve_categories():
      
      categories = list(map(Category.format, Category.query.all()))

      result = {
          'success': True,
          'categories': categories
      }

      return jsonify(result)

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
      # Create a new list
      # Map the elements from Category.format with the values provided by Category.query.all
      # Return the jsonify
      questions = list(map(Question.format, Question.query.all()))
      
      result = {
          'success': True,
          'questions': questions
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
      
      return jsonify({
        'success': True
      })
      
      # question_query = Question.query.get(question_id)
      
      # if question_query:
      #   Question.delete(question_query)

      # else:
      #   error(404)  

      

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

    return jsonify({
        'success': True
    })

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
    return jsonify({
      'success': True
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_with_category(category_id):
    category_query = Category.query.get(category_id)

    question_query = Question.query.filter_by(category=str(category_id)).all()
    
    questions = list(map(Question.format, question_query))

    return jsonify({
      'success': True,
      'questions': questions
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
    return jsonify({
      'success': True
    })

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

    