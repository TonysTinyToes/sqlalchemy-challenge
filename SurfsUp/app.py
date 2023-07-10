# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create session object to connect to DB
session = Session(bind=engine)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
# Initialize a Flask web server 
app = Flask(__name__)

# Define home function
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>" # Returns a string with available routes/ endpoints
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0<start>/<end>"
    )   


#################################################
# Flask Routes

# Define the Precipitation function
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the Measurement table for date and precipitation fields
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Transform result, list of tuples, into a dictionary
    precip_dict = {date: prcp for date, prcp in results}

    # Convert the dictionary into a JSON response
    return jsonify(precip_dict)


# Define the Stations function
@app.route("/api/v1.0/stations")
def stations():
    # Query the Station table for station fields.
    results = session.query(Station.station).all()

    # Convert the result, another list of tuples, into a list
    stations = list(np.ravel(results))

    # Convert again to JSON response
    return jsonify(stations)

# Define Tobs function
@app.route("/api/v1.0/tobs")
def tobs():

    # Query the Measurement table for the tobs field for the most active station
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').all()
   
    # transform again such that the function returns a JSON-ified result
    tobs = list(np.ravel(results))
    return jsonify(tobs)



# Define Start function as a dynamic route that uses the input date in the query function
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query the Measurement table for min, average, and max, but only for dates greater/
    # equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Return results as JSON
    temperatures = list(np.ravel(results))
    return jsonify(temperatures)


# Define Start/End function as a dynamic route that uses the input date range in the 
# query function
@app.route("/api/v1.0/<start><end>")
def start_end_date(start, end):

    # Query the Measurement table for min, average, and max, but only for dates between 
    # start and end date 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                func.max(Measurement.tobs)).filter(Measurement.date <= start).filter(Measurement.date <= end).all()

    temperatures = list(np.ravel(results))
    return jsonify(temperatures)

# This is the entry point of the app
if __name__  == '__main__':
    app.run(debug=True)
#################################################