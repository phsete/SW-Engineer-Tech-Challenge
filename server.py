from fastapi import FastAPI
import sqlite3
import models

app = FastAPI()

def init_db():
    con = sqlite3.connect("series_data.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS series_data(SeriesInstanceUID, PatientName, PatientID, StudyInstanceUID, InstancesInSeries)")
    return con, cur

@app.post("/series")
def add_series(series: models.Series):
    con, cur = init_db()
    data = tuple(series.model_dump().values())
    print(data)
    cur.execute("INSERT INTO series_data VALUES(?, ?, ?, ?, ?)", data)
    con.commit()
    con.close()
    print("inserted data into db")
    # TODO: check if insert was successfull and return status code and body