import pytest
import json
from app import Members
def test_create_member(client):
    data1={
        "name":"Harsh Soni",
        "email":"harsh@123"
    }
    data2={
        "name":"Palak Soni",
        "email":"palak@123"
    }
    res1=client.post('/member/add',json=data1)
    res2=client.post('/member/add',json=data2)
    member=Members.selectBy(email="palak@123")
    Members.delete(member[0].id)
    assert res1.status_code==409
    assert res2.status_code==200

def test_delete_member(client):
    demomember=Members(name="demo",email="demo@123")
    member_id=demomember.id
    res1=client.delete(f'/member/delete/{member_id}')
    assert res1.status_code==200
    res2=client.delete('/member/delete')
    assert res2.status_code==404





