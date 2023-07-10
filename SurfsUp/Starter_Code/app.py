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
        f"/api/v1.0/precipitations<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0?<start><end>"
    )   


#################################################
# Flask Routes

# Define the Precipitation function
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the Measurement table for date and precipitation fields
    results = session.query(Measurement.date, Measurement.pcrp).all()

    # Transform result, list of tuples, into a dictionary
    precip_dict = {date: pcrp for date, pcrp in results}

    # Convert the dictionary into a JSON response
    return jsonify(precip_dict)


# Define the Stations function
@app.route("/api/v1.0/stations")
def stations():
     # Here we're querying the Station table for station fields.

    # We're using numpy's ravel method to convert the result (which is a list of tuples) into a list.

    

#################################################
