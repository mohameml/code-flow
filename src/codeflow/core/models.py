from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import  Dict, List, Literal, Optional
from enum import Enum


# EventType = Literal["call", "line", "return", "exception"]
RunStatus = Literal["ok", "runtime_error"]

class EventType(str, Enum):
    """
    Types of execution events that can be recorded during tracing.
    
    Attributes:
        CALL: Function/method call event
        LINE: Line execution event
        RETURN: Function return event  
        EXCEPTION: Exception raised event
    """
    CALL = 'call'
    LINE = 'line'
    RETURN = 'return'
    EXCEPTION = 'exception'


@dataclass(frozen=True)
class Event:
    """
    Represents a single execution event during code tracing.
    
    An Event captures a moment in program execution, such as a function call,
    line execution, return statement, or exception. Each event is linked to
    a CallNode and contains information about the execution context.
    
    The Event class is immutable (frozen) to ensure that historical execution
    data cannot be accidentally modified after creation.
    
    Attributes:
        id: Unique identifier for this event (must be positive)
        type: Type of event (call, line, return, exception)
        node_id: ID of the CallNode this event belongs to (must be positive)
        func_name: Name of the function being executed (non-empty)
        filename: Source file where the event occurred (non-empty)
        lineno: Line number in the source file (non-negative)
        locals: Snapshot of local variables at this point as string representations
        arg: Additional event-specific context:
            - For 'return' events: the return value (repr)
            - For 'exception' events: exception info (repr)
            - For other events: None
    
    Examples:
        >>> # Creating a call event
        >>> event = Event.create_call(
        ...     event_id=1, node_id=1,
        ...     func_name='fibonacci', filename='fib.py', lineno=5,
        ...     locals_snapshot={'n': '4'}
        ... )
        >>> event.is_call()
        True
        
        >>> # Creating a return event
        >>> event = Event.create_return(
        ...     event_id=2, node_id=1,
        ...     func_name='fibonacci', filename='fib.py', lineno=7,
        ...     locals_snapshot={'n': '4'}, return_value='3'
        ... )
        >>> event.is_return()
        True
    
    Raises:
        ValueError: If validation fails during initialization
    """
    id: int
    type: EventType
    node_id: int
    func_name: str
    filename: str
    lineno: int
    locals: Dict[str, str] = field(default_factory=dict)
    arg: Optional[str] = None  

    def __post_init__(self):
        """
        Validate event data after initialization.
        
        Raises:
            ValueError: If any validation constraint is violated
        """
        if self.id <= 0:
            raise ValueError(f"Event ID must be positive, got {self.id}")
        if self.node_id <= 0:
            raise ValueError(f"Node ID must be positive, got {self.node_id}")
        if self.lineno < 0:
            raise ValueError(f"Line number must be non-negative, got {self.lineno}")
        if not self.func_name:
            raise ValueError("Function name cannot be empty")
        if not self.filename:
            raise ValueError("Filename cannot be empty")
    # ========== Factory Methods ==========
    
    @classmethod
    def create_call(
        cls, 
        event_id: int, 
        node_id: int, 
        func_name: str, 
        filename: str, 
        lineno: int, 
        locals_snapshot: Dict[str, str]
    ) -> Event:
        """
        Create a 'call' event.
        
        Args:
            event_id: Unique event identifier
            node_id: ID of the associated CallNode
            func_name: Name of the called function
            filename: Source file containing the function
            lineno: Line number where function is defined
            locals_snapshot: Local variables at call time
            
        Returns:
            New Event instance representing a function call
        """
        return cls(
            id=event_id,
            type=EventType.CALL,
            node_id=node_id,
            func_name=func_name,
            filename=filename,
            lineno=lineno,
            locals=locals_snapshot,
            arg=None
        )
    
    @classmethod
    def create_line(
        cls,
        event_id: int,
        node_id: int,
        func_name: str,
        filename: str,
        lineno: int,
        locals_snapshot: Dict[str, str]
    ) -> Event:
        """
        Create a 'line' event.
        
        Args:
            event_id: Unique event identifier
            node_id: ID of the associated CallNode
            func_name: Name of the executing function
            filename: Source file being executed
            lineno: Line number being executed
            locals_snapshot: Local variables at this line
            
        Returns:
            New Event instance representing line execution
        """
        return cls(
            id=event_id,
            type=EventType.LINE,
            node_id=node_id,
            func_name=func_name,
            filename=filename,
            lineno=lineno,
            locals=locals_snapshot,
            arg=None
        )
    
    @classmethod
    def create_return(
        cls,
        event_id: int,
        node_id: int,
        func_name: str,
        filename: str,
        lineno: int,
        locals_snapshot: Dict[str, str],
        return_value: str
    ) -> Event:
        """
        Create a 'return' event.
        
        Args:
            event_id: Unique event identifier
            node_id: ID of the associated CallNode
            func_name: Name of the returning function
            filename: Source file containing the function
            lineno: Line number of the return statement
            locals_snapshot: Local variables at return time
            return_value: String representation of the return value
            
        Returns:
            New Event instance representing a function return
        """
        return cls(
            id=event_id,
            type=EventType.RETURN,
            node_id=node_id,
            func_name=func_name,
            filename=filename,
            lineno=lineno,
            locals=locals_snapshot,
            arg=return_value
        )
    
    @classmethod
    def create_exception(
        cls,
        event_id: int,
        node_id: int,
        func_name: str,
        filename: str,
        lineno: int,
        locals_snapshot: Dict[str, str],
        exception_info: str
    ) -> Event:
        """
        Create an 'exception' event.
        
        Args:
            event_id: Unique event identifier
            node_id: ID of the associated CallNode
            func_name: Name of the function where exception occurred
            filename: Source file where exception was raised
            lineno: Line number where exception occurred
            locals_snapshot: Local variables when exception occurred
            exception_info: String representation of exception (type and message)
            
        Returns:
            New Event instance representing an exception
        """
        return cls(
            id=event_id,
            type=EventType.EXCEPTION,
            node_id=node_id,
            func_name=func_name,
            filename=filename,
            lineno=lineno,
            locals=locals_snapshot,
            arg=exception_info
        )
    
    # ========== Query Methods ==========
    
    def is_call(self) -> bool:
        """Check if this is a call event."""
        return self.type == EventType.CALL
    
    def is_line(self) -> bool:
        """Check if this is a line event."""
        return self.type == EventType.LINE
    
    def is_return(self) -> bool:
        """Check if this is a return event."""
        return self.type == EventType.RETURN
    
    def is_exception(self) -> bool:
        """Check if this is an exception event."""
        return self.type == EventType.EXCEPTION
    
    def get_return_value(self) -> Optional[str]:
        """
        Get the return value if this is a return event.
        
        Returns:
            Return value string representation, or None if not a return event
        """
        return self.arg if self.is_return() else None
    
    def get_exception_info(self) -> Optional[str]:
        """
        Get the exception info if this is an exception event.
        
        Returns:
            Exception info string, or None if not an exception event
        """
        return self.arg if self.is_exception() else None
    
    # ========== Serialization Methods ==========
    
    def to_dict(self) -> dict:
        """
        Convert event to dictionary for serialization.
        
        Returns:
            Dictionary representation suitable for JSON serialization
            
        Example:
            >>> event = Event.create_call(1, 1, 'func', 'file.py', 5, {'x': '10'})
            >>> event.to_dict()
            {'id': 1, 'type': 'call', 'node_id': 1, ...}
        """
        return {
            'id': self.id,
            'type': self.type.value,  # Convert Enum to string
            'node_id': self.node_id,
            'func_name': self.func_name,
            'filename': self.filename,
            'lineno': self.lineno,
            'locals': self.locals,
            'arg': self.arg
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Event:
        """
        Create Event from dictionary.
        
        Args:
            data: Dictionary with event data
            
        Returns:
            Event instance
            
        Raises:
            KeyError: If required fields are missing
            ValueError: If data is invalid (caught by __post_init__)
            
        Example:
            >>> data = {'id': 1, 'type': 'call', 'node_id': 1, ...}
            >>> event = Event.from_dict(data)
        """
        return cls(
            id=data['id'],
            type=EventType(data['type']),  # Convert string to Enum
            node_id=data['node_id'],
            func_name=data['func_name'],
            filename=data['filename'],
            lineno=data['lineno'],
            locals=data.get('locals', {}),
            arg=data.get('arg')
        )
    
    # ========== String Representation ==========
    
    def __str__(self) -> str:
        """
        Human-readable string representation.
        
        Returns:
            Concise string describing the event
            
        Example:
            "Event#1[call] fibonacci:5"
            "Event#2[return] fibonacci:7 -> 3"
        """
        arg_str = f" -> {self.arg}" if self.arg else ""
        return (
            f"Event#{self.id}[{self.type.value}] "
            f"{self.func_name}:{self.lineno}{arg_str}"
        )





@dataclass
class CallNode:
    id: int
    func_name: str
    filename: str
    call_event_id: int
    args: Dict[str, str] = field(default_factory=dict)

    return_event_id: Optional[int] = None
    return_value: Optional[str] = None
    exception: Optional[str] = None


@dataclass
class CallEdge:
    parent_id: int
    child_id: int


@dataclass
class RunResult:
    status: RunStatus
    events: List[Event]
    nodes: List[CallNode]
    edges: List[CallEdge]
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "error": self.error,
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
            "events": [asdict(ev) for ev in self.events],
        }



