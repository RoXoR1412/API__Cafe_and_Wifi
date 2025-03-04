from crypt import methods

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

def to_dict(self):
    dictionary={}
    for column in self.__table__.columns:
        dictionary[column.name]=getattr(self,column.name)
    print(dictionary)
    return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record

@app.route("/random")
def get_random_cafe():
    result=db.session.execute(db.select(Cafe))
    all_cafe=result.scalars().all()
    random_cafe=random.choice(all_cafe)
    return jsonify(to_dict(random_cafe))

@app.route("/all")
def get_all_cafe():
    result=db.session.execute(db.select(Cafe))
    all_cafe=result.scalars().all()
    return jsonify(cafes=[to_dict(cafe) for cafe in all_cafe])

@app.route("/search")
def search_cafe():
    location=request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    all_cafe = result.scalars().all()
    if all_cafe:
        return jsonify(cafe=[to_dict(cafe) for cafe in all_cafe])
    return jsonify({"error": "Please provide a location."}), 400

@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("has_sockets")),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response="Cafe added successfully.")

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_cafe(cafe_id: int):
    updated_price = request.args.get("updated_price")
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if cafe:
        cafe.coffee_price = updated_price
        db.session.commit()
        return jsonify(response="Cafe price updated successfully.")
    return jsonify(error="Cafe not found."), 404

@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id: int):
    api_key=request.args.get("api-key")
    if api_key != "top secret key":
        return jsonify(error="Invalid API key."), 403
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response="Cafe deleted successfully.")
    return jsonify(error="Cafe not found."), 404







#   return jsonify(cafe={
#         #"id": random_cafe.id,
#         "name": random_cafe.name,
#         "map_url": random_cafe.map_url,
#         "img_url": random_cafe.img_url,
#         "location": random_cafe.location,
#         "amenities":{
#
#             "seats": random_cafe.seats,
#             "has_toilet": random_cafe.has_toilet,
#             "has_wifi": random_cafe.has_wifi,
#             "has_sockets": random_cafe.has_sockets,
#             "can_take_calls": random_cafe.can_take_calls,
#             "coffee_price": random_cafe.coffee_price,
#         }
#     })




# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
