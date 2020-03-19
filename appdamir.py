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

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first().date
    past12mth_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= past12mth_date).\
        group_by(Measurement.date).all()  

    temp_dict = [{element[0]:element[1]} for element in tobs_results]
        
    return  jsonify(temp_dict) 

@app.route("/api/v1.0/stations")
def stations():
    station_nm = session.query(Station.station,Station.name).all()
    return jsonify(station_nm)    


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):
    temp_results = session.query(func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all() 
    return jsonify(temp_results)
     
                                    
if __name__ == '__main__':
    app.run(debug=True)    