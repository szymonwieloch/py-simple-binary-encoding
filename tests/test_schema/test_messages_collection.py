from sbe2.schema import Message, Messages
from pytest import raises

def test_add_get():
    
    m = Messages()
    msg = Message(name="TestMessage", description='', id=5, fields=[], groups=[], datas=[], package='package')
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
    
def test_add_duplicate():
    m = Messages()
    msg = Message(name="TestMessage", description='', id=5, fields=[], groups=[], datas=[], package='package')
    m.add(msg)
    duplicate_id = Message(name="TestMessage2", description='', id=5, fields=[], groups=[], datas=[], package='package')
    with raises(ValueError):
        m.add(duplicate_id)
    duplicate_name = Message(name="TestMessage", description='', id=6, fields=[], groups=[], datas=[], package='package')
    with raises(ValueError):
        m.add(duplicate_name)
        
        
def test_get_invalid_key():
    m = Messages()
    msg = Message(name="TestMessage", description='', id=5, fields=[], groups=[], datas=[], package='package')
    m.add(msg)
    with raises(KeyError):
        _ = m[5.0]  # Invalid key type