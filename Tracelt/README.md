# Tracelt

A Flask web application for a school Lost, Found, and For Sale platform.

## Features

- Add lost, found, or sale items
- Search and filter items
- View item details
- Dark and light mode toggle
- Responsive design

## Installation

1. Install Python 3.x
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Open http://127.0.0.1:5000/ in your browser

## Deployment on Render

1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `gunicorn app:app`
5. Deploy.

Note: SQLite database will reset on redeploys. For persistent data, consider using a database like PostgreSQL.
Note: Gunicorn is used for production on Linux; locally on Windows, use `python app.py`.

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates
- `static/`: CSS, JS, and uploaded images
- `tracelt.db`: SQLite database (created automatically)