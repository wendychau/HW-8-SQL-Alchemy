import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"<u>Available Routes:<br/></u>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, avg, & max temp for range:<br/>"
        f"<em>(Input start date only; end date = last day)</em><br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"<br/>"
        f"<em>(Input start & end date)</em><br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def jsonified_precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()


    all_precipitation = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["prcp"] = precipitation.prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def jsonified_stations():
    stations_results = session.query(Measurement.station).all()
    all_stations = list(np.ravel(stations_results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def jsonified_tobs():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    tobs_data = []
    for tobs in precipitation_data:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["prcp"] = tobs.prcp
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def jsonified_start(start):
  
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    one_year_ago = dt.timedelta(days=365)
    start = start_date - one_year_ago
    end =  dt.date(2017, 8, 23)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(results))

    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def jsonified_start_end(start,end):

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end,'%Y-%m-%d')
    one_year_ago = dt.timedelta(days=365)
    start = start_date - one_year_ago
    end = end_date - one_year_ago
    results2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip2 = list(np.ravel(results2))
    return jsonify(trip2)

if __name__ == "__main__":
    app.run(debug=True)