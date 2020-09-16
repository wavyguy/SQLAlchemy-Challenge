#!/usr/bin/env python
# coding: utf-8

# In[3]:


#####################
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an Existing Database into a New Model
Base = automap_base()

# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create Session
Session = Session(engine)


# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Home page<br/>"
        f"List Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (YYYY-MM-DD)<br/>"
        f"/api/v1.0/start (YYYY-MM-DD) / end (YYYY-MM-DD)<br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    past_year ='2016-08-23'
    prcp_twelve_months = Session.query(Measurement.date, Measurement.prcp).        filter(Measurement.date >= past_year).    order_by(Measurement.date).all()

    prcp_dict = {}
    for tuple_ in prcp_twelve_months:
        prcp_dict[tuple_[0]]=tuple_[1]
    Session.close()
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    station_list = Session.query(Station.station).    order_by(Station.station).all()

    station_loop=[]
    for tuple_ in station_list:
        station_loop.append(tuple_[0])

    return jsonify(station_loop)


@app.route("/api/v1.0/tobs")
def tobs():
    last_year = Session.query(Measurement.date,Measurement.tobs).    filter(Measurement.date >="2016-08-23").    filter("USC00519281"==Measurement.station).all()

    temp =[]
    for tuple_ in last_year:
        temp.append(tuple_[1])

    Session.close()
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def given_start(start,end=None):
    if end==None:
        start_func = Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).            filter(Measurement.date >= start).all()[0]
    else:
        start_func = Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).            filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]
    start_dict = {
        "Min":start_func[0],
        "Avg":start_func[1],
        "Max":start_func[2],
    }

  
    Session.close()
    return jsonify(start_dict)

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




