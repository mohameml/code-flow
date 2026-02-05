"""
Comprehensive unit tests for the improved Event class.

Run with: pytest test_event_improved.py -v
"""
import pytest
from codeflow.core.models import Event, EventType


class TestEventCreation:
    """Test Event creation and validation."""
    
    def test_create_valid_call_event(self):
        """Test creating a valid call event."""
        event = Event(
            id=1,
            type=EventType.CALL,
            node_id=1,
            func_name='test_func',
            filename='test.py',
            lineno=10,
            locals={'x': '5'},
            arg=None
        )
        assert event.id == 1
        assert event.type == EventType.CALL
        assert event.node_id == 1
        assert event.func_name == 'test_func'
        assert event.filename == 'test.py'
        assert event.lineno == 10
        assert event.locals == {'x': '5'}
        assert event.arg is None
    
    def test_create_with_defaults(self):
        """Test creating event with default values."""
        event = Event(
            id=1,
            type=EventType.LINE,
            node_id=2,
            func_name='func',
            filename='file.py',
            lineno=5
        )
        assert event.locals == {}
        assert event.arg is None
    
    def test_validation_negative_event_id(self):
        """Test that negative event ID raises ValueError."""
        with pytest.raises(ValueError, match="Event ID must be positive"):
            Event(
                id=-1,
                type=EventType.CALL,
                node_id=1,
                func_name='test',
                filename='test.py',
                lineno=1
            )
    
    def test_validation_zero_event_id(self):
        """Test that zero event ID raises ValueError."""
        with pytest.raises(ValueError, match="Event ID must be positive"):
            Event(
                id=0,
                type=EventType.CALL,
                node_id=1,
                func_name='test',
                filename='test.py',
                lineno=1
            )
    
    def test_validation_negative_node_id(self):
        """Test that negative node ID raises ValueError."""
        with pytest.raises(ValueError, match="Node ID must be positive"):
            Event(
                id=1,
                type=EventType.CALL,
                node_id=-5,
                func_name='test',
                filename='test.py',
                lineno=1
            )
    
    def test_validation_negative_lineno(self):
        """Test that negative line number raises ValueError."""
        with pytest.raises(ValueError, match="Line number must be non-negative"):
            Event(
                id=1,
                type=EventType.CALL,
                node_id=1,
                func_name='test',
                filename='test.py',
                lineno=-1
            )
    
    def test_validation_empty_func_name(self):
        """Test that empty function name raises ValueError."""
        with pytest.raises(ValueError, match="Function name cannot be empty"):
            Event(
                id=1,
                type=EventType.CALL,
                node_id=1,
                func_name='',
                filename='test.py',
                lineno=1
            )
    
    def test_validation_empty_filename(self):
        """Test that empty filename raises ValueError."""
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            Event(
                id=1,
                type=EventType.CALL,
                node_id=1,
                func_name='test',
                filename='',
                lineno=1
            )


class TestFactoryMethods:
    """Test Event factory methods."""
    
    def test_create_call_factory(self):
        """Test create_call factory method."""
        event = Event.create_call(
            event_id=1,
            node_id=2,
            func_name='my_func',
            filename='module.py',
            lineno=42,
            locals_snapshot={'a': '1', 'b': '2'}
        )
        
        assert event.id == 1
        assert event.type == EventType.CALL
        assert event.node_id == 2
        assert event.func_name == 'my_func'
        assert event.filename == 'module.py'
        assert event.lineno == 42
        assert event.locals == {'a': '1', 'b': '2'}
        assert event.arg is None
    
    def test_create_line_factory(self):
        """Test create_line factory method."""
        event = Event.create_line(
            event_id=5,
            node_id=3,
            func_name='process',
            filename='app.py',
            lineno=100,
            locals_snapshot={'x': '10'}
        )
        
        assert event.type == EventType.LINE
        assert event.arg is None
    
    def test_create_return_factory(self):
        """Test create_return factory method."""
        event = Event.create_return(
            event_id=10,
            node_id=4,
            func_name='calculate',
            filename='math.py',
            lineno=50,
            locals_snapshot={'result': '42'},
            return_value='42'
        )
        
        assert event.type == EventType.RETURN
        assert event.arg == '42'
    
    def test_create_exception_factory(self):
        """Test create_exception factory method."""
        event = Event.create_exception(
            event_id=15,
            node_id=5,
            func_name='risky_func',
            filename='dangerous.py',
            lineno=99,
            locals_snapshot={'data': 'None'},
            exception_info='ValueError: invalid input'
        )
        
        assert event.type == EventType.EXCEPTION
        assert event.arg == 'ValueError: invalid input'


class TestQueryMethods:
    """Test Event query/predicate methods."""
    
    def test_is_call(self):
        """Test is_call() method."""
        call_event = Event.create_call(1, 1, 'f', 'file.py', 1, {})
        line_event = Event.create_line(2, 1, 'f', 'file.py', 2, {})
        
        assert call_event.is_call() is True
        assert line_event.is_call() is False
    
    def test_is_line(self):
        """Test is_line() method."""
        line_event = Event.create_line(1, 1, 'f', 'file.py', 5, {})
        return_event = Event.create_return(2, 1, 'f', 'file.py', 10, {}, '5')
        
        assert line_event.is_line() is True
        assert return_event.is_line() is False
    
    def test_is_return(self):
        """Test is_return() method."""
        return_event = Event.create_return(1, 1, 'f', 'file.py', 10, {}, 'result')
        exception_event = Event.create_exception(2, 1, 'f', 'file.py', 15, {}, 'Error')
        
        assert return_event.is_return() is True
        assert exception_event.is_return() is False
    
    def test_is_exception(self):
        """Test is_exception() method."""
        exception_event = Event.create_exception(1, 1, 'f', 'file.py', 5, {}, 'Error')
        call_event = Event.create_call(2, 2, 'g', 'file.py', 10, {})
        
        assert exception_event.is_exception() is True
        assert call_event.is_exception() is False
    
    def test_get_return_value_on_return_event(self):
        """Test get_return_value() on return event."""
        event = Event.create_return(1, 1, 'f', 'file.py', 5, {}, '42')
        assert event.get_return_value() == '42'
    
    def test_get_return_value_on_non_return_event(self):
        """Test get_return_value() on non-return event."""
        event = Event.create_call(1, 1, 'f', 'file.py', 5, {})
        assert event.get_return_value() is None
    
    def test_get_exception_info_on_exception_event(self):
        """Test get_exception_info() on exception event."""
        event = Event.create_exception(1, 1, 'f', 'file.py', 5, {}, 'TypeError: bad')
        assert event.get_exception_info() == 'TypeError: bad'
    
    def test_get_exception_info_on_non_exception_event(self):
        """Test get_exception_info() on non-exception event."""
        event = Event.create_line(1, 1, 'f', 'file.py', 5, {})
        assert event.get_exception_info() is None


class TestSerialization:
    """Test Event serialization (to_dict/from_dict)."""
    
    def test_to_dict_call_event(self):
        """Test to_dict() on call event."""
        event = Event.create_call(1, 2, 'func', 'file.py', 10, {'x': '5'})
        data = event.to_dict()
        
        assert data == {
            'id': 1,
            'type': 'call',
            'node_id': 2,
            'func_name': 'func',
            'filename': 'file.py',
            'lineno': 10,
            'locals': {'x': '5'},
            'arg': None
        }
    
    def test_to_dict_return_event(self):
        """Test to_dict() on return event."""
        event = Event.create_return(5, 3, 'calc', 'math.py', 20, {'res': '100'}, '100')
        data = event.to_dict()
        
        assert data['type'] == 'return'
        assert data['arg'] == '100'
    
    def test_from_dict_call_event(self):
        """Test from_dict() creating call event."""
        data = {
            'id': 1,
            'type': 'call',
            'node_id': 2,
            'func_name': 'test',
            'filename': 'test.py',
            'lineno': 5,
            'locals': {'a': '1'},
            'arg': None
        }
        event = Event.from_dict(data)
        
        assert event.id == 1
        assert event.type == EventType.CALL
        assert event.node_id == 2
        assert event.func_name == 'test'
        assert event.locals == {'a': '1'}
        assert event.arg is None
    
    def test_from_dict_with_missing_optional_fields(self):
        """Test from_dict() with missing locals and arg."""
        data = {
            'id': 1,
            'type': 'line',
            'node_id': 1,
            'func_name': 'f',
            'filename': 'f.py',
            'lineno': 1
        }
        event = Event.from_dict(data)
        
        assert event.locals == {}
        assert event.arg is None
    
    def test_serialization_roundtrip_call(self):
        """Test that to_dict() and from_dict() are inverses for call event."""
        original = Event.create_call(10, 5, 'process', 'app.py', 100, {'data': '[1,2,3]'})
        data = original.to_dict()
        restored = Event.from_dict(data)
        
        assert restored == original
    
    def test_serialization_roundtrip_return(self):
        """Test that to_dict() and from_dict() are inverses for return event."""
        original = Event.create_return(20, 10, 'compute', 'calc.py', 50, {'x': '42'}, '84')
        data = original.to_dict()
        restored = Event.from_dict(data)
        
        assert restored == original
    
    def test_serialization_roundtrip_exception(self):
        """Test that to_dict() and from_dict() are inverses for exception event."""
        original = Event.create_exception(
            30, 15, 'fail', 'error.py', 99, {'msg': 'oops'}, 'RuntimeError: oops'
        )
        data = original.to_dict()
        restored = Event.from_dict(data)
        
        assert restored == original
    
    def test_from_dict_invalid_type_raises_error(self):
        """Test that invalid event type raises ValueError."""
        data = {
            'id': 1,
            'type': 'invalid_type',  # Invalid
            'node_id': 1,
            'func_name': 'f',
            'filename': 'f.py',
            'lineno': 1
        }
        with pytest.raises(ValueError):
            Event.from_dict(data)


class TestImmutability:
    """Test that Event is immutable (frozen)."""
    
    def test_cannot_modify_id(self):
        """Test that Event.id cannot be modified."""
        event = Event.create_call(1, 1, 'f', 'file.py', 1, {})
        
        with pytest.raises(AttributeError):
            event.id = 999 # type: ignore
    
    def test_cannot_modify_type(self):
        """Test that Event.type cannot be modified."""
        event = Event.create_call(1, 1, 'f', 'file.py', 1, {})
        
        with pytest.raises(AttributeError):
            event.type = EventType.RETURN # type: ignore
    
    def test_cannot_modify_func_name(self):
        """Test that Event.func_name cannot be modified."""
        event = Event.create_call(1, 1, 'f', 'file.py', 1, {})
        
        with pytest.raises(AttributeError):
            event.func_name = 'hacked' # type: ignore


class TestStringRepresentation:
    """Test Event string representations."""
    
    def test_str_call_event(self):
        """Test __str__() on call event."""
        event = Event.create_call(1, 1, 'fibonacci', 'fib.py', 5, {})
        result = str(event)
        
        assert 'Event#1' in result
        assert '[call]' in result
        assert 'fibonacci:5' in result
    
    def test_str_return_event_with_value(self):
        """Test __str__() on return event with value."""
        event = Event.create_return(2, 1, 'add', 'math.py', 10, {}, '42')
        result = str(event)
        
        assert 'Event#2' in result
        assert '[return]' in result
        assert 'add:10' in result
        assert '-> 42' in result
    
    def test_str_exception_event(self):
        """Test __str__() on exception event."""
        event = Event.create_exception(3, 1, 'divide', 'ops.py', 20, {}, 'ZeroDivisionError')
        result = str(event)
        
        assert 'Event#3' in result
        assert '[exception]' in result
        assert '-> ZeroDivisionError' in result


class TestEquality:
    """Test Event equality comparisons."""
    
    def test_equal_events(self):
        """Test that identical events are equal."""
        event1 = Event.create_call(1, 1, 'f', 'file.py', 5, {'x': '10'})
        event2 = Event.create_call(1, 1, 'f', 'file.py', 5, {'x': '10'})
        
        assert event1 == event2
    
    def test_unequal_events_different_id(self):
        """Test that events with different IDs are not equal."""
        event1 = Event.create_call(1, 1, 'f', 'file.py', 5, {})
        event2 = Event.create_call(2, 1, 'f', 'file.py', 5, {})
        
        assert event1 != event2
    
    def test_unequal_events_different_type(self):
        """Test that events with different types are not equal."""
        event1 = Event.create_call(1, 1, 'f', 'file.py', 5, {})
        event2 = Event.create_line(1, 1, 'f', 'file.py', 5, {})
        
        assert event1 != event2


class TestEventTypeEnum:
    """Test EventType enum."""
    
    def test_event_type_values(self):
        """Test EventType enum values."""
        assert EventType.CALL.value == 'call'
        assert EventType.LINE.value == 'line'
        assert EventType.RETURN.value == 'return'
        assert EventType.EXCEPTION.value == 'exception'
    
    def test_event_type_from_string(self):
        """Test creating EventType from string."""
        assert EventType('call') == EventType.CALL
        assert EventType('return') == EventType.RETURN
    
    def test_event_type_invalid_string_raises_error(self):
        """Test that invalid string raises ValueError."""
        with pytest.raises(ValueError):
            EventType('invalid')


# ========== Integration Tests ==========

class TestEventIntegration:
    """Integration tests simulating real usage."""
    
    def test_trace_fibonacci_simulation(self):
        """Simulate tracing fibonacci(2) execution."""
        events = []
        
        # Module call
        events.append(Event.create_call(1, 1, '<module>', 'fib.py', 1, {}))
        
        # First fib(2) call
        events.append(Event.create_call(2, 2, 'fib', 'fib.py', 1, {'n': '2'}))
        events.append(Event.create_line(3, 2, 'fib', 'fib.py', 2, {'n': '2'}))
        events.append(Event.create_line(4, 2, 'fib', 'fib.py', 4, {'n': '2'}))
        
        # Recursive call fib(1)
        events.append(Event.create_call(5, 3, 'fib', 'fib.py', 1, {'n': '1'}))
        events.append(Event.create_line(6, 3, 'fib', 'fib.py', 2, {'n': '1'}))
        events.append(Event.create_line(7, 3, 'fib', 'fib.py', 3, {'n': '1'}))
        events.append(Event.create_return(8, 3, 'fib', 'fib.py', 3, {'n': '1'}, '1'))
        
        # Recursive call fib(0)
        events.append(Event.create_call(9, 4, 'fib', 'fib.py', 1, {'n': '0'}))
        events.append(Event.create_line(10, 4, 'fib', 'fib.py', 2, {'n': '0'}))
        events.append(Event.create_line(11, 4, 'fib', 'fib.py', 3, {'n': '0'}))
        events.append(Event.create_return(12, 4, 'fib', 'fib.py', 3, {'n': '0'}, '0'))
        
        # Return from fib(2)
        events.append(Event.create_return(13, 2, 'fib', 'fib.py', 4, {'n': '2'}, '1'))
        
        # Verify structure
        assert len(events) == 13
        assert events[0].is_call()
        assert events[-1].is_return()
        
        # Verify all events are valid
        for event in events:
            assert event.id > 0
            assert event.node_id > 0
            assert event.func_name
            assert event.filename
        
        # Serialize all events
        serialized = [e.to_dict() for e in events]
        assert len(serialized) == 13
        
        # Deserialize and verify
        restored = [Event.from_dict(d) for d in serialized]
        assert restored == events


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])