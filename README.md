# Full Stack Udacity Project 2: Trivia

A basic trivia app. Project 2 in the Full Stack Udacity nanodegree.

## Usage
CD into the backend folder. Create a virtual environment and install the required backend dependencies by running ```$ pip install -r requirements.txt```. Restore a database with psql running by running ```$ psql trivia < trivia.psql```. You must set environment variables for DB_USER and DB_PASS. Then run these commands to run the server:

```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

In another terminal, cd into the frontend folder. Install the required dependencies by running ```npm install```. Then start the client by running ```npm start```.

The app will now be running at localhost:3000.


## API Reference

Base URL: This app can only be run locally. The default address is localhost:3000/.

### GET /categories

Fetches the complete list of all categories of trivia questions.
Arguments: none
Returns: an object with a categories key, the value of which is a dictionay containing the category ids mapped to the respective category name.
```
{
    "categories": {
        "1": "Science",
        "2": "Art"
    },
    "success": true
}
```

### GET /questions

Fetches all questions.
Arguments: page (int)
Returns: an object containing three fields: questions, total_questions, and categories. See the GET /categories endpoint for the structure of the categories field. The total_questions field is simply the number of all questions. The questions field contains a paginated list of 10 questions. Each question includes fields for the question id, question text, answer, difficulty, and category id.
```
{
    "total_questions": 2,
    "categories": {
        "1": "Science"
    },
    "questions": [
        {
            "id": 1,
            "question": "What?",
            "answer": "Yes",
            "difficulty": 4,
            "category": 1
        }
    ]
    "success": true
}
```

### DELETE /questions/{question_id}

Deletes the question with the specified id.
Arguments: none
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### POST /add

Creates a new question using the submitted data.
Arguments: In the data field of the request, an object should contain the question text (question), answer text (answer), difficulty, and category id (category).
Returns: an object that contains only the success field.
```
{
"success": true
}
```

### POST /questions

Searches question texts for the specified search term.
Arguments: In the data field of the request, an object should contain the search term (searchTerm).
Returns: an object that contains the relevant questions (using the same formatting specifid in GET /questions) and the number of relevant questions.
```
{
    "success": true,
    "total_questions": 1,
    "questions": [
        {
            "id": 1,
            "question": "What?",
            "answer": "Yes",
            "difficulty": 2,
            "category": 1
        }
    ]
}
```

### GET /categories/{category_id}/questions

Gets all questions in the specified category.
Arguments: none
Returns: an object with the same structure as POST /questions.
```
{
    "success": true,
    "total_questions": 1,
    "questions": [
        {
            "id": 1,
            "question": "What?",
            "answer": "Yes",
            "difficulty": 2,
            "category": 1
        }
    ]
}
```

### POST /quizzes

Gets the next question when playing a quiz.
Arguments: In the data field of the request, an object containing fields for quiz_category and previous_questions. The quiz_category field is an object that must contain a field for id (which denotes the specific category, use 0 if no category is selected.) The previous_questions field is a list containing the ids of questions that have been previously answered.
Returns: an object that contains a question field. This question field uses the same question formatting.
```
{
    "success": true,
    "question": {
        "question": "What?",
        "answer": "Yes",
        "difficulty": 2,
        "category": 1
    }
}
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false,
    "error": 400,
    "message": "Bad request."
}
```
