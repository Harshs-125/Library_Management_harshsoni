import pytest
import json
from app import Members
def test_create_member(client):
    data1={
        "name":"demo",
        "email":"demo@123"
    }
    res1=client.post('/member/add',json=data1)
    demomember_id=res1.json['member-id']
    res2=client.post('/member/add',json=data1)
    member=Members.get(demomember_id)
    member.delete(demomember_id)
    assert res1.status_code==200
    assert res2.status_code==409


def test_delete_member(client):
    demomember=Members(name="demo",email="demo@123")
    member_id=demomember.id
    res1=client.delete(f'/member/delete/{member_id}')
    assert res1.status_code==200
    res2=client.delete('/member/delete')
    assert res2.status_code==404





