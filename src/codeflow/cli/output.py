import sys
from typing import Optional

from codeflow.cli.models import CliOutput , OutputStatus
from codeflow.core.models import RunResult

"""

Questions : 
    - Q1. why we show the input in OuputHandler ?
    - Q2. 




- Strucutre of Output : 

    src/codeflow/cli/
    ├── models.py
    ├── parser.py
    │-- output
        ├── handler.py              # Main OutputHandler
        ├── formatters.py          # Success & Error formatters (2 classes)
        ├── templates.py           # String templates
        ├── ui.py           # UI for rich 
        └── utils.py # file_stats, format_size, etc.

- handler.py -> OutputHandler : 
    - verbsoe : bool
    - success_formatter : SuccessFormater
    - error_formatter : ErrorFormatter

    - display(output : CliOutput , result: RunResult)

- SuccessFormater :
    - display()
    -  _display_normal()
    - _display_verbose()

- ErrorFormatter  :
    - display(output :CliOuput , result : RunResult)
    - _display_user_error()
    - _display_internal_error()

- Template 

    - Template.normal_suucess_template : 

        📄 Input: examples/fib.py
            ⚙️  Tracing...
            ✅ Trace completed

        📊 Output:
            PNG  : examples/fib.callgraph.png
            JSON : examples/fib.trace.json


    - Template.verbose_success_template : 

        📄 Input File
            Path: examples/fib.py
            Size: 156 bytes
            Lines: 7

        ⚙️  Tracing execution...
            [⠋] Event #10: call fib(n=3) at line 1
            [⠙] Event #20: return fib → 2 at line 4
            [⠹] Event #30: call fib(n=1) at line 1
            ...

        ✅ Trace completed in 0.023s

        📊 Execution Statistics
            Total events:       40
                • call events:    10
                • line events:    20  
                • return events:  10
            
            Functions traced:   2 (fib, <module>)
            Max recursion depth: 4

        📈 Call Graph
            Nodes: 10
            Edges: 9
            Max fan-out: 2

        💾 Output Files
            PNG  : examples/fib.callgraph.png (15.2 KB)
            JSON : examples/fib.trace.json (8.3 KB)
        

    -  Template.error_user_code 
        ╭─────────────────────────────────────────╮
        │ Error in your code: buggy.py           │
        ╰─────────────────────────────────────────╯

        Traceback (most recent call last):
        File "buggy.py", line 10, in divide
            return a / b (use rich for beatuf heilthging)
                ~~^~~
        ZeroDivisionError: division by zero


    - Template.errror_internal_codeflow 

        This looks like a CodeFlow bug. Please report it!
    GitHub: "https://github.com/mohameml/code-flow/issues"


- utils : 
    - get_file_stats(file : Path) -> FileStats
        - we shoudl also typed FileStats 
    -  get_events_stats(result : RunResult) -> EventsStats

- Timer with context menagement 

- UI : 
    - spinner 
    - panel and synatax with tracke back beatufil errors panel  for heilight code user 


"""

"""
Paln : 

1. ✅ `utils.py`
   - `get_file_stats()`
   - `format_size()`
   - `get_event_stats()`

2. ✅ `formatters.py`
   - `SuccessFormatter` (normal + verbose modes)
   - `ErrorFormatter` (user + internal errors)

3. ✅ `output.py`
   - `OutputHandler.display()`
   - `OutputHandler.show_input()`

4. ✅ Integration with `main.py`

### **Phase 2: Polish (Later)**

5. ⏳ Timing wrapper
   - Auto-measure execution time
   - Display in verbose mode

6. ⏳ Spinner/Progress
   - Simple spinner for normal mode
   - Context manager for clean usage

7. ⏳ Rich error formatting
   - Syntax-highlighted tracebacks
   - Better panels

### **Phase 3: Advanced (Future)**

8. ⏳ Live event updates (verbose mode)
9. ⏳ Templates system
10. ⏳ Custom error tips per error type

"""

class OutputHandler:
    """
    Handle CLI output formatting and display.
    
    Responsibilities:
    - Format success/error messages
    - Display output to console
    - Handle verbose mode
    - Provide colored output (optional)
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def format_success(
        self,
        png_path: str,
        json_path: Optional[str] = None,
        result: Optional[RunResult] = None
    ) -> CliOutput:
        """
        Create success output message.
        
        Args:
            png_path: Path to generated PNG
            json_path: Path to generated JSON (optional)
            result: RunResult for verbose output
            
        Returns:
            CliOutput with success status
        """
        message = "Trace completed successfully"
        
        if self.verbose and result:
            message += f"\nEvents: {len(result.events)}"
            message += f"\nNodes: {len(result.nodes)}"
            message += f"\nEdges: {len(result.edges)}"
        
        return CliOutput(
            status=OutputStatus.SUCCESS,
            message=message,
            png_path=png_path,
            json_path=json_path
        )
    
    def format_error(
        self,
        error: Exception,
        error_details: Optional[str] = None
    ) -> CliOutput:
        """
        Create error output message.
        
        Args:
            error: Exception that occurred
            error_details: Additional error details
            
        Returns:
            CliOutput with error status
        """
        message = f"Execution failed: {type(error).__name__}"
        
        return CliOutput(
            status=OutputStatus.ERROR,
            message=message,
            error_details=error_details or str(error)
        )
    
    def display(self, output: CliOutput) -> None:
        """
        Display output to console.
        
        Args:
            output: CliOutput to display
        """
        if output.is_success():
            self._display_success(output)
        else:
            self._display_error(output)
    
    def _display_success(self, output: CliOutput) -> None:
        """Display success message."""
        print(f"✅ {output.message}")
        
        if output.png_path:
            print(f"PNG  : {output.png_path}")
        
        if output.json_path:
            print(f"JSON : {output.json_path}")
    
    def _display_error(self, output: CliOutput) -> None:
        """Display error message."""
        print(f"❌ {output.message}", file=sys.stderr)
        
        if output.error_details and self.verbose:
            print(f"\n{output.error_details}", file=sys.stderr)