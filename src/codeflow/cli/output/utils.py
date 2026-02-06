"""
Utility functions and data classes for CLI output.

This module provides:
- File statistics computation
- Event statistics computation
- Size and duration formatting
- Timer context manager
"""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

from codeflow.core.models import Event, RunResult

# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class FileStats:
    """
    Statistics about a source file.
    
    Attributes:
        path: Path to the file
        size_bytes: File size in bytes
        size_formatted: Human-readable size (e.g., "1.5 KB")
        lines: Number of lines in the file
    
    Example:
        >>> stats = get_file_stats(Path("script.py"))
        >>> print(stats.size_formatted)
        '234 bytes'
        >>> print(stats.lines)
        15
    """
    path: Path
    size_bytes: int
    size_formatted: str
    lines: int

@dataclass
class EventStats:
    """
    Statistics computed from execution events.
    
    Attributes:
        total: Total number of events
        calls: Number of 'call' events
        lines: Number of 'line' events
        returns: Number of 'return' events
        exceptions: Number of 'exception' events
        function_count: Number of unique functions traced
        function_names: Comma-separated list of function names (first 5)
        max_depth: Estimated maximum recursion depth
    
    Example:
        >>> stats = get_event_stats(result.events, result.nodes)
        >>> print(f"Total: {stats.total}, Calls: {stats.calls}")
        Total: 40, Calls: 10
    """
    total: int
    calls: int
    lines: int
    returns: int
    exceptions: int
    function_count: int
    function_names: str
    max_depth: int


# ============================================================================
# File Statistics
# ============================================================================

def get_file_stats(filepath: Path) -> FileStats:

    """
    Get statistics about a source file.
    
    Args:
        filepath: Path to the file to analyze
        
    Returns:
        FileStats object with file information
        
    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file cannot be read
        
    Example:
        >>> stats = get_file_stats(Path("examples/fib.py"))
        >>> print(f"{stats.lines} lines, {stats.size_formatted}")
        7 lines, 156 bytes
    """
    if not filepath.exists() :
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Get file size :
    size_bytes = filepath.stat().st_size
    size_formatted = format_size(size_bytes)

    # Count Lines : 
    with open(filepath , 'r' , encoding="utf-8") as f : 
        lines = len(f.readlines())
    
    return FileStats(
        path=filepath,
        size_bytes=size_bytes,
        size_formatted=size_formatted,
        lines=lines
    )

# ============================================================================
# Event Statistics
# ============================================================================

def get_event_stats(events: List[Event], node_count: int = 0) -> EventStats:
    """
    Compute statistics from execution events.
    
    Args:
        events: List of Event objects from tracing
        node_count: Number of nodes (for max_depth estimation)
        
    Returns:
        EventStats object with computed statistics
        
    Example:
        >>> stats = get_event_stats(result.events, len(result.nodes))
        >>> print(f"{stats.calls} function calls")
        10 function calls
    """
    # Count event types 
    calls = sum(1 for e in events if e.is_call())
    lines = sum(1 for e in events if e.is_line())
    returns = sum(1 for e in events if e.is_return())
    exceptions = sum(1 for e in events if e.is_exception())

    functions = set(e.func_name for e in events)
    function_count = len(functions)

    # Format function names (show first , sorted)
    sorted_funcs = sorted(functions)
    if len(sorted_funcs) <= 5 : 
        function_names = ", ".join(sorted_funcs)
    else:
        function_names = ", ".join(sorted_funcs[:5]) + f", ... (+{len(sorted_funcs) - 5} more)"
    
    # TODO : Compute the real max depth 
    #  Estimate max depth (simplified: use node count as proxy)
    max_depth = node_count if node_count > 0 else 1
    
    return EventStats(
        total=len(events),
        calls=calls,
        lines=lines,
        returns=returns,
        exceptions=exceptions,
        function_count=function_count,
        function_names=function_names,
        max_depth=max_depth
    )

# ============================================================================
# Formatting Functions
# ============================================================================
def format_size(size_bytes : int) -> str : 
    """
    Format byte size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
        
    Examples:
        >>> format_size(123)
        '123 bytes'
        >>> format_size(1500)
        '1.5 KB'
        >>> format_size(1500000)
        '1.4 MB'
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        kb = size_bytes / 1024
        return f"{kb:.1f} KB"
    else:
        mb = size_bytes / (1024 * 1024)
        return f"{mb:.1f} MB"

def format_duration(seconds: float) -> str:
    """
    Format duration to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
        
    Examples:
        >>> format_duration(0.023)
        '0.023s'
        >>> format_duration(1.5)
        '1.500s'
        >>> format_duration(65.3)
        '1m 5.3s'
    """
    if seconds < 60:
        return f"{seconds:.3f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"

# ============================================================================
# Timer Context Manager
# ============================================================================


class Timer:
    """
    Context manager for timing code execution.
    
    Attributes:
        duration: Elapsed time in seconds (available after context exit)
        start_time: Start timestamp
        end_time: End timestamp
    
    Usage:
        >>> with Timer() as timer:
        ...     # Do some work
        ...     time.sleep(0.1)
        >>> print(f"Took {timer.duration:.3f}s")
        Took 0.100s
        
        >>> with Timer() as timer:
        ...     result = runner.run_file("script.py")
        >>> print(f"Execution: {format_duration(timer.duration)}")
        Execution: 0.234s
    """
    
    def __init__(self):
        self.duration: float = 0.0
        self.start_time: float = 0.0
        self.end_time: float = 0.0
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and compute duration."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        # Don't suppress exceptions
        return False
    
    def __str__(self) -> str:
        """Return formatted duration."""
        return format_duration(self.duration)


# ============================================================================
# Additional Helpers
# ============================================================================

def get_graph_stats(result: RunResult) -> dict:
    """
    Get call graph statistics.
    
    Args:
        result: RunResult containing nodes and edges
        
    Returns:
        Dictionary with graph statistics:
        - node_count: Number of nodes
        - edge_count: Number of edges
        - max_fanout: Maximum number of children any node has
        
    Example:
        >>> stats = get_graph_stats(result)
        >>> print(f"Graph: {stats['node_count']} nodes, {stats['edge_count']} edges")
        Graph: 10 nodes, 9 edges
    """
    node_count = len(result.nodes)
    edge_count = len(result.edges)

    # TODO : what the hell is fan-out ?  
    # Calculate max fan-out (max children per node)
    fanout_counts = {}
    for edge in result.edges:
        fanout_counts[edge.parent_id] = fanout_counts.get(edge.parent_id, 0) + 1
    
    max_fanout = max(fanout_counts.values()) if fanout_counts else 0
    
    # TODO : type the output of this functions 
    return {
        'node_count': node_count,
        'edge_count': edge_count,
        'max_fanout': max_fanout
    }