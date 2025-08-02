# Flask Sessions Summative Lab
This lab creates a secure Flask API backend, implementing authentication using session-based methods. The backend adds users and a resource of a mood tracker to a provided front end.

## Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
   ```

2. **Create and Activate a Virtual Environment**
    ```bash
    virutalenv env
    source env/bin/activate
    ```
3. **Install all Necessary Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Up the Database**
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```
5. Seed the Database
    ```bash
    python seed.py
    ```
## Run Instructions
To start the development server:
```bash
python app.py
```

## API Endpoints
* `POST /signup` <br>
A user creates an account with a username, password, and name
* `POST /login` <br>
User's login with their username and password
* `GET /check_session` <br>
Returns a users information if they are logged in, otherwise sends a message informing the user they are not logged in.
* `DELETE /logout` <br>
Logs a user out 
* `GET /moods?page=1&per_page=2` <br>
Gets all of a user's moods, response is paginated
* `POST /moods` <br>
Create a mood for a user
* `GET /moods/<int:id>` <br>
Get a mood by id, user's only have access to their own moods
* `PATCH /moods/<int:id>` <br>
Update a mood, user's can only update their own moods
* `DELETE/moods/<int:id>` <br>
Delete a mood, user's can only delete their own moods

