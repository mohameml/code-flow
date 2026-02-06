"""
Terminal UI components using Rich library.

This module provides a clean interface to Rich library features:
- Panels for error messages
- Syntax-highlighted tracebacks
- Spinners for progress indication
- Code syntax highlighting
"""

import sys
from contextlib import contextmanager
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.syntax import Syntax


class UI:
    """
    Terminal UI helper using Rich library.
    
    Provides methods for displaying:
    - Error panels
    - Syntax-highlighted tracebacks
    - Progress spinners
    - Code syntax highlighting
    
    Usage:
        >>> ui = UI()
        >>> ui.show_panel("Error occurred", title="Error", style="red")
        >>> 
        >>> with ui.spinner("Loading..."):
        ...     # Do work
        ...     pass
    """
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize UI.
        
        Args:
            console: Optional Rich Console instance. If None, creates one.
        """
        self.console = console or Console()
    
    # ========================================================================
    # Panel Display
    # ========================================================================
    
    def show_panel(
        self,
        content: str,
        title: str,
        style: str = "yellow"
    ) -> None:
        """
        Display content in a bordered panel.
        
        Args:
            content: Text to display in panel
            title: Panel title
            style: Border style/color (yellow, red, green, blue, etc.)
            
        Example:
            >>> ui.show_panel(
            ...     "File not found: script.py",
            ...     title="Error",
            ...     style="red"
            ... )
            
            ╭──── Error ────╮
            │ File not found│
            ╰───────────────╯
        """
        panel = Panel(
            content,
            title=title,
            border_style=style,
            expand=False
        )
        self.console.print(panel)
    
    # ========================================================================
    # Traceback Display
    # ========================================================================
    
    def show_traceback(
        self,
        error: Optional[Exception] = None,
        show_locals: bool = False
    ) -> None:
        """
        Display syntax-highlighted traceback.
        
        Args:
            error: Optional exception to display. If None, shows current exception.
            show_locals: Whether to show local variables in traceback
            
        Example:
            >>> try:
            ...     1 / 0
            ... except Exception as e:
            ...     ui.show_traceback(e)
            
            [Displays beautiful syntax-highlighted traceback]
        """
        if error:
            # Show traceback for specific exception
            self.console.print_exception(
                show_locals=show_locals,
                max_frames=20
            )
        else:
            # Show current exception
            self.console.print_exception(
                show_locals=show_locals,
                max_frames=20
            )
    
    def show_traceback_from_text(
        self,
        traceback_text: str,
        title: Optional[str] = None
    ) -> None:
        """
        Display traceback from text string.
        
        Useful when you have traceback as a string (e.g., from RunResult.error).
        
        Args:
            traceback_text: Traceback as string
            title: Optional panel title
            
        Example:
            >>> ui.show_traceback_from_text(
            ...     result.error,
            ...     title="Error in your code"
            ... )
        """
        if title:
            panel = Panel(
                traceback_text,
                title=title,
                border_style="yellow",
                expand=False
            )
            self.console.print(panel)
        else:
            # Show without panel, with syntax highlighting
            syntax = Syntax(
                traceback_text,
                "python",
                theme="monokai",
                line_numbers=False
            )
            self.console.print(syntax)
    
    # ========================================================================
    # Code Syntax Highlighting
    # ========================================================================
    
    def show_code(
        self,
        code: str,
        language: str = "python",
        line_numbers: bool = True,
        theme: str = "monokai"
    ) -> None:
        """
        Display syntax-highlighted code.
        
        Args:
            code: Code string to highlight
            language: Programming language (python, javascript, etc.)
            line_numbers: Whether to show line numbers
            theme: Color theme (monokai, github-dark, etc.)
            
        Example:
            >>> ui.show_code(
            ...     "def fib(n):\\n    return n",
            ...     line_numbers=True
            ... )
            
            1 │ def fib(n):
            2 │     return n
        """
        syntax = Syntax(
            code,
            language,
            theme=theme,
            line_numbers=line_numbers
        )
        self.console.print(syntax)
    
    # ========================================================================
    # Spinner / Progress
    # ========================================================================
    
    @contextmanager
    def spinner(
        self,
        message: str = "Working...",
        spinner_type: str = "dots"
    ):
        """
        Show spinner during operation (context manager).
        
        Args:
            message: Message to display next to spinner
            spinner_type: Spinner animation type (dots, line, arc, etc.)
            
        Yields:
            None
            
        Usage:
            >>> with ui.spinner("Tracing execution..."):
            ...     # Do work
            ...     result = runner.run_file("script.py")
            
            [Shows: ⠋ Tracing execution...]
            
        Available spinner types:
            - dots (recommended)
            - line
            - arc
            - arrow
            - bounce
            - circle
        """
        spinner = Spinner(
            spinner_type, 
            text=message,
            style="bright_green"
        )
        with Live(spinner, console=self.console, transient=True):
            yield
    
    def show_spinner_static(self, message: str) -> None:
        """
        Show static spinner message (no animation).
        
        Useful when you can't use context manager.
        
        Args:
            message: Message to display
            
        Example:
            >>> ui.show_spinner_static("⚙️  Tracing...")
        """
        self.console.print(message)
    
    # ========================================================================
    # Simple Printing
    # ========================================================================
    
    def print(self, *args, **kwargs) -> None:
        """
        Print using Rich console.
        
        Args:
            *args: Arguments to print
            **kwargs: Keyword arguments (style, highlight, etc.)
            
        Example:
            >>> ui.print("Success!", style="green bold")
            >>> ui.print("[red]Error[/red]: Something went wrong")
        """
        self.console.print(*args, **kwargs)
    
    def print_error(self, *args, **kwargs) -> None:
        """
        Print to stderr using Rich console.
        
        Args:
            *args: Arguments to print
            **kwargs: Keyword arguments
            
        Example:
            >>> ui.print_error("Error occurred", style="red")
        """
        # Create temporary stderr console
        err_console = Console(stderr=True)
        err_console.print(*args, **kwargs)
    
    # ========================================================================
    # Dividers and Spacing
    # ========================================================================
    
    def show_divider(self, char: str = "─") -> None:
        """
        Show horizontal divider line.
        
        Args:
            char: Character to use for divider
            
        Example:
            >>> ui.show_divider()
            ──────────────────────────────────
        """
        width = self.console.width
        self.console.print(char * width)
    
    def newline(self, count: int = 1) -> None:
        """
        Print empty lines.
        
        Args:
            count: Number of empty lines
        """
        for _ in range(count):
            self.console.print()


# ============================================================================
# Convenience Functions (Optional)
# ============================================================================

# Module-level singleton for convenience
_default_ui = UI()


def show_panel(content: str, title: str, style: str = "yellow") -> None:
    """Convenience function to show panel."""
    _default_ui.show_panel(content, title, style)


def show_traceback(error: Optional[Exception] = None) -> None:
    """Convenience function to show traceback."""
    _default_ui.show_traceback(error)


def spinner(message: str = "Working..."):
    """Convenience function to get spinner context manager."""
    return _default_ui.spinner(message)