import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    """
    Creates and returns a connection to the database using credentials
    stored in environment variables
    """
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),  # Use environment variable for host
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn

@app.route('/')
def index():
    """
    The main route that queries the database for estate listings, ordering
    them by price in descending order. Each estate's information is fetched,
    formatted, and then passed to a template to be displayed.
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM estates ORDER BY price DESC;')
    estates_raw = cur.fetchall()
    cur.close()
    conn.close()
    
    estates = []
    for estate_row in estates_raw:
        title = estate_row['title']
        image_urls = estate_row['image_urls']  
        price = f"{estate_row['price']:,}"
        
        estate_dict = {
            'title': title,
            'image_urls': image_urls,
            'price': price
        }
        estates.append(estate_dict)
        
    return render_template('estates.html', estates=estates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
