from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, request,jsonify, abort, make_response
from flask_mysqldb import MySQL
from flask_restful import Api, Resource
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
import json, requests
app = Flask(__name__)
api = Api(app)
app.secret_key = 'eozretailer'

#Config SQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'svsuhsvud#3vxHia'
app.config['MYSQL_DB'] = 'eozretailer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def home():
    url = requests.get("http://eozlogistic.ddns.net/api")
    text = url.text
    data = json.load(text)
    return render_template('home.html', url=url, text=text, data=data)

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
class CartForm(Form):
    address = TextAreaField('Billing Address')
    qty_1 = IntegerField('Product 1', [validators.NumberRange(min=1, max=25)])
    qty_2 = IntegerField('Product 2', [validators.NumberRange(min=1, max=25)])
    qty_3 = IntegerField('Product 3', [validators.NumberRange(min=1, max=25)])

@app.route('/cart',  methods=['POST', 'GET'])
def cart():
    if 'username' in session:
        form = CartForm(request.form)
        if request.method == 'POST' and form.validate():
            address = form.address.data
            qty_1 = form.qty_1.data
            qty_2 = form.qty_2.data
            qty_3 = form.qty_3.data
            total = qty_1*149.9 +qty_2*749 + qty_3*329.9

            # Create cursor
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cart(address, qty_1, qty_2, qty_3, total) VALUES (%s, %s, %s, %s, %s)", (address, qty_1, qty_2, qty_3, total))
            
            # Commit to database
            mysql.connection.commit()

            # Close connection
            cur.close()
            return redirect(url_for('checkout'))
        return render_template ('cart.html', form = form)

    else:
        return render_template('home.html')

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if 'username' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM cart order by cartid DESC limit 1")
        if result > 0:
            cartDetails = cur.fetchall()
            return render_template('checkout.html', cartDetails = cartDetails)
    else:
        return render_template('home.html')

@app.route('/success_checkout', methods=['POST', 'GET'])
def success_checkout():
    if 'username' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM cart order by cartid DESC limit 1")
        if result > 0:
            cartDetails = cur.fetchall()
            data_json = json.dumps(cartDetails[0], indent = 4)
            requests.get("http://eozlogistic.ddns.net/insert123456")
            return render_template('success_checkout.html', cartDetails = cartDetails)

    else:
        return render_template('home.html')

@app.route('/ship_details')
def ship_details():
    if 'username' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM cart order by cartid DESC limit 1")
        if result > 0:
            cartDetails = cur.fetchall()
            return render_template('ship_details.html', cartDetails = cartDetails)
    else:
        return render_template('home.html')

if __name__== '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080) 
