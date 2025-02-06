from fastapi import FastAPI, status
import sqlite3
import models

app = FastAPI()

def init_db():
    con = sqlite3.connect("series_data.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS series_data(SeriesInstanceUID, PatientName, PatientID, StudyInstanceUID, InstancesInSeries)")
    return con, cur

@app.post("/series", status_code=status.HTTP_201_CREATED)
def add_series(series: models.Series):
    con, cur = init_db()
    data = tuple(series.model_dump().values())
    try:
        cur.execute("INSERT INTO series_data VALUES(?, ?, ?, ?, ?)", data)
        con.commit()
    except sqlite3.Error:
        print("Could not insert data into DB")
        return 
        
    print("Inserted into DB:", data)
    con.close()
    return series.model_dump()