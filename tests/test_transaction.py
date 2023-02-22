
import pytest
import json
from app import Transactions

def test_viewrecord(client):
    transactions=Transactions(book_id=1,member_id=1)
    transactions_id=transactions.id
    res1=client.get(f'transaction/viewrecord/{transactions_id}')
    assert res1.status_code==200
    transactions.delete(transactions_id)
    res2=client.get(f'transaction/viewrecord/{transactions_id}')
    assert res2.status_code==404
