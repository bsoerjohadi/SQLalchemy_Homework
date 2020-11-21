import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Setup Flask
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Surfs Up Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return the JSON representation of your dictionary
    prcps = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23', Measurement.date < '2017-08-23').all()
    
    year_prcps = []
    for date,prcp in prcps:
        year_prcps_dict = {}
        year_prcps_dict["Date"] = date
        year_prcps_dict["Precipitation"] = prcp

        year_prcps.append(year_prcps_dict)
    return jsonify(year_prcps)

@app.route("/api/v1.0/stations")
def stations():
	# Return a json list of stations from the dataset
	stations = session.query(Station.station).all()

	all_stations = list(np.ravel(stations))

	return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    # Query the dates and temperature observations of the most active station for the last year of data
    last_temperature = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23', Measurement.date < '2017-08-23').\
        filter(measurement.station == 'USC00519281').all()
    # Return a json list of Temperature Observations (tobs) for the previous year	
    temperature = list(np.ravel(last_temp))
	return jsonify(temperature)

@app.route("/api/v1.0/<start>")
def temp(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    temp = list(np.ravel(start_temp))
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def temp(start, end):
    end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all
    temp2 = list(np.ravel(end_temp))
    return jsonfity(temp2)

if __name__ == "__main__":
    app.run(debug=True)
   