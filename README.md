# Wedding Website

This is a Flask-based web application for a wedding website, providing information about the event, RSVP functionality, and more.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Deploying to AWS Elastic Beanstalk](#deploying-to-aws-elastic-beanstalk)
- [Environment Variables](#environment-variables)
- [License](#license)

## Getting Started

Follow these instructions to set up a development environment and run the project locally.

### Prerequisites

- Python 3.9
- pip (Python package installer)
- Git
- AWS CLI
- EB CLI (Elastic Beanstalk CLI)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/wedding-website.git
   cd wedding-website
   ```

2. **Create a virtual environment:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

### Running the App

1. **Run the Flask application:**

   ```sh
   flask run
   ```

2. **Access the application in your web browser:**

   ```sh
   http://127.0.0.1:5000
   ```

### Deploying to AWS Elastic Beanstalk

1. **Configure AWS CLI:**

   ```sh
   aws configure
   ```

2. **Initialize Elastic Beanstalk:**

   ```sh
   eb init -p python-3.9 wedding-website --region us-east-1
   ```

3. **Create an environment:**

   ```sh
   eb create wedding-website-env
   ```

4. **Deploy the application:**

   ```sh
   eb deploy
   ```

### Environment Variables

Create a `config.py` file to store your environment variables:

```python
class Config:
    SECRET_KEY = 'your_secret_key'
    SESSION_TYPE = 'filesystem'
```