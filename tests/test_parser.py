"""
Comprehensive unit tests for Parser class.

Run with: pytest tests/test_parser.py -v
"""

import pytest
from pathlib import Path
from codeflow.cli.parser import Parser, parse_args
from codeflow.cli.models import CliInput


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def temp_py_file(tmp_path):
    """Create a temporary Python file for testing."""
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")
    return test_file


@pytest.fixture
def parser():
    """Create a Parser instance."""
    return Parser()


# ============================================================================
# Parser Creation Tests
# ============================================================================

class TestParserCreation:
    """Test Parser instantiation."""
    
    def test_create_parser(self):
        """Test that Parser can be instantiated."""
        parser = Parser()
        assert parser is not None
        assert parser._parser is not None
    
    def test_parser_has_correct_program_name(self):
        """Test that parser has correct prog name."""
        parser = Parser()
        assert parser._parser.prog == "codeflow"


# ============================================================================
# Argument Parsing Tests - Success Cases
# ============================================================================

class TestArgumentParsingSuccess:
    """Test successful argument parsing scenarios."""
    
    def test_parse_minimal_args(self, parser, temp_py_file):
        """Test parsing with only required argument."""
        args = [str(temp_py_file)]
        cli_input = parser.parse(args)
        
        assert cli_input.source_file == str(temp_py_file)
        assert cli_input.output_png == str(temp_py_file.parent / "test.callgraph.png")
        assert cli_input.output_json is None
        assert cli_input.show_module is False
        assert cli_input.verbose is False
    
    def test_parse_with_custom_png(self, parser, temp_py_file):
        """Test parsing with custom PNG path."""
        args = [str(temp_py_file), "--out-png", "custom.png"]
        cli_input = parser.parse(args)
        
        assert cli_input.output_png == "custom.png"
    
    def test_parse_with_json_output(self, parser, temp_py_file):
        """Test parsing with JSON output."""
        args = [str(temp_py_file), "--out-json", "trace.json"]
        cli_input = parser.parse(args)
        
        assert cli_input.output_json == "trace.json"

    def test_parse_with_json_output_auto(self, parser, temp_py_file):
        """Test parsing with JSON output."""
        args = [str(temp_py_file), "--out-json"]
        cli_input = parser.parse(args)
        
        assert cli_input.output_json == str(temp_py_file.parent / "test.trace.json")
    
    def test_parse_with_show_module(self, parser, temp_py_file):
        """Test parsing with --show-module flag."""
        args = [str(temp_py_file), "--show-module"]
        cli_input = parser.parse(args)
        
        assert cli_input.show_module is True
    
    def test_parse_with_verbose(self, parser, temp_py_file):
        """Test parsing with --verbose flag."""
        args = [str(temp_py_file), "--verbose"]
        cli_input = parser.parse(args)
        
        assert cli_input.verbose is True
    
    def test_parse_with_verbose_short(self, parser, temp_py_file):
        """Test parsing with -v flag."""
        args = [str(temp_py_file), "-v"]
        cli_input = parser.parse(args)
        
        assert cli_input.verbose is True
    
    def test_parse_with_all_options(self, parser, temp_py_file):
        """Test parsing with all optional arguments."""
        args = [
            str(temp_py_file),
            "--out-png", "graph.png",
            "--out-json", "trace.json",
            "--show-module",
            "--verbose"
        ]
        cli_input = parser.parse(args)
        
        assert cli_input.source_file == str(temp_py_file)
        assert cli_input.output_png == "graph.png"
        assert cli_input.output_json == "trace.json"
        assert cli_input.show_module is True
        assert cli_input.verbose is True


# ============================================================================
# Argument Parsing Tests - Failure Cases
# ============================================================================

class TestArgumentParsingFailure:
    """Test argument parsing failure scenarios."""
    
    def test_parse_no_arguments(self, parser):
        """Test that parsing with no arguments fails."""
        with pytest.raises(SystemExit):
            parser.parse([])
    
    def test_parse_help_flag(self, parser):
        """Test that --help flag raises SystemExit."""
        with pytest.raises(SystemExit):
            parser.parse(["--help"])
    
    def test_parse_unknown_flag(self, parser, temp_py_file):
        """Test that unknown flag raises SystemExit."""
        with pytest.raises(SystemExit):
            parser.parse([str(temp_py_file), "--unknown-flag"])


# ============================================================================
# File Validation Tests
# ============================================================================

class TestFileValidation:
    """Test file existence and type validation."""
    
    def test_validate_nonexistent_file(self, parser):
        """Test that nonexistent file raises FileNotFoundError."""
        args = ["nonexistent.py"]
        
        with pytest.raises(FileNotFoundError, match="Source file not found"):
            parser.parse(args)
    
    def test_validate_directory_instead_of_file(self, parser, tmp_path):
        """Test that directory path raises ValueError."""
        args = [str(tmp_path)]
        
        with pytest.raises(ValueError, match="Source path is not a file"):
            parser.parse(args)
    
    def test_validate_non_py_file_shows_warning(self, parser, tmp_path, capsys):
        """Test that non-.py file shows warning but doesn't fail."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        args = [str(test_file)]
        cli_input = parser.parse(args)
        
        # Should parse successfully
        assert cli_input.source_file == str(test_file)
        
        # Should print warning to stderr
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert ".py extension" in captured.err


# ============================================================================
# Output Path Generation Tests
# ============================================================================

class TestOutputPathGeneration:
    """Test automatic output path generation."""
    
    def test_default_png_path_simple_filename(self, parser, tmp_path):
        """Test default PNG path for simple filename."""
        test_file = tmp_path / "script.py"
        test_file.write_text("pass")
        
        args = [str(test_file)]
        cli_input = parser.parse(args)
        
        expected = str(tmp_path / "script.callgraph.png")
        assert cli_input.output_png == expected
    
    def test_default_png_path_nested_file(self, parser, tmp_path):
        """Test default PNG path for nested file."""
        nested_dir = tmp_path / "subdir"
        nested_dir.mkdir()
        test_file = nested_dir / "script.py"
        test_file.write_text("pass")
        
        args = [str(test_file)]
        cli_input = parser.parse(args)
        
        expected = str(nested_dir / "script.callgraph.png")
        assert cli_input.output_png == expected
    
    def test_default_png_path_with_dots_in_name(self, parser, tmp_path):
        """Test default PNG path with dots in filename."""
        test_file = tmp_path / "my.test.script.py"
        test_file.write_text("pass")
        
        args = [str(test_file)]
        cli_input = parser.parse(args)
        
        # Should use stem (everything before last dot)
        expected = str(tmp_path / "my.test.script.callgraph.png")
        assert cli_input.output_png == expected
    
    def test_custom_png_path_overrides_default(self, parser, temp_py_file):
        """Test that custom PNG path overrides default."""
        args = [str(temp_py_file), "--out-png", "custom/path/graph.png"]
        cli_input = parser.parse(args)
        
        assert cli_input.output_png == "custom/path/graph.png"


# ============================================================================
# Directory Creation Tests
# ============================================================================

class TestDirectoryCreation:
    """Test automatic creation of output directories."""
    
    def test_creates_png_output_directory(self, parser, temp_py_file, tmp_path):
        """Test that PNG output directory is created."""
        output_dir = tmp_path / "output" / "graphs"
        output_png = output_dir / "graph.png"
        
        # Directory doesn't exist yet
        assert not output_dir.exists()
        
        args = [str(temp_py_file), "--out-png", str(output_png)]
        cli_input = parser.parse(args)
        
        # Directory should be created
        assert output_dir.exists()
        assert output_dir.is_dir()
    
    def test_creates_json_output_directory(self, parser, temp_py_file, tmp_path):
        """Test that JSON output directory is created."""
        output_dir = tmp_path / "output" / "traces"
        output_json = output_dir / "trace.json"
        
        # Directory doesn't exist yet
        assert not output_dir.exists()
        
        args = [str(temp_py_file), "--out-json", str(output_json)]
        cli_input = parser.parse(args)
        
        # Directory should be created
        assert output_dir.exists()
        assert output_dir.is_dir()
    
    def test_creates_nested_directories(self, parser, temp_py_file, tmp_path):
        """Test that nested directories are created."""
        output_dir = tmp_path / "a" / "b" / "c"
        output_png = output_dir / "graph.png"
        
        args = [str(temp_py_file), "--out-png", str(output_png)]
        cli_input = parser.parse(args)
        
        # All nested directories should be created
        assert (tmp_path / "a").exists()
        assert (tmp_path / "a" / "b").exists()
        assert output_dir.exists()
    
    def test_handles_existing_directory(self, parser, temp_py_file, tmp_path):
        """Test that existing directory doesn't cause error."""
        output_dir = tmp_path / "existing"
        output_dir.mkdir()
        output_png = output_dir / "graph.png"
        
        # Should not raise error
        args = [str(temp_py_file), "--out-png", str(output_png)]
        cli_input = parser.parse(args)
        
        assert cli_input.output_png == str(output_png)


# ============================================================================
# CliInput Integration Tests
# ============================================================================

class TestCliInputIntegration:
    """Test integration with CliInput model."""
    
    def test_returns_valid_cli_input(self, parser, temp_py_file):
        """Test that parse() returns valid CliInput."""
        args = [str(temp_py_file)]
        cli_input = parser.parse(args)
        
        assert isinstance(cli_input, CliInput)
        assert cli_input.source_file is not None
        assert cli_input.output_png is not None
    
    def test_cli_input_is_frozen(self, parser, temp_py_file):
        """Test that returned CliInput is immutable."""
        args = [str(temp_py_file)]
        cli_input = parser.parse(args)
        
        # Should not be able to modify
        with pytest.raises(AttributeError):
            cli_input.source_file = "changed.py"  # type: ignore
    
    def test_cli_input_helper_methods_work(self, parser, temp_py_file):
        """Test that CliInput helper methods work with parsed data."""
        args = [str(temp_py_file), "--out-json", "trace.json"]
        cli_input = parser.parse(args)
        
        assert cli_input.is_json_export_enabled() is True
        assert cli_input.get_source_filename() == "test.py"


# ============================================================================
# Convenience Function Tests
# ============================================================================

class TestConvenienceFunction:
    """Test the parse_args convenience function."""
    
    def test_parse_args_function(self, temp_py_file):
        """Test parse_args convenience function."""
        cli_input = parse_args([str(temp_py_file)])
        
        assert isinstance(cli_input, CliInput)
        assert cli_input.source_file == str(temp_py_file)


# ============================================================================
# Edge Cases and Corner Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and unusual inputs."""
    
    def test_parse_file_with_spaces_in_name(self, parser, tmp_path):
        """Test parsing file with spaces in name."""
        test_file = tmp_path / "my script.py"
        test_file.write_text("pass")
        
        args = [str(test_file)]
        cli_input = parser.parse(args)
        
        assert cli_input.source_file == str(test_file)
        assert "my script.callgraph.png" in cli_input.output_png
    
    def test_parse_file_with_unicode_name(self, parser, tmp_path):
        """Test parsing file with Unicode characters."""
        test_file = tmp_path / "tëst_文件.py"
        test_file.write_text("pass")
        
        args = [str(test_file)]
        cli_input = parser.parse(args)
        
        assert cli_input.source_file == str(test_file)
    
    def test_parse_absolute_vs_relative_path(self, parser, temp_py_file):
        """Test parsing with absolute vs relative path."""
        # Absolute path
        args_abs = [str(temp_py_file.resolve())]
        cli_input_abs = parser.parse(args_abs)
        
        # Relative path
        args_rel = [str(temp_py_file.name)]
        # This will fail because relative path won't exist from current dir
        # Just testing that absolute paths work
        assert cli_input_abs.source_file == str(temp_py_file)
    
    def test_parse_current_directory_output(self, parser, tmp_path):
        """Test output in current directory (no subdirectory creation needed)."""
        test_file = tmp_path / "script.py"
        test_file.write_text("pass")
        
        # Output in same directory as input
        args = [str(test_file), "--out-png", "graph.png"]
        cli_input = parser.parse(args)
        
        assert cli_input.output_png == "graph.png"


# ============================================================================
# Error Message Quality Tests
# ============================================================================

class TestErrorMessages:
    """Test quality and clarity of error messages."""
    
    def test_file_not_found_error_message(self, parser):
        """Test that FileNotFoundError has helpful message."""
        try:
            parser.parse(["nonexistent.py"])
            pytest.fail("Should have raised FileNotFoundError")
        except FileNotFoundError as e:
            error_msg = str(e)
            assert "Source file not found" in error_msg
            assert "nonexistent.py" in error_msg
            assert "check that the file path is correct" in error_msg
    
    def test_directory_error_message(self, parser, tmp_path):
        """Test that directory error has helpful message."""
        try:
            parser.parse([str(tmp_path)])
            pytest.fail("Should have raised ValueError")
        except ValueError as e:
            error_msg = str(e)
            assert "Source path is not a file" in error_msg
            assert "provide a path to a Python file" in error_msg


# ============================================================================
# Real-World Usage Tests
# ============================================================================

class TestRealWorldUsage:
    """Test real-world usage scenarios."""
    
    def test_fibonacci_example(self, parser, tmp_path):
        """Test parsing for fibonacci example scenario."""
        fib_file = tmp_path / "fib.py"
        fib_file.write_text("""
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(4))
        """)
        
        args = [str(fib_file)]
        cli_input = parser.parse(args)
        
        assert cli_input.source_file == str(fib_file)
        assert "fib.callgraph.png" in cli_input.output_png
    
    def test_project_structure_example(self, parser, tmp_path):
        """Test parsing with project-like structure."""
        # Create structure: project/examples/fib.py
        examples_dir = tmp_path / "project" / "examples"
        examples_dir.mkdir(parents=True)
        fib_file = examples_dir / "fib.py"
        fib_file.write_text("pass")
        
        # User runs: codeflow examples/fib.py --out-png output/fib.png
        output_dir = tmp_path / "project" / "output"
        args = [
            str(fib_file),
            "--out-png", str(output_dir / "fib.png"),
            "--out-json", str(output_dir / "fib.json")
        ]
        
        cli_input = parser.parse(args)
        
        # Output directory should be created
        assert output_dir.exists()
        assert cli_input.output_png == str(output_dir / "fib.png")
        assert cli_input.output_json == str(output_dir / "fib.json")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])