from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
app = Flask(__name__)
app.secret_key = 'eozretailer'

#Config SQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'eozretailer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about_us')
def about():
    return render_template('about_us.html')


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=4, max=50)])
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phone_no = form.phone_no.data
        username = form.username.data
        password = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, phone_no, username, password) VALUES (%s, %s, %s, %s, %s)", (name, email, phone_no, username, password))
        
        # Commit to database
        mysql.connection.commit()

        # Close connection
        cur.close()
        session['username'] = username
        flash("You registered successfully and logged in", "success")
        return redirect(url_for("profile", username = username))
    return render_template ('register.html', form = form)

@app.route('/profile/<username>')
def profile(username):
    return render_template('home.html', username = username)

@app.route('/approved/<username>')
def approved(username):
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phone_no = form.phone_no.data
        username = form.username.data
        password = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE (username, password) VALUES (%s, %s)", (username, password,)) 

        if cur.fetchone():
            session['username'] = username
            flash(f'You logged in successfully', 'success')
            return redirect(url_for('home'))
        
        else:
            flash(f'Log in process failed, please try again!', 'danger')
            return redirect(url_for('login'))
        
        # Commit to database
        mysql.connection.commit()

        # Close connection
        cur.close()
    return render_template('home.html', username = username)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    form = RegisterForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute( "SELECT * FROM users WHERE username LIKE %s", [username] )
        result=cur.fetchone()
        if result and result['password']==password:
            session['username'] = username
            flash(f'You logged in successfully', 'success')
            return redirect(url_for("profile", username = username))
        else:
            flash(f'Log in process failed, please try again!', 'danger')
            return redirect(url_for('login'))
        

        # Close connection
        cur.close()

        return redirect(url_for("profile", username = username))
    return render_template ('login.html', form = form)

@app.route('/logout')
def logout():
    if  'username' in session:
        session.pop('username', None)
        flash(f'You logged out successfully', 'success')
        return render_template('home.html')

    else:
        return render_template('home.html')


@app.route('/product_001')
def product_001():
    if 'username' in session:
        return render_template('product_001.html')

    else:
        return render_template('home.html')

@app.route('/product_002')
def product_002():
    if 'username' in session:
        return render_template('product_002.html')

    else:
        return render_template('home.html')

@app.route('/product_003')
def product_003():
    if 'username' in session:
        return render_template('product_003.html')

    else:
        return render_template('home.html')

class CommentForm(Form):
    comment = TextAreaField('Comment')

@app.route('/comment',  methods=['POST', 'GET'])
def comments():
    if 'username' in session:
        form = CommentForm(request.form)
        if request.method == 'POST':
            comment = str(form.comment.data)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO comment(comment_desc) VALUES (%s)", [comment])

            mysql.connection.commit()

            cur.close()

            flash(f'Thank you for commenting us!', 'success')
        return render_template ('comment_us.html', form = form)
    
    else:
        return render_template('home.html')

@app.route('/cart')
def cart():
    if 'username' in session:
        return render_template('cart.html')

    else:
        return render_template('home.html')

@app.route('/checkout')
def checkout():
    if 'username' in session:
        return render_template('checkout.html')

    else:
        return render_template('home.html')

if __name__== '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080) 