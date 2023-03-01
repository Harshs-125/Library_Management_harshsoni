import pytest

def test_app(client):
    res=client.get('/')
    assert res.status_code==200