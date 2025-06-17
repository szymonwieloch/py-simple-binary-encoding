from sbe2.schema import Message, Messages
from pytest import raises

def test_add_get():
    
    m = Messages()
    msg = Message(name="TestMessage", description='', id=5, fields=[], groups=[], datas=[])
    m.add(msg)
    assert m['TestMessage'] is msg
    assert m[5] is msg
    
    with raises(KeyError):
        _ = m['WrongName']
    with raises(KeyError):
        _ = m[8]
        
    assert m.get('TestMessage') is msg
    assert m.get(5) is msg
    assert m.get('WrongName') is None
    assert m.get(8) is None