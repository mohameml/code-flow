import argparse
import os
from pathlib import Path
from typing import Optional

from codeflow.cli.models import CliInput


class Parser:
    """
    Parse and validate command-line arguments.
    
    Responsibilities:
    - Parse sys.argv into structured data
    - Validate file existence
    - Generate default output paths
    - Provide helpful error messages
    """
    
    def __init__(self):
        self._parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all options."""
        parser = argparse.ArgumentParser(
            description="Trace Python code execution and generate call graph.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  codeflow script.py
  codeflow script.py --out-png graph.png
  codeflow script.py --out-json trace.json --show-module
            """
        )
        
        parser.add_argument(
            "file",
            help="Python file to trace"
        )
        
        parser.add_argument(
            "--out-png",
            default=None,
            help="Output PNG path (default: <file>.callgraph.png)"
        )
        
        parser.add_argument(
            "--out-json",
            default=None,
            help="Output JSON path (optional)"
        )
        
        parser.add_argument(
            "--show-module",
            action="store_true",
            help="Show <module> node in call graph"
        )
        
        parser.add_argument(
            "-v", "--verbose",
            action="store_true", 
            help="Verbose output"
        )
        
        return parser
    
    def parse(self, args: Optional[list] = None) -> CliInput:
        """
        Parse command-line arguments.
        
        Args:
            args: Arguments to parse (None = sys.argv)
            
        Returns:
            Validated CliInput
            
        Raises:
            SystemExit: If parsing fails
        """
        parsed = self._parser.parse_args(args)
        
        # Generate default output paths
        source_path = Path(parsed.file)
        base_name = source_path.stem
        
        output_png = parsed.out_png or f"{base_name}.callgraph.png"
        
        cli_input = CliInput(
            source_file=str(source_path),
            output_png=output_png,
            output_json=parsed.out_json,
            show_module=parsed.show_module,
            verbose=parsed.verbose
        )
        
        # Validate
        self.validate(cli_input)
        
        return cli_input
    
    def validate(self, cli_input: CliInput) -> None:
        """
        Validate CLI input.
        
        Args:
            cli_input: Input to validate
            
        Raises:
            FileNotFoundError: If source file doesn't exist
            ValueError: If validation fails
        """
        # Check file exists
        if not os.path.exists(cli_input.source_file):
            raise FileNotFoundError(
                f"Source file not found: {cli_input.source_file}"
            )
        
        # Check file is Python
        if not cli_input.source_file.endswith('.py'):
            raise ValueError(
                f"Source file must be a Python file (.py): {cli_input.source_file}"
            )
        
        # Check output directory exists (create if needed)
        output_dir = Path(cli_input.output_png).parent
        if output_dir != Path('.') and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)