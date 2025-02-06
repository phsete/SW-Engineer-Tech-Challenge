from fastapi import FastAPI, status, Response
import sqlite3
import models

app = FastAPI()

def connect_to_db(name = "series_data.db") -> sqlite3.Connection:
   return sqlite3.connect(name)

def init_db():
    con = connect_to_db()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS series_data(SeriesInstanceUID TEXT PRIMARY KEY, PatientName TEXT, PatientID INT, StudyInstanceUID TEXT, InstancesInSeries INT)")
    con.commit()
    return con, cur

@app.post("/series", status_code=status.HTTP_201_CREATED)
def add_series(series: models.Series, response: Response):
    con, cur = init_db()
    data = tuple(series.model_dump().values())
    try:
        cur.execute("INSERT INTO series_data VALUES(?, ?, ?, ?, ?)", data)
        con.commit()
    except sqlite3.Error:
        print("Could not insert data into DB")
        response.status_code = status.HTTP_403_FORBIDDEN
        return {}
        
    print("Inserted into DB:", data)
    con.close()
    return series.model_dump()