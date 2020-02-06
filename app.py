# Flask API

from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

# Create Engine/Base
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
app = Flask(__name__)

Measurement = Base.classes.measurement
Hawaii = Base.classes.station


# Site map
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/api/v1.0/stations<br/>"
        f"/api/v1.0/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Create session, run query, dictionary comprehenesion, jsonify
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcpQuery = session.query(Measurement.prcp,Measurement.date).all()
    d = [{'date':date,'prcp':prcp} for prcp, date in prcpQuery]
    return jsonify(d)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    statQuery = session.query(Hawaii.station,Hawaii.name).all()

    sd = [{'station':station,'name':name} for station, name in statQuery]
    return jsonify(sd)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobQuery = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date < "2017-08-23", Measurement.date > "2016-08-23").all()
    tobD = [{'date':date,'tobs':tobs} for date, tobs in tobQuery]
    return jsonify(tobD)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    startEndQuery = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]
    sEQ = [{'min':startEndQuery[0],'avg':startEndQuery[1],'max':startEndQuery[2]}]
    return jsonify(sEQ)


if __name__ == '__main__':
    app.run(debug=True)

