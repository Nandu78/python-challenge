import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, request, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Adding below code to manage session betweek routes
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/daterange?startdate=&enddate="
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    sel = [func.strftime("%Y", Measurement.date), 
                     func.strftime("%m", Measurement.date), func.strftime("%d", Measurement.date)]
    latest_dt = session.query(*sel).order_by(Measurement.date.desc()).first()
    latest_year = int(latest_dt[0])
    latest_month = int(latest_dt[1])
    latest_day = int(latest_dt[2])

    # Calculate the date 1 year ago from the last data point in the database
    latest_date = dt.date(latest_year, latest_month, latest_day)
    last_year = latest_date - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    stmt = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= latest_date).\
        filter(Measurement.date >= last_year).statement
    lastyrdata_df = pd.read_sql_query(stmt, session.bind)
    lastyrdata_df =  lastyrdata_df[np.isfinite(lastyrdata_df['prcp'])]
    
    # Save the query results as a Pandas DataFrame and set the index to the date column
    lastyrdata_df = lastyrdata_df.set_index('date')

    #convert to dictionary and then jsonify the response
    res_dict = lastyrdata_df.to_dict('dict')
    return jsonify(res_dict)

    
@app.route("/api/v1.0/stations")
def stations():
    # Get unique stations
    stations = session.query(Measurement.station).group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations )

@app.route("/api/v1.0/tobs")
def tobs():
 # Design a query to retrieve temperature data start the latest date record going back 1 year
    sel = [func.strftime("%Y", Measurement.date), 
                     func.strftime("%m", Measurement.date), func.strftime("%d", Measurement.date)]
    latest_dt = session.query(*sel).order_by(Measurement.date.desc()).first()
    latest_year = int(latest_dt[0])
    latest_month = int(latest_dt[1])
    latest_day = int(latest_dt[2])

    # Calculate the date 1 year ago from the last data point in the database
    latest_date = dt.date(latest_year, latest_month, latest_day)
    last_year = latest_date - dt.timedelta(days=365)

     # Perform a query to retrieve the data and tobs scores
    stmt = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date <= latest_date).\
        filter(Measurement.date >= last_year).statement
    lastyrdata_df = pd.read_sql_query(stmt, session.bind)
    
    # Save the query results as a Pandas DataFrame and set the index to the date column
    lastyrdata_df = lastyrdata_df.set_index('date')

    #convert to dictionary and then jsonify the response
    res_dict = lastyrdata_df.to_dict('dict')
    return jsonify(res_dict)

# http://localhost:5000/api/v1.0/daterange?startdate=2017-01-01 or 
# http://localhost:5000/api/v1.0/daterange?startdate=2017-01-01&enddate=2017-12-31
@app.route('/api/v1.0/daterange', methods=['get'])
def dates():
 # Get date values
    startdate = request.args.get('startdate', None)
    enddate = request.args.get('enddate', None)
    if enddate  == None:
        enddate = '9999-12-31'
    # res_dict = {'startdate': startdate, 'enddate': enddate}

    sel = [func.min(Measurement.tobs).label('tMin'), 
        func.max(Measurement.tobs).label('tMax'), func.avg(Measurement.tobs).label('tAvg')]
    
    
    # Perform a query to retrieve the data and tobs scores
    result = session.query(*sel).\
        filter(Measurement.date >= startdate).\
        filter(Measurement.date <= enddate).all()

    #Convert list of tuples into normal list
    result_list = list(np.ravel(result))

    # Covert list to Dictionary
    result_dict = {"Minimum Temperature": result_list[0],
                    "Maximum Temperature": result_list[1],
                    "Average Temperature": result_list[2]}

    #sonify the response
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(debug=True)
