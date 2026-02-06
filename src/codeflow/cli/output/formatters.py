"""
Output formatters for success and error cases.

This module provides:
- SuccessFormatter: Formats successful execution output
- ErrorFormatter: Formats error output with detection of user vs internal errors
"""

from pathlib import Path
from typing import Optional

from codeflow.cli.models import CliOutput
from codeflow.core.models import RunResult
from codeflow.cli.output.templates import Templates
from codeflow.cli.output.utils import (
    get_event_stats,
    get_graph_stats,
    get_file_stats,
    format_size
)
from codeflow.cli.output.ui import UI

class SuccessFormatter:
    """
    Format successful execution output.
    
    Handles two modes:
    - Normal: Minimal output (input, result)
    - Verbose: Detailed statistics and metrics
    
    Usage:
        >>> formatter = SuccessFormatter(verbose=False)
        >>> formatter.display(output, result)
        ✅ Trace completed
        
        📊 Output:
            PNG  : fib.callgraph.png
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize formatter.
        
        Args:
            verbose: If True, show detailed statistics
        """
        self.verbose = verbose
        self.ui = UI()

    def display(
        self,
        output: CliOutput,
        result: Optional[RunResult] = None,
        duration: float = 0.0
    ) -> None:
        """
        Display success message.
        
        Args:
            output: CliOutput with paths and status
            result: Optional RunResult for verbose stats
            duration: Execution duration in seconds
        """
        if self.verbose:
            self._display_verbose(output, result, duration)
        else:
            self._display_normal(output)

    def _display_normal(self, output: CliOutput) -> None:
        """
        Display normal (minimal) success output.
        
        Format:
            ✅ Trace completed
            
            📊 Output:
               PNG  : fib.callgraph.png
               JSON : fib.trace.json
        """
        message = Templates.normal_success(
            source_file="",  # Not shown in normal mode
            png_path=output.png_path or "",
            json_path=output.json_path
        )
        
        print(message)

    def _display_verbose(
        self,
        output: CliOutput,
        result: Optional[RunResult],
        duration: float
    ) -> None:
        """
        Display verbose (detailed) success output.
        
        Format:
            ✅ Trace completed in 0.023s
            
            📊 Execution Statistics
               Total events:       40
               ...
            
            📈 Call Graph
               Nodes: 10
               ...
            
            💾 Output Files
               PNG  : fib.callgraph.png (15.2 KB)
        """
        if not result:
            # Fallback to normal if no result available
            self._display_normal(output)
            return
        
        # Get statistics
        event_stats = get_event_stats(result.events, len(result.nodes))
        graph_stats = get_graph_stats(result)
        
        # Get file sizes
        png_path = Path(output.png_path) if output.png_path else None
        json_path = Path(output.json_path) if output.json_path else None
        
        # TODO : why not use get_file_stats 
        # png_stats = get_file_stats(png_path)

        png_size = format_size(png_path.stat().st_size) if png_path and png_path.exists() else "0 bytes"
        json_size = format_size(json_path.stat().st_size) if json_path and json_path.exists() else None
        
        # Format duration
        from codeflow.cli.output.utils import format_duration
        duration_str = format_duration(duration)
        
        # Generate verbose message
        message = Templates.verbose_success(
            source_file="",  # Already shown before execution
            png_path=output.png_path or "",
            json_path=output.json_path,
            duration=duration_str,
            total_events=event_stats.total,
            call_events=event_stats.calls,
            line_events=event_stats.lines,
            return_events=event_stats.returns,
            function_count=event_stats.function_count,
            function_names=event_stats.function_names,
            max_depth=event_stats.max_depth,
            node_count=graph_stats['node_count'],
            edge_count=graph_stats['edge_count'],
            max_fanout=graph_stats['max_fanout'],
            png_size=png_size,
            json_size=json_size
        )
        
        print(message)

class ErrorFormatter:
    """
    Format error output.
    
    Detects and handles two types of errors:
    - User code errors: Errors in the traced script
    - Internal errors: Errors in CodeFlow itself
    
    Usage:
        >>> formatter = ErrorFormatter()
        >>> formatter.display(output, result)
        ❌ User code error: ZeroDivisionError
        
        [Error panel with traceback]
        
        💡 Tip: Fix the error in your code and try again.
    """
    
    def __init__(self):
        """Initialize error formatter."""
        self.ui = UI()

    def display(
        self,
        output : CliOutput,
        result : Optional[RunResult] = None , 

    ) -> None:
        """
        Display error message.
        
        Automatically detects whether error is from user code or CodeFlow
        and formats accordingly.
        
        Args:
            output: CliOutput with error information
            result: Optional RunResult (helps detect error type)
        """
        # Detect error type
        is_user_error = self._is_user_error(output, result)
        
        if is_user_error:
            self._display_user_error(output, result)
        else:
            self._display_internal_error(output)

    def _is_user_error(
        self,
        output: CliOutput,
        result: Optional[RunResult]
    ) -> bool:
        """
        Detect if error is from user code or CodeFlow.
        
        Strategy:
        1. If result.status == "runtime_error", it's user code
        2. If we have events (partial trace), it's user code
        3. Otherwise, it's CodeFlow internal error
        
        Args:
            output: CliOutput with error info
            result: Optional RunResult
            
        Returns:
            True if error is from user code, False if internal
        """
        # TODO : i'm not shure about this strategy for user error detection 
        # because it will leve exception so we need to catch it and return always RunResult ??? 

        # Strategy 1: Check result status
        if result and result.status == "runtime_error":
            return True
        
        # Strategy 2: If we have partial trace, error happened during execution
        if result and len(result.events) > 0:
            return True
        
        # Strategy 3: Default to internal error
        return False

    def _display_user_error(
        self,
        output: CliOutput,
        result: Optional[RunResult]
    ) -> None:
        """
        Display user code error with syntax highlighting.
        
        Shows:
        - Error message
        - Syntax-highlighted traceback in panel
        - Helpful tip
        """
        # Print error header
        print(f"\n❌ {output.message}\n")
        
        # Show traceback in panel
        if output.error_details:
            self.ui.show_panel(
                content=output.error_details,
                title="Error in your code",
                style="yellow"
            )
        
        # Show tip
        print("\n💡 Tip: Fix the error in your code and try again.\n")
        
        # If we have partial results, mention them
        if result and len(result.events) > 0:
            print(f"Note: Captured {len(result.events)} events before error occurred.\n")

    def _display_internal_error(self, output: CliOutput) -> None:
        """
        Display CodeFlow internal error.
        
        Shows:
        - Error message
        - Error details in panel
        - Link to report bug
        """
        # Print error header
        print(f"\n❌ {output.message}\n")
        
        # Show error details in panel
        if output.error_details:
            self.ui.show_panel(
                content=output.error_details,
                title="CodeFlow Error",
                style="red"
            )
        
        # Show tip with GitHub link
        print("\n💡 This looks like a CodeFlow bug. Please report it!")
        print("   GitHub: https://github.com/mohameml/code-flow/issues\n")



# ============================================================================
# Helper Functions
# ============================================================================

def format_success(
    output: CliOutput,
    result: Optional[RunResult] = None,
    duration: float = 0.0,
    verbose: bool = False
) -> None:
    """
    Convenience function to format and display success.
    
    Args:
        output: CliOutput with success information
        result: Optional RunResult for verbose stats
        duration: Execution duration in seconds
        verbose: Whether to show verbose output
        
    Example:
        >>> format_success(output, result, duration=0.123, verbose=True)
    """
    formatter = SuccessFormatter(verbose=verbose)
    formatter.display(output, result, duration)


def format_error(
    output: CliOutput,
    result: Optional[RunResult] = None
) -> None:
    """
    Convenience function to format and display error.
    
    Args:
        output: CliOutput with error information
        result: Optional RunResult
        
    Example:
        >>> format_error(output, result)
    """
    formatter = ErrorFormatter()
    formatter.display(output, result)




