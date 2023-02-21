import pytest
import json
import requests

def test_add_books(client):
    # res= client.post('/book/add',json={
    #     "genre":"fiction"
    # })
    #assert res.status_code==400
    res2=client.post('/book/add',json={
        "genre":""
    })
    assert res2.status_code==400
    res3=client.post('/book/add',json={
        "genre":"1"
    })
    assert res3.status_code==400
    res4=client.post('/book/add',json={
        "genre":"dededededd"
    })
    assert res4.status_code==400

