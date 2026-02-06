"""
Main output handler for CodeFlow CLI.

This module provides the OutputHandler class which orchestrates
all output formatting and display.
"""

from pathlib import Path
from typing import Optional

from codeflow.cli.models import CliInput, CliOutput
from codeflow.core.models import RunResult
from codeflow.cli.output.formatters import SuccessFormatter, ErrorFormatter
from codeflow.cli.output.templates import Templates
from codeflow.cli.output.utils import get_file_stats
from codeflow.cli.output.ui import UI


class OutputHandler:
    """
    Main output handler for CodeFlow CLI.
    
    Responsibilities :
        - Display input file information
        - Show progress during execution
        - Format and display success/error results
        - create CliOutput 
    
    Usage:
        >>> handler = OutputHandler(verbose=False)
        >>> handler.show_input(cli_input)
        📄 Input: fib.py
        
        >>> with handler.show_progress():
        ...     result = runner.run_file(...)
        
        >>> handler.display(output, result, duration=0.123)
        ✅ Trace completed
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize output handler.
        
        Args:
            verbose: If True, show detailed output
        """
        self.verbose = verbose
        self.success_formatter = SuccessFormatter(verbose=verbose)
        self.error_formatter = ErrorFormatter()
        self.ui = UI()
    
    # ========================================================================
    # Input Display
    # ========================================================================
    
    def show_input(self, cli_input: CliInput) -> None:
        """
        Display input file information.
        
        In normal mode: Shows just the filename
        In verbose mode: Shows filename, size, and line count
        
        Args:
            cli_input: CliInput with source file path
            
        Example (normal):
            📄 Input: examples/fib.py
            
        Example (verbose):
            📄 Input File
               Path: examples/fib.py
               Size: 156 bytes
               Lines: 7
        """
        if self.verbose:
            self._show_input_verbose(cli_input)
        else:
            self._show_input_normal(cli_input)
    
    def _show_input_normal(self, cli_input: CliInput) -> None:
        """Show minimal input information."""
        message = Templates.input_normal(cli_input.source_file)
        print(message)
    
    def _show_input_verbose(self, cli_input: CliInput) -> None:
        """Show detailed input information."""
        # Get file statistics
        file_path = Path(cli_input.source_file)
        stats = get_file_stats(file_path)
        
        # Format and display
        message = Templates.input_verbose(
            source_file=cli_input.source_file,
            file_size=stats.size_formatted,
            line_count=stats.lines
        )
        print(message)
    
    # ========================================================================
    # Progress Display
    # ========================================================================
    
    def show_progress(self, message: Optional[str] = None):
        """
        Show progress indicator during execution.
        
        Returns a context manager:
        - In normal mode: Shows animated spinner
        - In verbose mode: Just prints message (no animation)
        
        Args:
            message: Optional custom progress message
            
        Returns:
            Context manager for progress display
            
        Usage:
            >>> with handler.show_progress():
            ...     result = runner.run_file("script.py")
            
            [Shows: ⠋ Tracing... (with animation)]
        """
        # Get default message based on mode
        if message is None:
            message = Templates.progress_verbose() if self.verbose else Templates.progress_normal()
        
        # if self.verbose:
        #     # In verbose mode, just print the message (no spinner)
        #     # User will see event updates later (Phase 2)
        #     print(message)
        #     # Return a no-op context manager
        #     from contextlib import nullcontext
        #     return nullcontext()
        # else:
        #     # In normal mode, show spinner
        #     return self.ui.spinner(message)
        
        return self.ui.spinner(message)
        
    
    # ========================================================================
    # Result Display
    # ========================================================================
    
    def display(
        self,
        output: CliOutput,
        result: Optional[RunResult] = None,
        duration: float = 0.0
    ) -> None:
        """
        Display execution results.
        
        Routes to appropriate formatter based on output status.
        
        Args:
            output: CliOutput with status and paths
            result: Optional RunResult for verbose statistics
            duration: Execution duration in seconds
        """
        if output.is_success():
            self.success_formatter.display(output, result, duration)
        else:
            self.error_formatter.display(output, result)
    
    # ========================================================================
    # Convenience Methods
    # ========================================================================
    
    def format_success(
        self,
        png_path: str,
        json_path: Optional[str] = None,
        result: Optional[RunResult] = None,
        duration: float = 0.0
    ) -> CliOutput:
        """
        Create a success CliOutput object.
        
        This is a helper method that creates the CliOutput object
        that will later be passed to display().
        
        Args:
            png_path: Path to generated PNG file
            json_path: Optional path to generated JSON file
            result: Optional RunResult for verbose mode
            duration: Execution duration
            
        Returns:
            CliOutput object with success status
            
        Example:
            >>> output = handler.format_success(
            ...     png_path="fib.png",
            ...     json_path="fib.json",
            ...     result=result,
            ...     duration=0.123
            ... )
            >>> handler.display(output, result, duration)
        """
        from codeflow.cli.models import OutputStatus
        
        message = "Trace completed successfully"
        
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
        Create an error CliOutput object.
        
        Args:
            error: Exception that occurred
            error_details: Optional detailed error message
            
        Returns:
            CliOutput object with error status
            
        Example:
            >>> try:
            ...     result = runner.run_file("buggy.py")
            ... except Exception as e:
            ...     output = handler.format_error(e, str(e))
            ...     handler.display(output)
        """
        from codeflow.cli.models import OutputStatus
        
        # Determine error message
        error_type = type(error).__name__
        message = f"Execution failed: {error_type}"
        
        return CliOutput(
            status=OutputStatus.ERROR,
            message=message,
            error_details=error_details or str(error)
        )


# ============================================================================
# Module-Level Convenience Functions
# ============================================================================

def create_handler(verbose: bool = False) -> OutputHandler:
    """
    Create an OutputHandler instance.
    
    Args:
        verbose: Whether to enable verbose mode
        
    Returns:
        OutputHandler instance
        
    Example:
        >>> handler = create_handler(verbose=True)
        >>> handler.show_input(cli_input)
    """
    return OutputHandler(verbose=verbose)