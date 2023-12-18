import pytest
from qt_core.datastore import DataStore

@pytest.fixture(autouse=True)
def clearForTest():
    DataStore().clear()

def test_clear():
    rlist = DataStore().query(f"select count(*) from {DataStore().views_table}")
    assert rlist[0] == [0]

def test_query():
    DataStore().inputTestData()
    datas = DataStore().query(f"select * from {DataStore().views_table}")
    assert datas[0][1] == "作業オーダ" and datas[0][2] == "Blues"
