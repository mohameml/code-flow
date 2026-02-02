from typing import Dict, List

from codeflow.core.models import CallEdge, CallNode, Event
from codeflow.core.safe_repr import SafeRepr


class TraceRecorder:
    """
    Enregistre events + call tree en traçant uniquement le fichier utilisateur.
    """
    def __init__(self, user_filename: str, safe_repr: SafeRepr):
        self.user_filename = user_filename
        self.safe_repr = safe_repr

        self.events: List[Event] = []
        self.nodes: List[CallNode] = []
        self.edges: List[CallEdge] = []

        self._event_id = 0
        self._node_id = 0
        self._call_stack: List[int] = []

    def _next_event_id(self) -> int:
        self._event_id += 1
        return self._event_id

    def _next_node_id(self) -> int:
        self._node_id += 1
        return self._node_id

    def _in_user_code(self, frame) -> bool:
        return frame.f_code.co_filename == self.user_filename

    def _snapshot_locals(self, frame) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for k, v in frame.f_locals.items():
            out[k] = self.safe_repr(v)
        return out

    def _set_node_return(self, node_id: int, event_id: int, ret_repr: str) -> None:
        for n in self.nodes:
            if n.id == node_id:
                n.return_event_id = event_id
                n.return_value = ret_repr
                return

    def _set_node_exception(self, node_id: int, exc_repr: str) -> None:
        for n in self.nodes:
            if n.id == node_id:
                n.exception = exc_repr
                return

    def trace(self, frame, event: str, arg):
        # Important: retourner self.trace pour continuer à tracer.
        if not self._in_user_code(frame):
            return self.trace

        func_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        if event == "call":
            node_id = self._next_node_id()

            if self._call_stack:
                self.edges.append(CallEdge(parent_id=self._call_stack[-1], child_id=node_id))

            eid = self._next_event_id()
            call_locals = self._snapshot_locals(frame)
            self.events.append(Event(
                id=eid, type="call", node_id=node_id,
                func_name=func_name, filename=filename, lineno=lineno,
                locals=call_locals, arg=None
            ))

            self.nodes.append(CallNode(
                id=node_id, func_name=func_name, filename=filename,
                call_event_id=eid, args=call_locals
            ))

            self._call_stack.append(node_id)
            return self.trace

        # line/return/exception doivent avoir un node courant
        if not self._call_stack:
            return self.trace

        node_id = self._call_stack[-1]

        if event == "line":
            eid = self._next_event_id()
            self.events.append(Event(
                id=eid, type="line", node_id=node_id,
                func_name=func_name, filename=filename, lineno=lineno,
                locals=self._snapshot_locals(frame), arg=None
            ))
            return self.trace

        if event == "return":
            eid = self._next_event_id()
            ret_repr = self.safe_repr(arg)
            self.events.append(Event(
                id=eid, type="return", node_id=node_id,
                func_name=func_name, filename=filename, lineno=lineno,
                locals=self._snapshot_locals(frame), arg=ret_repr
            ))
            self._set_node_return(node_id, eid, ret_repr)
            self._call_stack.pop()
            return self.trace

        if event == "exception":
            eid = self._next_event_id()
            exc_type, exc_val, _tb = arg
            exc_repr = f"{exc_type.__name__}: {exc_val}"
            self.events.append(Event(
                id=eid, type="exception", node_id=node_id,
                func_name=func_name, filename=filename, lineno=lineno,
                locals=self._snapshot_locals(frame), arg=exc_repr
            ))
            self._set_node_exception(node_id, exc_repr)
            return self.trace

        return self.trace
