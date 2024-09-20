
import mysql.connector
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask.cli import with_appcontext
from config import SECRET_KEY,DB_CONFIG
from datetime import datetime,timezone,timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)

# conn = mysql.connector.connect (
#     user = 'root',
#     host = 'localhost',
#     password = 'SHREYASQL',
#     database = 'capstone_lilly'
# )
conn = mysql.connector.connect (
    user = DB_CONFIG['user'],
    host = DB_CONFIG['host'],
    password = DB_CONFIG['password'],
    database = DB_CONFIG['database']
)
app.config['SECRET_KEY'] = SECRET_KEY
cur = conn.cursor()
cursor = conn.cursor(dictionary=True)

@app.route('/users', methods=['GET'])
def get_users():
    cur.execute("SELECT * FROM user")  # Change to your table name
    results = cur.fetchall()
    # Convert results to a list of dictionaries
    users = [{'id': row[0], 'name': row[1]} for row in results]
    cursor.execute('SELECT id from user where email="admin@mail.com"')
    admin_id=cursor.fetchone()['id']
    # print(admin_id)
    return render_template('users.html', users=users,admin_id=admin_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            query = '''
                INSERT INTO user (username, email, password)
                VALUES (%s, %s, %s)
            '''
            cur.execute(query, (username, email, hashed_password))
            conn.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except BaseException as e:
            return f"There was an issue adding user: {e}"
    return render_template('register.html')

@app.route('/register_book', methods=['GET', 'POST'])
def register_book():
    cursor.execute('SELECT id from user where email="admin@mail.com"')
    admin_id=cursor.fetchone()['id']
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        try:
            cur.execute('''INSERT INTO book (title, author) VALUES (%s, %s)''', (title,author))
            conn.commit()
            print('done')
            flash('Your book has been added!', 'success')
            return redirect(url_for('index',user_id=admin_id))
        except BaseException as e:
            return f"There was an issue adding book:{e}"
    return render_template('register_book.html',admin_id=admin_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()
        print(user)
        if user and bcrypt.check_password_hash(user['password'], password):
            user_id = user['id']
            if user['email']=='admin@mail.com':
                return redirect(url_for('index',user_id=user_id))
            else:
                return redirect(url_for('borrowed_books',user_id=user_id))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/borrowed_books')
def borrowed_books():
    user_id = request.args.get('user_id', type=int)
    print(user_id)
    if user_id is None:
        return "User ID is required", 400
    
    cursor.execute('SELECT * from user where id=%s',(user_id,))
    user=cursor.fetchone()
    if user['email']=='admin@mail.com':
        cursor.execute('''
            SELECT user.username,book.title,book.author,Borrow.borrow_date,Borrow.return_date,Borrow.id
            FROM borrow left join user on Borrow.user_id=user.id 
            left join book on Borrow.book_id=book.id;
        ''')
        books_info = cursor.fetchall()
        print("books info:",books_info)
        return render_template('admin_borrowed_books.html', books_info=books_info, admin_id=user['id'])
    else:
        cursor.execute('''
            SELECT user.username,book.title,book.author,Borrow.borrow_date,Borrow.return_date,Borrow.id
            FROM borrow left join user on Borrow.user_id=user.id 
            left join book on Borrow.book_id=book.id where user.id=%s;
        ''',(user_id,))
        books_info = cursor.fetchall()
        return render_template('borrowed_books.html', books_info=books_info)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/books', methods=['GET'])
def get_books():
    cur.execute("SELECT * FROM book")  # Change to your table name
    results = cur.fetchall()
    
    books = [{'id': row[0], 'name': row[1], 'author': row[2]} for row in results]
    cursor.execute('SELECT id from user where email="admin@mail.com"')
    admin_id=cursor.fetchone()['id']
    return render_template('books.html', books=books,admin_id=admin_id)

@app.route('/borrow', methods=['GET'])
def get_borrow_table():
    cur.execute("SELECT * FROM borrow")  # Change to your table name
    results = cur.fetchall()
    
    borrow = [{'id': row[0], 'user': row[1], 'book': row[2], 'borrow_date': row[3], 'return_date': row[4]} for row in results]
    
    return borrow

@app.route('/borrow_function', methods=['GET', 'POST'])
def borrow_book():
    # print(current_user)
    cursor.execute('SELECT * from user')
    user_list = cursor.fetchall()
    # cursor.execute('SELECT * from book')
    cursor.execute('''
        SELECT book.id,book.title,book.author
        FROM Book LEFT JOIN Borrow ON book.id = Borrow.book_id
        WHERE Borrow.book_id IS NULL;
    ''')
    book_list = cursor.fetchall()    # book_list = Book.query.all()
    users=[]
    books=[]
    print(user_list,book_list)
    for user in user_list:
        users.append({'id':user['id'],'name':user['username']})
    for book in book_list:
        books.append({'id':book['id'],'name':book['title'],'author':book['author']})
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        book_id = request.form.get('book_id')
        # borrow = Borrow(user_id=user_id,book_id=book_id)
        cur.execute('INSERT into borrow(user_id,book_id) VALUES (%s,%s)',(user_id,book_id))
        try:
            conn.commit()
            flash('The book has been borrowed!', 'success')
            cursor.execute('SELECT id from user where email="admin@mail.com"')
            user_id=cursor.fetchone()['id']
            return redirect(url_for('borrowed_books',user_id=user_id))
        except BaseException as e:
            return f"There was an issue adding borrow book {e}"
    return render_template('borrowing_books.html',users=users,books=books)

@app.route('/return/<int:id>')
def delete(id):
    # task_to_delete = Borrow.query.get_or_404(id)
    cur.execute('DELETE FROM borrow WHERE id = %s',(id,))

    try:
        conn.commit()
        print('deleted')
        cursor.execute('SELECT id from user where email="admin@mail.com"')
        user_id=cursor.fetchone()
        print('user_id:',user_id['id'])
        return redirect(url_for('borrowed_books',user_id=user_id['id']))
    except BaseException as e:
        return f"There was a problem deleting that task ,{e}"
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # task=Borrow.query.get_or_404(id)
    query = 'UPDATE borrow SET borrow_date = %s,return_date = %s WHERE id = %s'
    borrow_date = datetime.now(timezone.utc)
    return_date = datetime.now(timezone.utc)+timedelta(days=14)
    cur.execute(query,(borrow_date,return_date,id))
    try:
        # db.session.commit()
        conn.commit()
        cursor.execute('SELECT * from user where email="admin@mail.com"')
        # user = User.query.filter_by(id=user_id).first()
        user=cursor.fetchone()
        # if user.is_admin==True:
        print(user)
        return redirect(url_for('borrowed_books',user_id=user['id']))
    except BaseException as e:
        return "There was an issue updating your task"+str(e)


@app.route('/')
def index():
    user_id = request.args.get('user_id', type=int)
    print(user_id)
    return render_template('index.html',user_id=user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8000)

