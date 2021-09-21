import os
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)


##WTForms

class CafeForm(FlaskForm):
    name = StringField("Name of the Cafe", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location of the Cafe", validators=[DataRequired()])
    has_sockets = BooleanField("Has sockets?", false_values=(False, 'false', 0, '0'))
    has_toilet = BooleanField("Has toilet?", false_values=(False, 'false', 0, '0'))
    has_wifi = BooleanField("Has WiFi?", false_values=(False, 'false', 0, '0'))
    can_take_calls = BooleanField("Can you take calls there?", false_values=(False, 'false', 0, '0'))
    seats = SelectField("How many seats are there?",
                        choices=[("0-10", "0-10"), ("10-20", "10-20"), ("20-30", "20-30"), ("30-40", "30-40"),
                                 ("50+", "50+")])
    coffee_price = StringField("Price of coffee", validators=[DataRequired()])
    submit = SubmitField("Submit")


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class Cafes(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    map_url = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    location = db.Column(db.String(250))
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def all_cafes():
    list_caffes = db.session.query(Cafes).all()
    return render_template("cafes.html", all_caffes=list_caffes)


@app.route("/cafe/<int:cafe_id>", methods=["GET"])
def show_cafe(cafe_id):
    requested_cafe = Cafes.query.get(cafe_id)
    return render_template("detail_cafe.html", detail_cafe=requested_cafe)


@app.route("/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafes.query.get(cafe_id)
    edit_cafe_form = CafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )
    if edit_cafe_form.validate_on_submit():
        cafe.name = edit_cafe_form.name.data
        cafe.map_url = edit_cafe_form.map_url.data
        cafe.img_url = edit_cafe_form.img_url.data
        cafe.location = edit_cafe_form.location.data
        cafe.has_sockets = edit_cafe_form.has_sockets.data
        cafe.has_toilet = edit_cafe_form.has_toilet.data
        cafe.has_wifi = edit_cafe_form.has_wifi.data
        cafe.can_take_calls = edit_cafe_form.can_take_calls.data
        cafe.seats = edit_cafe_form.seats.data
        cafe.coffee_price = edit_cafe_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("show_cafe", cafe_id=cafe.id))
    return render_template("add_cafe.html", form=edit_cafe_form)


@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafes(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))
    return render_template("add_cafe.html", form=form)


if __name__ == '__main__':
    app.run()
