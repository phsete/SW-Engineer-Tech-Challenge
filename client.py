import asyncio
import time
from pydicom import Dataset
from scp import ModalityStoreSCP
import requests
import models
from typing import Dict


class SeriesCollector:
    """A Series Collector is used to build up a list of instances (a DICOM series) as they are received by the modality.
    It stores the (during collection incomplete) series, the Series (Instance) UID, the time the series was last updated
    with a new instance and the information whether the dispatch of the series was started.
    """
    def __init__(self, first_dataset: Dataset) -> None:
        """Initialization of the Series Collector with the first dataset (instance).

        Args:
            first_dataset (Dataset): The first dataset or the regarding series received from the modality.
        """
        self.series_instance_uid = first_dataset.SeriesInstanceUID
        self.series: list[Dataset] = [first_dataset]
        self.last_update_time = time.time()
        self.dispatch_started = False

    def add_instance(self, dataset: Dataset) -> bool:
        """Add an dataset to the series collected by this Series Collector if it has the correct Series UID.

        Args:
            dataset (Dataset): The dataset to add.

        Returns:
            bool: `True`, if the Series UID of the dataset to add matched and the dataset was therefore added, `False` otherwise.
        """
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.series.append(dataset)
            self.last_update_time = time.time()
            return True

        return False


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming series (hint: there is no attribute indicating how
    many instances are in a series, so you have to wait for some time to find out if a new instance is transmitted).
    For simplyfication, you can assume that only one series is transmitted at a time.
    You can use the given template, but you don't have to!
    """

    def __init__(self) -> None:
        """Initialize the Series Dispatcher.
        """

        self.loop: asyncio.AbstractEventLoop
        self.queue = asyncio.Queue()
        self.modality_scp: ModalityStoreSCP
        self.series_collector: Dict[str, SeriesCollector] = {}

    async def main(self) -> None:
        """An infinitely running method used as hook for the asyncio event loop.
        Keeps the event loop alive whether or not datasets are received from the modality and prints a message
        regulary when no datasets are received.
        """
        self.modality_scp = ModalityStoreSCP(self.loop, self.queue)

        while True:
            # TODO: Regulary check if new datasets are received and act if they are.
            # Information about Python asyncio: https://docs.python.org/3/library/asyncio.html
            # When datasets are received you should collect and process them
            # (e.g. using `asyncio.create_task(self.run_series_collector()`)

            dataset: Dataset = await self.queue.get()
            self.loop.create_task(self.run_series_collectors(dataset))

    async def run_series_collectors(self, dataset: Dataset) -> None:
        """Runs the collection of datasets, which results in the Series Collector being filled.
        """
        # TODO: Get the data from the SCP and start dispatching

        uid = dataset.SeriesInstanceUID
        if uid in self.series_collector:
            self.series_collector[uid].add_instance(dataset)
        else:
            self.series_collector[uid] = SeriesCollector(dataset)
            self.loop.create_task(self.dispatch_series_collector(uid))

    async def dispatch_series_collector(self, uid) -> None:
        """Tries to dispatch a Series Collector, i.e. to finish it's dataset collection and scheduling of further
        methods to extract the desired information.
        """
        # Check if the series collector hasn't had an update for a long enough timespan and send the series to the
        # server if it is complete
        # NOTE: This is the last given function, you should create more for extracting the information and
        # sending the data to the server
        maximum_wait_time = 1

        while self.series_collector[uid].last_update_time + maximum_wait_time > time.time():
            await asyncio.sleep(0.2)
        print("started dispatch")
        self.series_collector[uid].dispatch_started = True
        self.dispatch_to_server(uid)
        self.series_collector.pop(uid)

    def extract_data(self, uid) -> models.Series:
        initial_dataset = self.series_collector[uid].series[0]
        series = models.Series(
            SeriesInstanceUID = self.series_collector[uid].series_instance_uid,
            PatientName = str(initial_dataset.PatientName),
            PatientID = initial_dataset.PatientID,
            StudyInstanceUID = initial_dataset.StudyInstanceUID,
            InstancesInSeries = len(self.series_collector[uid].series))
        return series

    def dispatch_to_server(self, uid) -> None:
        series = self.extract_data(uid)
        print("dispatched data", series.SeriesInstanceUID)
        response = requests.post("http://localhost:8000/series", json=series.model_dump())
        print("API responded with code", response.status_code, "and body", response.text)


if __name__ == "__main__":
    """Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    engine = SeriesDispatcher()
    engine.loop = asyncio.get_event_loop()
    engine.loop.run_until_complete(engine.main())
