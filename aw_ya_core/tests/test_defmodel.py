import pytest
from qt_core.defmodel import AnalysisDefinition,AnalysisViewDefinition,CategoryDefinition
from qt_core.datastore import DataStore 

@pytest.fixture(scope='module')
def dataInput():
    DataStore().inputTestData()

def test_loadData():
    ad = AnalysisDefinition()
    ad.loadData()
    assert len(ad.views) == 2
    

    