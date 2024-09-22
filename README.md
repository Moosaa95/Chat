# AI Chat System

A RESTful API-based AI Chat System built with Django and Django REST Framework (DRF). This system allows users to register, log in, and interact with an AI-powered chatbot. Each interaction with the chatbot deducts tokens from the user's account, promoting efficient usage.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Chat](#chat)
  - [Token Balance](#token-balance)
- [Sample Requests and Responses](#sample-requests-and-responses)
- [Challenges Encountered](#challenges-encountered)
- [Suggestions for Improvement](#suggestions-for-improvement)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Registration**: Create a new account with a unique username, email, and password.
- **User Login**: Authenticate using username to receive an authentication token.
- **AI Chat Interaction**: Send messages to an AI chatbot and receive responses while deducting tokens.
- **Token Management**: Track and view remaining tokens in the user's account.
- **Secure Authentication**: Token-based authentication ensuring secure access to protected endpoints.
- **Admin Interface**: Manage users, chats, and tokens via Django's admin panel.

## Technologies Used

- **Python 3.12**
- **Django 5.1.1**
- **Django REST Framework**
- **SQLite** (default; can be replaced with PostgreSQL or others)

## Prerequisites

- **Python 3.12**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/moosa/chat.git
   cd chat
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not present, install dependencies manually:*

  
4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**

   To access Django's admin interface.

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   The application will be accessible at `http://localhost:8000/`.

## Configuration

1. **Environment Variables**

   It's good practice to manage sensitive configurations using environment variables. Create a `.env` file in the project's root (optional) and add necessary configurations.

   ```bash
   DEBUG=True
   SECRET_KEY=your_secret_key
   
   ```

   *Ensure to set `SECRET_KEY` to a strong, unique value in production and use appropriate email backends.*



## Running the Application

Start the development server:

```bash
python manage.py runserver
```

Access the API at `http://localhost:8000/api/` and the admin interface at `http://localhost:8000/admin/`.

## API Endpoints

### User Registration

- **URL**: `/api/register/`
- **Method**: `POST`
- **Permissions**: `AllowAny`
- **Description**: Register a new user with a unique username and email. Upon successful registration, a token is provided.

#### Request Body

```json
{
    "username": "jane_doe",
    "password": "StrongPass123!"
}
```

### User Login

- **URL**: `/api/login/`
- **Method**: `POST`
- **Permissions**: `AllowAny`
- **Description**: Log in using either username or email along with the password to receive an authentication token.

#### Request Body (Login via Username)

```json
{
    "username": "jane_doe",
    "password": "StrongPass123!"
}
```

### Chat

- **URL**: `/api/chat/`
- **Method**: `POST`
- **Permissions**: `IsAuthenticated`
- **Description**: Send a message to the AI chatbot. Each message deducts 100 tokens from the user's account.

#### Headers

```http
Authorization: Token your_token_here
```

#### Request Body

```json
{
    "message": "Hello, AI!"
}
```

### Token Balance

- **URL**: `/api/tokens/`
- **Method**: `GET`
- **Permissions**: `IsAuthenticated`
- **Description**: Retrieve the remaining number of tokens in the user's account.

#### Headers

```http
Authorization: Token your_token_here
```

## Sample Requests and Responses

### 1. User Registration

**Request**

```bash
curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "jane_doe",
           "password1": "StrongPass123!"
         }'
```

**Response (HTTP 201 Created)**

```json
{
    "message": "User registered successfully.",
    "token": "a1b2c3d4e5f6g7h8i9j0..."
}
```

### 2. User Login

**Request (Via Username)**

```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "jane_doe",
           "password": "StrongPass123!"
         }'
```

**Response (HTTP 200 OK)**

```json
{
    "token": "a1b2c3d4e5f6g7h8i9j0..."
}
```

### 3. Chat

**Request**

```bash
curl -X POST http://localhost:8000/api/chat/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0..." \
     -d '{
           "message": "Hello, AI!"
         }'
```

**Response (HTTP 200 OK)**

```json
{
    "response": "Echo: Hello, AI!",
    "remaining_tokens": 3900
}
```

### 4. Token Balance

**Request**

```bash
curl -X GET http://localhost:8000/api/tokens/ \
     -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0..."
```

**Response (HTTP 200 OK)**

```json
{
    "tokens": 3900
}
```

## Challenges Encountered

1. **Custom User Model Integration**: Extending Django's `AbstractBaseUser` required careful setup of the `UserManager`, `USERNAME_FIELD`, and `REQUIRED_FIELDS`. Missing essential attributes like `REQUIRED_FIELDS` led to attribute errors during authentication checks.

2. **Token Authentication**: Implementing a custom token-based authentication system necessitated ensuring that the `User` model integrated seamlessly with DRF's permission classes. Initially, missing properties like `is_authenticated` in the custom `User` model caused permission-related errors.

3. **Password Handling**: Ensuring secure password storage and validation required integrating Django's built-in password hashing and validation mechanisms within serializers and the user creation process.

4. **Flexible Login Mechanism**: Allowing users to log in using username added complexity to the login serializer and view, requiring conditional authentication logic.

## Suggestions for Improvement

1. **Implement Email Verification**: Enhance security by requiring users to verify their email addresses during registration. This can prevent spam accounts and ensure the validity of user emails.

2. **Token Expiry and Refresh Mechanism**: Introduce token expiration to enhance security. Implementing a token refresh endpoint can allow users to obtain new tokens without re-authenticating.

3. **Integrate with Third-Party AI Services**: Replace the dummy AI response with actual integration to AI services like OpenAI's GPT models to provide meaningful chatbot interactions.

4. **Rate Limiting and Throttling**: Implement rate limiting to prevent abuse of the chat API, ensuring fair usage and protecting against potential DDoS attacks.

5. **Comprehensive Testing**: Expand unit and integration tests to cover all possible scenarios, ensuring the reliability and robustness of the API.

6. **Deploy to Production**: Set up deployment configurations for production environments, including configuring a production-ready database (e.g., PostgreSQL), setting up a web server (e.g., Gunicorn with Nginx), and securing the application with HTTPS.

7. **API Documentation**: Enhance API documentation using tools like Swagger (`drf-yasg`) to provide interactive and comprehensive API docs for developers.

8. **User Profile Management**: Allow users to update their profiles, including changing passwords, updating personal information, and managing tokens.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes**

4. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

5. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

---

   
**Note**: Replace `git clone https://github.com/moosa/chat.git` with the actual URL of your GitHub repository. Also, ensure to include a `requirements.txt` file listing all project dependencies for easier installation.
