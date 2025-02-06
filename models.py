from pydantic import BaseModel

class Series(BaseModel):
    SeriesInstanceUID: str
    PatientName: str
    PatientID: int
    StudyInstanceUID: str
    InstancesInSeries: int