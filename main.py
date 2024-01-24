from flask import Flask, jsonify
import psycopg2
import config as cfg
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
