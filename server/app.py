# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def get_by_id(id):
    record = Earthquake.query.filter_by(id=id).first()
    if record:
        txt = """
            {{
            "id": {},
            "location": "{}",
            "magnitude": {},
            "year": {}
                }}"""
        return txt.format(record.id,record.location,record.magnitude,record.year)
    else:
        return """{{
            "message":"Earthquake {} not found."
            }}""".format(id),404
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    res = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    #convert the result into a list of dictionaries
    quake_list = [{"id": quake.id,"location": quake.location, "magnitude": quake.magnitude,"year": quake.year} for quake in res]
    resp_body = jsonify({'count': len(quake_list), 'quakes': quake_list})
    return make_response(resp_body,200)
        


if __name__ == "__main__":
    app.run(port=5555, debug=True)
