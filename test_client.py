from pydicom import Dataset
import pytest
import client
from unittest.mock import patch, MagicMock
import asyncio
import models

@pytest.fixture
def mock_dataset():
    """Create a mock dataset for testing."""
    dataset = Dataset()
    dataset.SeriesInstanceUID = "1.23.456.7890"
    dataset.PatientName = "Firstname^Lastname"
    dataset.PatientID = "42"
    dataset.StudyInstanceUID = "0.98.765.4321"
    return dataset

@pytest.fixture
def collector(mock_dataset):
    return client.SeriesCollector(mock_dataset)

def test_initial_collection(collector: client.SeriesCollector, mock_dataset: Dataset):
    """Test if a new Series Collector is correctly created when the initial dataset is submitted"""
    assert collector.series_instance_uid == mock_dataset.SeriesInstanceUID
    assert len(collector.series) == 1
    assert collector.series == [mock_dataset]

def test_add_instance_collection(collector: client.SeriesCollector, mock_dataset: Dataset):
    """Test if a Series Collector is reused when a new dataset is submitted"""
    collector.add_instance(mock_dataset)

    assert collector.series_instance_uid == mock_dataset.SeriesInstanceUID
    assert len(collector.series) == 2
    assert collector.series == [mock_dataset, mock_dataset]

@pytest.mark.asyncio
async def test_runs_in_a_loop():
    assert asyncio.get_running_loop()

@pytest.fixture
def dispatcher():
    dispatcher = client.SeriesDispatcher()
    return dispatcher

@pytest.mark.asyncio
@patch('requests.post')
async def test_dispatch_to_server(mock_post: MagicMock, dispatcher: client.SeriesDispatcher, mock_dataset: Dataset):
    """Test if the dispatcher calls the API correctly"""
    series = models.Series(
        SeriesInstanceUID = "1.23.456.7890",
        PatientName = "Firstname^Lastname",
        PatientID = 42,
        StudyInstanceUID = "0.98.765.4321",
        InstancesInSeries = 1
    )
    mock_response = mock_post.return_value
    mock_response.status_code = 201 # Created
    mock_response.json.return_value = series.model_dump()

    dispatcher.loop = asyncio.get_running_loop()
    series_collector_task = dispatcher.loop.create_task(dispatcher.run_series_collectors(mock_dataset))
    dispatcher_task: asyncio.Task = await series_collector_task
    result: asyncio.Task = await dispatcher_task
    
    mock_post.assert_called_with("http://localhost:8000/series", json=series.model_dump())