"""
CodeFlow CLI Output Module.

This module provides output formatting and display functionality.

Main Components:
- OutputHandler: Main orchestrator for all output
- SuccessFormatter: Formats successful execution output
- ErrorFormatter: Formats error output
- Templates: String templates for consistent formatting
- UI: Terminal UI helpers (Rich library wrappers)
- Utils: Helper functions and data classes

Usage:
    >>> from codeflow.cli.output import OutputHandler
    >>> 
    >>> handler = OutputHandler(verbose=True)
    >>> handler.show_input(cli_input)
    >>> 
    >>> with handler.show_progress():
    ...     result = runner.run_file(...)
    >>> 
    >>> output = handler.format_success(png_path, json_path, result, duration)
    >>> handler.display(output, result, duration)
"""

from codeflow.cli.output.handler import OutputHandler, create_handler
from codeflow.cli.output.formatters import (
    SuccessFormatter,
    ErrorFormatter,
    format_success,
    format_error
)
from codeflow.cli.output.templates import Templates
from codeflow.cli.output.ui import UI
from codeflow.cli.output.utils import (
    FileStats,
    EventStats,
    Timer,
    get_file_stats,
    get_event_stats,
    format_size,
    format_duration,
    get_graph_stats
)

__all__ = [
    # Main handler
    "OutputHandler",
    "create_handler",
    
    # Formatters
    "SuccessFormatter",
    "ErrorFormatter",
    "format_success",
    "format_error",
    
    # Templates
    "Templates",
    
    # UI
    "UI",
    
    # Utils
    "FileStats",
    "EventStats",
    "Timer",
    "get_file_stats",
    "get_event_stats",
    "format_size",
    "format_duration",
    "get_graph_stats",
]