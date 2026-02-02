from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import  Dict, List, Literal, Optional



EventType = Literal["call", "line", "return", "exception"]
RunStatus = Literal["ok", "runtime_error"]


@dataclass
class Event:
    id: int
    type: EventType
    node_id: int
    func_name: str
    filename: str
    lineno: int
    locals: Dict[str, str] = field(default_factory=dict)
    arg: Optional[str] = None  # return value repr OR exception info repr


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






