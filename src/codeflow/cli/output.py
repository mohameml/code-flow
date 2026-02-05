import sys
from typing import Optional

from codeflow.cli.models import CliOutput
from codeflow.core.models import RunResult


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
            status="success",
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
            status="error",
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