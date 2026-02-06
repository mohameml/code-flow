"""
Output templates for CodeFlow CLI.

This module provides formatted output templates for different scenarios.
Templates are implemented as static methods for flexibility and type safety.
"""

from pathlib import Path
from typing import Optional

class Templates:
    """
    Collection of output templates for CodeFlow CLI.
    
    All methods are static and return formatted strings ready for display.
    Templates handle optional fields and formatting logic internally.
    """
    
    # ========================================================================
    # Success Templates
    # ========================================================================

    @staticmethod
    def normal_success(
        source_file: str,
        png_path: str,
        json_path: Optional[str] = None
    ) -> str:
        """
        Normal mode success template.
        
        Args:
            source_file: Path to traced file
            png_path: Path to generated PNG
            json_path: Optional path to generated JSON
            
        Returns:
            Formatted success message
            
        Example output:
            ✅ Trace completed
            
            📊 Output:
                PNG  : fib.callgraph.png
                JSON : fib.trace.json
        """
        # TODO : why don't use triple quote string """ """

        output = "✅ Trace completed\n\n"
        output += "📊 Output:\n"
        output += f"   PNG  : {png_path}\n"
        
        if json_path:
            output += f"   JSON : {json_path}\n"
        
        return output
    @staticmethod
    def verbose_success(
        source_file: str,
        png_path: str,
        json_path: Optional[str],
        duration: str,
        total_events: int,
        call_events: int,
        line_events: int,
        return_events: int,
        function_count: int,
        function_names: str,
        max_depth: int,
        node_count: int,
        edge_count: int,
        max_fanout: int,
        png_size: str,
        json_size: Optional[str] = None
    ) -> str:
        """
        Verbose mode success template.
        
        Args:
            # TODO : what the hell this is 
            # can we change this to something more structred 

            source_file: Path to traced file
            png_path: Path to generated PNG
            json_path: Optional path to generated JSON
            duration: Formatted execution duration
            total_events: Total number of events
            call_events: Number of call events
            line_events: Number of line events
            return_events: Number of return events
            function_count: Number of unique functions
            function_names: Comma-separated function names
            max_depth: Maximum recursion depth
            node_count: Number of call graph nodes
            edge_count: Number of call graph edges
            max_fanout: Maximum fan-out in call graph
            png_size: Formatted PNG file size
            json_size: Optional formatted JSON file size
            
        Returns:
            Formatted verbose success message
            
        Example output:
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
                PNG  : fib.callgraph.png (15.2 KB)
                JSON : fib.trace.json (8.3 KB)
        """
        output = f"✅ Trace completed in {duration}\n\n"
        
        # Execution Statistics
        output += "📊 Execution Statistics\n"
        output += f"   Total events:       {total_events}\n"
        output += f"     • call events:    {call_events}\n"
        output += f"     • line events:    {line_events}\n"
        output += f"     • return events:  {return_events}\n"
        output += "\n"
        output += f"   Functions traced:   {function_count} ({function_names})\n"
        output += f"   Max recursion depth: {max_depth}\n"
        output += "\n"
        
        # Call Graph Statistics
        output += "📈 Call Graph\n"
        output += f"   Nodes: {node_count}\n"
        output += f"   Edges: {edge_count}\n"
        output += f"   Max fan-out: {max_fanout}\n"
        output += "\n"
        
        # Output Files
        output += "💾 Output Files\n"
        output += f"   PNG  : {png_path} ({png_size})\n"
        
        if json_path and json_size:
            output += f"   JSON : {json_path} ({json_size})\n"
        
        return output

    # ========================================================================
    # Input Display Templates
    # ========================================================================
    
    @staticmethod
    def input_normal(source_file: str) -> str:
        """
        Normal mode input display.
        
        Args:
            source_file: Path to source file
            
        Returns:
            Formatted input message
            
        Example output:
            📄 Input: examples/fib.py
        """
        return f"📄 Input: {source_file}\n"
    
    @staticmethod
    def input_verbose(
        source_file: str,
        file_size: str,
        line_count: int
    ) -> str:
        """
        Verbose mode input display.
        
        Args:
            source_file: Path to source file
            file_size: Formatted file size
            line_count: Number of lines
            
        Returns:
            Formatted input message
            
        Example output:
            📄 Input File
                Path: examples/fib.py
                Size: 156 bytes
                Lines: 7
        """
        # TODO : and for the icon is it supported in every terminal ? 
        output = "📄 Input File\n"
        output += f"   Path: {source_file}\n"
        output += f"   Size: {file_size}\n"
        output += f"   Lines: {line_count}\n"
        return output

    # ========================================================================
    # Error Templates
    # ========================================================================
    
    @staticmethod
    def error_user_code(
        error_message: str,
        traceback_text: str
    ) -> str:
        """
        User code error template.
        
        This template is used when the error occurred in the user's code
        (not in CodeFlow itself).
        
        Args:
            error_message: Brief error description
            traceback_text: Full traceback (will be syntax-highlighted by UI)
            
        Returns:
            Formatted error message
            
        Note:
            The actual panel and syntax highlighting is done by UI.show_panel()
            and UI.show_traceback(). This just provides the structure.
            
        Example output:
            ❌ User code error: ZeroDivisionError
            
            [Panel with traceback - rendered by Rich]
            
            💡 Tip: Fix the error in your code and try again.
        """
        
        # TODO : do we realy nedd this functions and error_internal 
        # because it is handle by ErrorFormatter 

        output = f"\n❌ {error_message}\n\n"
        # Traceback will be shown in panel by UI
        # Tip
        output += "\n💡 Tip: Fix the error in your code and try again.\n"
        return output
    
    @staticmethod
    def error_internal(
        error_message: str,
        error_details: str
    ) -> str:
        """
        CodeFlow internal error template.
        
        This template is used when the error occurred in CodeFlow itself,
        not in the user's code.
        
        Args:
            error_message: Brief error description
            error_details: Detailed error information
            
        Returns:
            Formatted error message
            
        Example output:
            ❌ CodeFlow error: FileNotFoundError
            
            [Panel with error details - rendered by Rich]
            
            💡 This looks like a CodeFlow bug. Please report it!
                GitHub: https://github.com/mohameml/code-flow/issues
        """
        # TODO : do we realy nedd this functions and error_internal 
        # because it is handle by ErrorFormatter 

        output = f"\n❌ {error_message}\n\n"
        # Error details will be shown in panel by UI
        # Tip with GitHub link
        output += "\n💡 This looks like a CodeFlow bug. Please report it!\n"
        output += "   GitHub: https://github.com/mohameml/code-flow/issues\n"
        return output

    # ========================================================================
    # Progress Messages
    # ========================================================================
    # TODO : do we need thsi two functions 

    @staticmethod
    def progress_normal() -> str:
        """Normal mode progress message."""
        return "⚙️  Tracing..."
    
    @staticmethod
    def progress_verbose() -> str:
        """Verbose mode progress message."""
        return "⚙️  Tracing execution..."


    # ========================================================================
    # Helper Methods
    # ========================================================================
    # TODO : do we need thsi two functions 
    @staticmethod
    def format_file_outputs(
        png_path: str,
        json_path: Optional[str] = None,
        png_size: Optional[str] = None,
        json_size: Optional[str] = None
    ) -> str:
        """
        Format output file listing.
        
        Used by both normal and verbose success templates.
        
        Args:
            png_path: Path to PNG file
            json_path: Optional path to JSON file
            png_size: Optional formatted PNG size
            json_size: Optional formatted JSON size
            
        Returns:
            Formatted file listing
        """
        output = ""
        
        if png_size:
            output += f"   PNG  : {png_path} ({png_size})\n"
        else:
            output += f"   PNG  : {png_path}\n"
        
        if json_path:
            if json_size:
                output += f"   JSON : {json_path} ({json_size})\n"
            else:
                output += f"   JSON : {json_path}\n"
        
        return output