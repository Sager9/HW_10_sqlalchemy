# Import the dependencies.

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from scipy import stats

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)



# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station



dates = measurement.date
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)





#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f'/api/v1.0/<start>'

    )

#percipitation for provios year
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #finds the year prior to max db year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    #query db for date and mesuremnt taking recent dates
    data = session.query(dates, measurement.prcp).filter(dates >= prev_year).all()


    
    #builds a dict out of query 
    data_out = {date: prcp for date,prcp in data}
    
    
    
    return jsonify(data_out)


#Gathers station names 
@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    data = session.query(station.name, station.station).all()

    data_out = {name:station for name, station in data}
    
    
    session.close()

    print(data)
    print(data_out)


    return jsonify(data_out)



#Gathers most active station dates and percipitation
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #finds the year prior to max db year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    #query db for date and mesuremnt taking recent dates
    data = session.query(dates, measurement.prcp).filter(dates >= prev_year, measurement.station == 'USC00519281')
    
    session.close()

    data_out = {date:prcp for date, prcp in data}



    return jsonify(data_out)


#Gathers min, max and average after start date
@app.route("/api/v1.0/<start>")
def start(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)


    data = session.query(dates, measurement.prcp).filter(dates >= start).all()

    data_out = {date:prcp for date, prcp in data}
    
    minimum = min(data_out.values())
    maximum = stats.tmax(data_out.values())
    #avg = stats.tavg(numbers) 

    session.close()

    

    print(minimum)


    return('alec')




if __name__ == '__main__':
    app.run(debug=True)







