# AppAvaliacaoFluenciaLeitora

## Description

AppAvaliacaoFluenciaLeitora is a Flask-based application designed to assist in the assessment of reading fluency. This backend manages user authentication, processes audio for transcription, calculates reading performance metrics, and provides these services via a RESTful API intended for integration with a front-end application.

## Features

- User Authentication (login and logout).
- Audio transcription and analysis.
- Calculation of reading metrics such as speed and accuracy.
- RESTful API endpoints for front-end integration.

## Technology Stack

- **Backend**: Flask
- **Database**: MySQL
- **Audio Processing**: SpeechRecognition
- **WSGI Server**: Gunicorn for production environments

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- MySQL
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/appAvaliacaoFluenciaLeitora.git
   cd appAvaliacaoFluenciaLeitora

2. **Set up a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows use `venv\Scripts\activate`

3.**Install dependencies**

  ```bash
 pip install -r requirements.txt
```

4.**Environment Configuration, Ensure all necessary environment variables are set, for example:**

  ```bash
    export FLASK_APP=run.py
    export FLASK_ENV=development
    export SECRET_KEY='your_secret_key'
```

5.**Database Setup Initialize your MySQL database and run any necessary migrations.**

6.**Running the application**

  ```bash
    flask run
    gunicorn app:app
```

7.**Accessing the application `Visit http://localhost:5000` in your web browser to view the application.**

**Deployment**

For deploying this application in a production environment, consider using services such as Heroku, AWS, or DigitalOcean.

Heroku Deployment Guide: https://devcenter.heroku.com/categories/deployment

**Built With**

- Flask - The web framework used.
- MySQL - Database system.
- SpeechRecognition - Library for performing speech recognition tasks

