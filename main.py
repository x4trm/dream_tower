from flask import Flask, render_template,flash,redirect,url_for
from form import MailForm
from flask_sqlalchemy import SQLAlchemy
import os

from flask_mail import Mail,Message



app = Flask(__name__)

#ustawienia maila
app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASS')
app.config['MAIL_MAX_EMAILS']=None

#baza danych
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///base.db'
app.config['SECRET_KEY']='70006f0ccb0b7edee8439669bed24f96'
#mail
mail = Mail()
mail.init_app(app)

db=SQLAlchemy(app)


'''def send_mail(subject,mail,wiadomosc):
    msg=Message(subject,sender=mail,recipients=[app.config['MAIL_USERNAME']])
    msg.body= wiadomosc
    mail.send(msg)'''
##########################
class Company(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True, nullable=False)
    floor= db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(40), unique=True, nullable=True)

    def __repr__(self):
        return f"Company('{self.name}','{self.floor}','{self.number}','{self.email}')"
class Business(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    floor= db.Column(db.Integer, nullable=False)
    number_id = db.Column(db.Integer,unique=True, nullable=False)
    surface = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Business('{self.number_id}','{self.floor}','{self.surface}','{self.rent}')"
class Work(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    position= db.Column(db.String(20), nullable=False)
    needments = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f"Business('{self.position}','{self.needments}','{self.benefits}')"

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")
@app.route('/opis')
def opis():
    return render_template('opis.html',title='Opis')
@app.route('/firmy')
def firmy():
    firmy=Company.query.all()
    return render_template('firmy.html',title='Firmy',firmy=firmy)

@app.route('/oferty')
def oferty():
    lokale=Business.query.all()
    return render_template('oferty.html',title='Oferty',lokale=lokale)
@app.route('/praca')
def praca():
    works=Work.query.all()
    return render_template('praca.html',title='Praca',works=works)
@app.route('/taras')
def taras():
    return render_template('taras.html',title='Taras')
@app.route("/kontakt", methods=['GET','POST'])
def kontakt():
    form = MailForm()
    if form.validate_on_submit():
        if form.temat.data and form.mail.data and form.wiadomosc.data:
            temat=form.temat.data
            email=form.mail.data
            wiadomosc=form.wiadomosc.data
            msg = Message(temat, sender=email, recipients=[app.config['MAIL_USERNAME']])
            msg.body = wiadomosc+'\n Wiadomosc wyslana przez: '+email
            mail.send(msg)
            flash('Twoja wiadomość została wysłana','success')
            return redirect(url_for('kontakt'))
        else:
            flash('Twoja wiadomość nie została wysłana!', 'danger')

    return render_template('kontakt.html',title='Kontakt',form=form)

if __name__=='__main__':
    app.run(debug=True)