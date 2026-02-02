
import sys 
import traceback
from typing import Dict , Any 


from codeflow.core.safe_repr import SafeRepr
from codeflow.core.models import Event , CallNode , CallEdge , RunResult , RunStatus
from codeflow.core.tracer import TraceRecorder


class Runner:
    """
    Exécution + trace. (MVP local)
    """
    def __init__(self, max_repr_len: int = 200):
        self.safe_repr = SafeRepr(max_len=max_repr_len)

    def run_file(self, filepath: str) -> RunResult:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        return self.run(code, user_filename=filepath)

    def run(self, code: str, user_filename: str) -> RunResult:
        recorder = TraceRecorder(user_filename=user_filename, safe_repr=self.safe_repr)

        # IMPORTANT: env unique (globals == locals) pour que la récursion fonctionne
        env: Dict[str, Any] = {"__name__": "__main__", "__file__": user_filename}

        try:
            compiled = compile(code, user_filename, "exec")
            sys.settrace(recorder.trace)
            exec(compiled, env, env)
            return RunResult(
                status="ok",
                events=recorder.events,
                nodes=recorder.nodes,
                edges=recorder.edges,
                error=None
            )
        except Exception:
            err = traceback.format_exc(limit=20)
            return RunResult(
                status="runtime_error",
                events=recorder.events,
                nodes=recorder.nodes,
                edges=recorder.edges,
                error=err
            )
        finally:
            sys.settrace(None)
