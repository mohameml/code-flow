"""
CLI data models for CodeFlow.

This module defines the input and output data structures for the CLI layer.
These models provide type-safe, validated representations of command-line
arguments and execution results.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class CliInput:
    """
    Validated command-line input parameters.
    
    This class represents the parsed and validated arguments from the command line.
    It is immutable (frozen) to prevent accidental modification after validation.
    
    Attributes:
        source_file: Path to the Python file to trace and analyze
        output_png: Path where the call graph PNG will be saved
        output_json: Optional path where the trace JSON will be saved
        show_module: Whether to include the <module> node in the call graph
        verbose: Whether to display verbose output with detailed statistics
    
    Examples:
        >>> cli_input = CliInput(
        ...     source_file="examples/fib.py",
        ...     output_png="fib.callgraph.png",
        ...     output_json=None,
        ...     show_module=False,
        ...     verbose=False
        ... )
        >>> cli_input.source_file
        'examples/fib.py'
        >>> cli_input.is_json_export_enabled()
        False
    
    Raises:
        ValueError: If validation fails (empty paths, invalid values)
    """
    
    source_file: str
    output_png: str
    output_json: Optional[str] = None
    show_module: bool = False
    verbose: bool = False
    
    def __post_init__(self):
        """
        Validate input parameters after initialization.
        
        Ensures that required fields are not empty and values are reasonable.
        This is called automatically by the dataclass after __init__.
        
        Raises:
            ValueError: If any validation check fails
        """
        # Validate source_file
        if not self.source_file:
            raise ValueError("source_file cannot be empty")
        
        if not isinstance(self.source_file, str):
            raise ValueError(f"source_file must be a string, got {type(self.source_file)}")
        
        # Validate output_png
        if not self.output_png:
            raise ValueError("output_png cannot be empty")
        
        if not isinstance(self.output_png, str):
            raise ValueError(f"output_png must be a string, got {type(self.output_png)}")
        
        # Validate output_json (optional)
        if self.output_json is not None:
            if not isinstance(self.output_json, str):
                raise ValueError(f"output_json must be a string or None, got {type(self.output_json)}")
            
            if not self.output_json:  # Empty string
                raise ValueError("output_json cannot be an empty string (use None instead)")
        
        # Validate boolean flags
        if not isinstance(self.show_module, bool):
            raise ValueError(f"show_module must be a boolean, got {type(self.show_module)}")
        
        if not isinstance(self.verbose, bool):
            raise ValueError(f"verbose must be a boolean, got {type(self.verbose)}")
    
    def is_json_export_enabled(self) -> bool:
        """
        Check if JSON export is enabled.
        
        Returns:
            True if output_json is specified, False otherwise
        """
        return self.output_json is not None
    
    def get_source_filename(self) -> str:
        """
        Get the filename (without directory) of the source file.
        
        Returns:
            Filename of the source file
            
        Example:
            >>> cli_input = CliInput("examples/fib.py", "out.png")
            >>> cli_input.get_source_filename()
            'fib.py'
        """
        return Path(self.source_file).name
    
    def get_output_png_path(self) -> Path:
        """
        Get the output PNG path as a Path object.
        
        Returns:
            Path object for the PNG output
        """
        return Path(self.output_png)
    
    def get_output_json_path(self) -> Optional[Path]:
        """
        Get the output JSON path as a Path object.
        
        Returns:
            Path object for the JSON output, or None if not specified
        """
        return Path(self.output_json) if self.output_json else None
    


class OutputStatus(str, Enum):
    """
    CLI execution status enumeration.
    
    This enum defines the possible execution statuses for the CLI.
    Inheriting from str allows the enum to be easily serialized to JSON
    and compared with string values when needed.
    
    Attributes:
        SUCCESS: Execution completed successfully
        ERROR: Execution failed with an error
    
    Examples:
        >>> status = OutputStatus.SUCCESS
        >>> status == OutputStatus.SUCCESS
        True
        >>> status.value
        'success'
        >>> OutputStatus('success')
        <OutputStatus.SUCCESS: 'success'>
    """
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class CliOutput:
    """
    CLI execution result and output information.
    
    This class encapsulates the result of running the CodeFlow CLI,
    including success/error status, messages, and paths to generated files.
    
    The status field uses an Enum for type safety, preventing invalid
    status values at compile time and providing IDE autocomplete.
    
    Attributes:
        status: Execution status (SUCCESS or ERROR)
        message: Human-readable message describing the result
        png_path: Path to the generated PNG file (required for SUCCESS)
        json_path: Path to the generated JSON file (if requested)
        error_details: Detailed error information (for ERROR status)
    
    Examples:
        >>> # Success case
        >>> output = CliOutput(
        ...     status=OutputStatus.SUCCESS,
        ...     message="Trace completed successfully",
        ...     png_path="fib.callgraph.png",
        ...     json_path="fib.trace.json"
        ... )
        >>> output.is_success()
        True
        
        >>> # Error case
        >>> output = CliOutput(
        ...     status=OutputStatus.ERROR,
        ...     message="Execution failed",
        ...     error_details="FileNotFoundError: file.py not found"
        ... )
        >>> output.is_error()
        True
    """
    
    status: OutputStatus
    message: str # TODO : what is the purpose of this message if we already have a ErrorFormatter ? 
    png_path: Optional[str] = None
    json_path: Optional[str] = None
    error_details: Optional[str] = None # and how we can catch the trac back in user code and pass it to UI ???
    
    def __post_init__(self):
        """
        Validate output data after initialization.
        
        Raises:
            ValueError: If validation fails
            TypeError: If status is not OutputStatus enum
        """
        # Validate status type
        if not isinstance(self.status, OutputStatus):
            raise TypeError(
                f"status must be OutputStatus enum, got {type(self.status)}. "
                f"Use OutputStatus.SUCCESS or OutputStatus.ERROR"
            )
        
        # Validate message
        if not self.message:
            raise ValueError("message cannot be empty")
        
        # Validate success case has png_path
        if self.status == OutputStatus.SUCCESS and not self.png_path:
            raise ValueError("SUCCESS status requires png_path to be set")
    
    def is_success(self) -> bool:
        """
        Check if execution was successful.
        
        Returns:
            True if status is SUCCESS, False otherwise
        """
        return self.status == OutputStatus.SUCCESS
    
    def is_error(self) -> bool:
        """
        Check if execution failed.
        
        Returns:
            True if status is ERROR, False otherwise
        """
        return self.status == OutputStatus.ERROR
    
    def has_json_output(self) -> bool:
        """
        Check if JSON output was generated.
        
        Returns:
            True if json_path is set, False otherwise
        """
        return self.json_path is not None
    
    def get_all_output_paths(self) -> list[str]:
        """
        Get all generated output file paths.
        
        Returns:
            List of paths to generated files (PNG and/or JSON)
            
        Example:
            >>> output = CliOutput(
            ...     OutputStatus.SUCCESS, "Done", "a.png", "b.json"
            ... )
            >>> output.get_all_output_paths()
            ['a.png', 'b.json']
        """
        paths = []
        if self.png_path:
            paths.append(self.png_path)
        if self.json_path:
            paths.append(self.json_path)
        return paths
    
    def __str__(self) -> str:
        """
        Human-readable string representation.
        
        Returns:
            Formatted string with status emoji and message
        """
        emoji = "✅" if self.is_success() else "❌"
        return f"{emoji} {self.message}"

