from flask import Flask, jsonify, render_template, request
import psycopg2
import config as cfg
from psycopg2 import sql


app = Flask(__name__)

db_params = cfg.db_params

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search/<int:book_id>', methods=['GET'])
def search_book(book_id):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=cfg.host,
        database=cfg.database,
        user=cfg.user,
        password=cfg.password
    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query to fetch book information by Book_ID
    cursor.execute("SELECT * FROM book_store WHERE book_id = %s", (book_id,))
    book_data = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    conn.close()

    if book_data:
        # Return book information in JSON format
        return jsonify({'Book_ID': book_data[0], 'Author_name': book_data[1], 'Book_name': book_data[2],
                        'Publish_year': book_data[3], 'Price': book_data[4]})
    else:
        return jsonify({'message': 'Book not found'}), 404
    
@app.route('/add_user_form')
def add_user_form():
    return render_template('yay.html')

# -----------------  POST ----------------
def execute_query(query, params=None):
    connection = None
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        connection.commit()

    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        return str(e), 500

    finally:
        if connection:
            connection.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    # Get form data from the request
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email is already registered
    query_check_email = sql.SQL("SELECT 1 FROM users WHERE email = {} LIMIT 1").format(sql.Literal(email))
    result = execute_query(query_check_email)
    
    if result and result[0]:
        return jsonify({'message': 'Email already registered'}), 400

    # Insert the new user into the database
    query_insert_user = sql.SQL("INSERT INTO users (username, email, password) VALUES ({}, {}, {})").format(
        sql.Literal(username), sql.Literal(email), sql.Literal(password)
    )

    result = execute_query(query_insert_user)

    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
