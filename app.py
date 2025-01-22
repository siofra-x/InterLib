from flask import Flask, session, redirect, url_for, render_template, request
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-very-secret-key' 

def get_db_connection():
    conn = sqlite3.connect('intbook.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/library', methods=['GET', 'POST'])
def books():
    try:
        conn = get_db_connection()
        books = conn.execute('''
            SELECT b.BookId, b.Title, b.Author, b.Price, b.Language, b.Cover_url, g.Type AS Genre, c.Symbol, c.CurrencyId, b.Purchase_url
            FROM Books b
            JOIN Genre g ON g.GenreId = b.GenreId
            join Currency c on c.CurrencyId = b.CurrencyId 
        ''').fetchall()
        print(books)
    except Exception as e:
        print(f"Error fetching books: {e}")
        books = []  
    finally:
        conn.close()
    return render_template('library.html', books=books)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        origin_country = request.form.get('origin_country')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Users (Username, Password, Email, Origin_country) VALUES (?, ?, ?, ?)',
                         (username, password, email, origin_country))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username already exists")
        except Exception as e:
            return render_template('signup.html', error=f"Database error: {e}")
        finally:
            conn.close()

        return redirect('/')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE Username = ? AND Password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = user['Username']  # Store the username
            session['user_id'] = user['UserId']  # Store the user_id
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    session.pop('user_id', None)   # Remove the user_id from the session
    return redirect('/')

@app.route('/favourites', methods=['GET', 'POST'])
def favourites():
    try:
        conn = get_db_connection()
        user_id = session.get('user_id')
        books = conn.execute('''
            SELECT b.BookId, b.Title, b.Author, b.Price, b.Language, b.Cover_url, g.Type AS Genre, b.Purchase_url
            FROM Books b
            JOIN Genre g ON g.GenreId = b.GenreId
            JOIN Favourites f on f.BookId = b.BookId
            where f.UserId = ?
        ''',(user_id,)).fetchall()
        print(books)
    except Exception as e:
        print(f"Error fetching books: {e}")
        books = []  
    finally:
        conn.close()
    return render_template('favourites.html', books=books)

@app.route('/add_to_favourites', methods=['POST'])
def add_to_favourites():
    data = request.get_json()
    book_id = data.get('bookId')  # Get BookId from the JSON body
    user_id = session.get('user_id')  # Get logged-in UserId

    if not user_id:
        return "User not logged in", 403
    if not book_id:
        return "Book ID is required", 400

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO Favourites (UserId, BookId) VALUES (?, ?)', (user_id, book_id))
        conn.commit()
    except sqlite3.IntegrityError:
        return "This book is already in your favourites!", 409
    finally:
        conn.close()

    return "Book added to favourites!", 200

@app.route('/remove-from-favourites', methods=['GET'])
def remove_from_favourites():
    try:
        conn = get_db_connection()
        user_id = session.get('user_id')  
        book_id = request.args.get('book_id')  

        if not book_id:
            return "Book ID is required.", 400

        conn.execute('''
            DELETE FROM Favourites
            WHERE UserId = ? AND BookId = ?
        ''', (user_id, book_id))
        conn.commit()  
        return redirect('/favourites')  
    except Exception as e:
        print(f"Error removing book from favourites: {e}")
        return "An error occurred while removing the book.", 500
    finally:
        conn.close()


@app.route('/add-books', methods=['GET', 'POST'])
def add_books():
    if request.method == 'POST':
        title = request.form.get('title')
        genre_id = request.form.get('genre_id')
        price = request.form.get('price')
        currency_id = request.form.get('currency_id')
        author = request.form.get('author')
        seriesname = request.form.get('seriesname')
        isbn = request.form.get('isbn')
        country = request.form.get('country')
        language = request.form.get('language')
        blurb = request.form.get('blurb')
        cover_url = request.form.get('coverurl')
        purchase_url = request.form.get('purchaseurl')

        conn = get_db_connection()
        try:
            conn.execute(
                '''INSERT INTO Books 
                (Title, GenreId, Price, CurrencyId, Author, Series_name, ISBN, Country, Language, Blurb, Cover_url, Purchase_url) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (title, genre_id, price, currency_id, author, seriesname, isbn, country, language, blurb, cover_url, purchase_url)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            
            return render_template('add-books.html', error="Book with this ISBN already exists or invalid data")
        except Exception as e:
           
            return render_template('add-books.html', error=f"Database error: {e}")
        finally:
            conn.close()

        return redirect('/library')  

    return render_template('add-books.html')

@app.route('/remove-from-books', methods=['GET'])
def remove_from_books():
    book_id = request.args.get('book_id')  # Retrieve book_id from the query string
    user_id = session.get('user_id')       # Retrieve user_id from the session

    if not book_id or not user_id:
        return "Invalid request", 400 

    conn = get_db_connection()
    try:
        conn.execute(
            "DELETE FROM Books WHERE BookId = ?", 
            (book_id,)
        )
        conn.commit()
        return redirect('/library')  
    except Exception as e:
        return f"Error: {e}", 500
    finally:
        conn.close()

@app.route('/edit-book', methods=['POST'])
def edit_book():
    data = request.get_json()  
    print(f"Received data: {data}")  # Log received data for debugging
    book_id = int(data.get('book_id'))  
    title = data.get('title')  
    language = data.get('language')  
    price = data.get('price')
    purchase_url = data.get('purchase_url')

    if not all([book_id, title, language, price, purchase_url ]):
        print("Missing fields detected!")  # Log missing fields for debugging
        return "Invalid request - missing fields", 400

    conn = get_db_connection()
    try:
        conn.execute(
            """UPDATE Books 
               SET Title = ?, Language = ?, Price = ?, Purchase_url = ?
               WHERE BookId = ?""",
            (title, language, price, purchase_url, book_id)
        )
        conn.commit()
        return "Book updated successfully", 200
    except Exception as e:
        return f"Error: {e}", 500
    finally:
        conn.close()


        
if __name__ == "__main__":
    app.run(debug=True)