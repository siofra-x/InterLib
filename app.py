from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books')
def books():
    conn = sqlite3.connect('intbook.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Title, Author, Price, Language, Cover_url FROM Books")
    books = cursor.fetchall()
    conn.close()
    return render_template('books.html', books=books)
