# Full Stack API Project

## Full Stack Trivia

Full Stack Trivia API Project
This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for it.

Frontend Dependencies
This project uses NPM to manage software dependencies. 

npm install


Backend Dependencies

Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

PIP Dependencies

pip3 install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

Key Dependencies
Flask is a lightweight backend micro-services framework. Flask is required to handle requests and responses.
SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.


Database Setup 
Install and setup "PostgreSQL" on the system and create a database named trivia in the Postgres server.

createdb trivia

With Postgres running, populate the database using the trivia.psql file provided. 

psql trivia < trivia.psql



Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

npm start
Running the Server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

export FLASK_APP=flaskr
export flask run --reload

The backend is hosted at http://127.0.0.1:5000/


Testing
To run the flask tests, run this command:

python -m unittest discover -t ../


API Reference

Endpoints
GET /categories
Returns a list of categories.

  {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "success": True
  }



GET /questions
Returns a list of questions.
Results are paginated in groups of 10.
Also returns list of categories and total number of questions.
Sample: curl http://127.0.0.1:5000/questions

  {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "questions": [
          {
              "answer": "Colorado, New Mexico, Arizona, Utah", 
              "category": 3, 
              "difficulty": 3, 
              "id": 164, 
              "question": "Which four states make up the 4 Corners region of the US?"
          }, 
          {
              "answer": "Muhammad Ali", 
              "category": 4, 
              "difficulty": 1, 
              "id": 9, 
              "question": "What boxer's original name is Cassius Clay?"
          }, 
      ], 
      "success": True, 
      "total_questions": 19
  }


DELETE /questions/<int:id>
Deletes a question by id using url parameters.
Returns id of deleted question upon success.
  {
      "success": True,
      "deleted": 6
  }


POST /questions
This endpoint either creates a new question

Creates a new question using JSON request parameters.
Returns JSON object with newly created question.

  {
    'success': True,    
    "question": {
        "id": 1,
        "question": "",
        "answer": "",
        "category": 1,
        "difficulty": 1
    }
}


POST /searchQuestions
This endpoint fetches the questions based on the search term

{
  "success": True  
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }],
  "total_questions": 1
}

GET /categories/<int:id>/questions
Create a GET endpoint to get questions based on category.
Returns JSON object with matching questions.

  {
      "success": True,
      "current_category": "Science", 
      "questions": [
          {
              "answer": "The Liver", 
              "category": 1, 
              "difficulty": 4, 
              "id": 20, 
              "question": "What is the heaviest organ in the human body?"
          }, 
          {
              "answer": "Alexander Fleming", 
              "category": 1, 
              "difficulty": 3, 
              "id": 21, 
              "question": "Who discovered penicillin?"
          }, 
          {
              "answer": "Blood", 
              "category": 1, 
              "difficulty": 4, 
              "id": 22, 
              "question": "Hematology is a branch of medicine involving the study of what?"
          }
      ]
  }


POST /quizzes
Allows users to play the quiz game.
Uses JSON request parameters of category and previous questions.
Returns JSON object with random question not among previous questions.

  {
      "success": True,
      "question": {
          "answer": "Blood", 
          "category": 1, 
          "difficulty": 4, 
          "id": 22, 
          "question": "Hematology is a branch of medicine involving the study of what?"
      }
  }