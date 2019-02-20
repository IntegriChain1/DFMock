import pytest
import pandas as pd
from dfmock.dfmock import DFMock

def test_mock_datetime_simple():
    mock = DFMock()
    
    stamps = mock._mock_datetime(count=1)
    
    assert len(stamps) == 1
    assert isinstance(stamps[0], pd.Timestamp)

def test_mock_string():
    pass

def test_mock_integer():
    pass

def test_mock_float():
    pass

def test_mock_bool():
    pass

def test_mock_category():
    pass

def test_mock_timedelta():
    pass
