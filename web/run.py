import os
import sqlite3
import folium
from functools import wraps
from db import Register, CheckUser, create_table, CheckData, CheckChartData
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import Flask, g, flash, render_template, redirect, url_for, request, session, get_flashed_messages

from passlib.hash import sha256_crypt

#Login Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için yetki sahibi değilsiniz! Giriş yapın.", "danger")
            return redirect(url_for("login"))
    return decorated_function

#Register
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5, max=35)])
    email = StringField("Email Adresi", validators=[validators.Email(message='Lütfen geçerli bir Email Adresi Giriniz.')])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyiniz"),
        validators.EqualTo(fieldname="confirm",message="parola uyuşmuyor!")
    ])
    confirm = PasswordField("Parola Doğrula")

#Login
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.secret_key=("__ToTaR__")

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

@app.route('/')
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg')
    return render_template('index.html', user_image = full_filename)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        Register(name,username,email,password)

        flash("Kaydınız başarılı bir şekilde gerçekleştirildi.", "success")
        return redirect(url_for("login"))
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    
    if request.method == 'POST':
        username = form.username.data
        password_entered = form.password.data

        result = CheckUser(username)
        
        if result:
            real_password = result[4]
            if sha256_crypt.verify(password_entered, real_password):
                flash("Başarıyla Giriş Yapıldı, Hoşgeldin {}".format(result[1]),"success")

                session["Logged_in"] = True
                session["username"] = username

                return redirect(url_for("dashboard"))
            else:
                flash("Parolanızı yanlış girdiniz!","warning")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor!","danger")
            return redirect(url_for("login"))

    return render_template("login.html", form = form)

#Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/data')
@login_required
def table():
    con = sqlite3.connect("database/TotarData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT plate, date, time, latitude, longitude, coordinate, address from Plates")
    rows = cur.fetchall() #istenilen sutunlari getir
    return render_template('table.html', rows = rows)

def saveTXT(filename,text):
    with open('{}'.format(filename),'w') as file:
        file.write(text)
        file.close()

@app.route("/dashboard")
@login_required
def dashboard():
    if True:
        result = CheckData()
       
        saveTXT("coordinateText.txt",'{},{}'.format(result[0],result[1]))
        print(result)
        map = folium.Map(
            location=[result[0],result[1]],
            zoom_start=16,
            widht="%75"
        )
        folium.Marker(
            location=[result[0],result[1]],
            popup="<i>TOTAR - Mobil Trafik Radar Sistemi</i>",
            tooltip = "Detay!"
        ).add_to(map)
        map.save("templates/includes/map.html")
        data = CheckChartData()
        labels=[row[0] for row in data]
        values=[row[1] for row in data]
        print(labels)
        print(values)

    return render_template("dashboard.html", labels = labels, values = values)

@app.route("/map")
@login_required
def map():
    return render_template("includes/map.html")

@app.route('/line')
@login_required
def line():
    data = CheckChartData()
    labels=[row[0] for row in data]
    values=[row[1] for row in data]

    print(data)
    return render_template('line_chart.html', labels = labels, values = values)

def __init__(self):
    con = sqlite3.connect("database/users.db")
    cursor = con.cursor()



if __name__ == '__main__':
    app.run(debug=True)
    server.use(express.static('public'));