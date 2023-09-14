# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
recent = dt.datetime(2017,8,23)
end = recent - dt.timedelta(days=365.25)

@app.route("/")
def index():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precip():
    precipdata = session.query(measurement.date, measurement.prcp).filter(measurement.date <= recent).filter(measurement.date > end).order_by(measurement.date).all()
    session.close()
    return(jsonify(dict(precipdata)))

@app.route('/api/v1.0/stations')
def stationlist():
    stations = session.query(measurement.station).distinct().all()
    stations = [station for station, in stations]
    session.close()
    return(jsonify(stations))

@app.route('/api/v1.0/tobs')
def tobs():
    tempdata = session.query(measurement.date, measurement.tobs).filter(measurement.date <= recent).filter(measurement.date > end).filter(measurement.station=='USC00519281').all()
    session.close()
    return(jsonify(dict(tempdata)))

@app.route('/api/v1.0/<start>')
def starter(start):
    min = session.query(func.min(measurement.tobs)).filter(measurement.date >=recent).all()
    avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >=recent).all()
    max = session.query(func.max(measurement.tobs)).filter(measurement.date >=recent).all()
    session.close()
    temps = {'min':min,
              'avg':avg,
              'max':max}
    return(jsonify(temps))

@app.route('/api/v1.0/<start>/<end>')
def end():
    min = session.query(func.min(measurement.tobs)).filter(measurement.date >=recent).filter(measurement.date <=end).all()
    avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >=recent).filter(measurement.date <=end).all()
    max = session.query(func.max(measurement.tobs)).filter(measurement.date >=recent).filter(measurement.date <=end).all()
    session.close()
    temps = {'min':min,
              'avg':avg,
              'max':max}    
    return(jsonify(temps))
#################################################

if __name__ == "__main__":
    app.run(debug=True)

