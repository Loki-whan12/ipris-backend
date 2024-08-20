
# Flask Backend for Plant Identification System

This repository contains the backend code for a plant identification system built with Flask. The backend provides APIs for user management, including creating new users and authenticating them, as well as functionality to fetch and store plant information.

## Features

- User registration with username, name, email, and password.
- Passwords are hashed before storage for security.
- Basic user authentication.
- Integration with plant identification services.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (optional, but recommended)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**

   Make sure you have a PostgreSQL (or other supported) database set up. Update the `config.py` file with your database configuration. Then, run:

   ```bash
   flask db upgrade
   ```

5. **Run the Application**

   ```bash
   flask run
   ```

   The application will start on [http://127.0.0.1:5000](http://127.0.0.1:5000) by default.

## API Endpoints

### User Management

#### Create a New User

**Endpoint:**

```http
POST /create
```

**Request Body:**

```json
{
  "username": "user123",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "yourpassword"
}
```

**Response:**

- `201 Created` if the user is created successfully.
- `409 Conflict` if the username is already taken.

### Example Code for User Creation

Here is the code for creating a new user:

```python
# Create a new user
@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    if db.session.query(db.exists().where(User.username == data['username'])).scalar():
        return jsonify({'message': 'Username taken'}), 409
    new_user = User(username=data['username'], name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201
```

## Configuration

### Environment Variables

You need to set up the following environment variables:

```plaintext
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=your_database_url
```

### Configuration File

Modify `config.py` to update the database connection and other settings.

## Suggestions

- **Error Handling:** Ensure comprehensive error handling for edge cases and validation errors.
- **Password Hashing:** Implement password hashing using `werkzeug.security` to ensure user passwords are securely stored.
- **Logging:** Implement logging to track application errors and debug issues effectively.

## Testing

To run tests, use:

```bash
pytest
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to suggest improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for the web framework.
- SQLAlchemy for ORM.
- Werkzeug for password hashing.
- PostgreSQL for the database management.
- Any external libraries or tools used in the project.
