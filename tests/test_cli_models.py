"""
Comprehensive unit tests for CLI models v2 (with Enum).

This test suite covers:
- CliInput creation and validation
- CliOutput creation and validation
- OutputStatus enum functionality
- Helper methods
- Edge cases
- Integration scenarios

Run with: pytest test_cli_models_v2.py -v
"""

import pytest
from pathlib import Path
from codeflow.cli.models import CliInput, CliOutput, OutputStatus


# ============================================================================
# OutputStatus Enum Tests
# ============================================================================

class TestOutputStatusEnum:
    """Test suite for OutputStatus enum."""
    
    def test_has_success_member(self):
        """Test that OutputStatus has SUCCESS member."""
        assert hasattr(OutputStatus, 'SUCCESS')
        assert OutputStatus.SUCCESS.value == "success"
    
    def test_has_error_member(self):
        """Test that OutputStatus has ERROR member."""
        assert hasattr(OutputStatus, 'ERROR')
        assert OutputStatus.ERROR.value == "error"
    
    def test_create_from_string(self):
        """Test creating OutputStatus from string value."""
        success = OutputStatus("success")
        error = OutputStatus("error")
        
        assert success == OutputStatus.SUCCESS
        assert error == OutputStatus.ERROR
    
    def test_invalid_value_raises_error(self):
        """Test that invalid string raises ValueError."""
        with pytest.raises(ValueError):
            OutputStatus("invalid")
    
    def test_enum_comparison(self):
        """Test OutputStatus enum comparison."""
        assert OutputStatus.SUCCESS == OutputStatus.SUCCESS
        assert OutputStatus.ERROR == OutputStatus.ERROR
        assert OutputStatus.SUCCESS != OutputStatus.ERROR
    
    def test_inherits_from_string(self):
        """Test that OutputStatus inherits from str."""
        assert isinstance(OutputStatus.SUCCESS, str)
        assert isinstance(OutputStatus.ERROR, str)


# ============================================================================
# CliInput Tests - Creation
# ============================================================================

class TestCliInputCreation:
    """Test suite for CliInput creation."""
    
    def test_minimal_creation(self):
        """Test creating CliInput with minimal required fields."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="test.png"
        )
        
        assert cli_input.source_file == "test.py"
        assert cli_input.output_png == "test.png"
        assert cli_input.output_json is None
        assert cli_input.show_module is False
        assert cli_input.verbose is False
    
    def test_full_creation(self):
        """Test creating CliInput with all fields."""
        cli_input = CliInput(
            source_file="examples/fib.py",
            output_png="fib.callgraph.png",
            output_json="fib.trace.json",
            show_module=True,
            verbose=True
        )
        
        assert cli_input.source_file == "examples/fib.py"
        assert cli_input.output_png == "fib.callgraph.png"
        assert cli_input.output_json == "fib.trace.json"
        assert cli_input.show_module is True
        assert cli_input.verbose is True


# ============================================================================
# CliInput Tests - Validation
# ============================================================================

class TestCliInputValidation:
    """Test suite for CliInput validation."""
    
    def test_empty_source_file_raises_error(self):
        """Test that empty source_file raises ValueError."""
        with pytest.raises(ValueError, match="source_file cannot be empty"):
            CliInput(source_file="", output_png="out.png")
    
    def test_empty_output_png_raises_error(self):
        """Test that empty output_png raises ValueError."""
        with pytest.raises(ValueError, match="output_png cannot be empty"):
            CliInput(source_file="test.py", output_png="")
    
    def test_empty_output_json_string_raises_error(self):
        """Test that empty string for output_json raises ValueError."""
        with pytest.raises(ValueError, match="output_json cannot be an empty string"):
            CliInput(
                source_file="test.py",
                output_png="out.png",
                output_json=""
            )
    
    def test_source_file_wrong_type_raises_error(self):
        """Test that non-string source_file raises ValueError."""
        with pytest.raises(ValueError, match="source_file must be a string"):
            CliInput(source_file=123, output_png="out.png") # type: ignore
    
    def test_output_png_wrong_type_raises_error(self):
        """Test that non-string output_png raises ValueError."""
        with pytest.raises(ValueError, match="output_png must be a string"):
            CliInput(source_file="test.py", output_png=12) # type: ignore
    
    def test_show_module_wrong_type_raises_error(self):
        """Test that non-boolean show_module raises ValueError."""
        with pytest.raises(ValueError, match="show_module must be a boolean"):
            CliInput(
                source_file="test.py",
                output_png="out.png",
                show_module="yes"# type: ignore
            )
    
    def test_verbose_wrong_type_raises_error(self):
        """Test that non-boolean verbose raises ValueError."""
        with pytest.raises(ValueError, match="verbose must be a boolean"):
            CliInput(
                source_file="test.py",
                output_png="out.png",
                verbose=1 # type: ignore
            )


# ============================================================================
# CliInput Tests - Helper Methods
# ============================================================================

class TestCliInputHelperMethods:
    """Test suite for CliInput helper methods."""
    
    def test_is_json_export_enabled_true(self):
        """Test is_json_export_enabled returns True when JSON is set."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="out.png",
            output_json="trace.json"
        )
        assert cli_input.is_json_export_enabled() is True
    
    def test_is_json_export_enabled_false(self):
        """Test is_json_export_enabled returns False when JSON is None."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="out.png"
        )
        assert cli_input.is_json_export_enabled() is False
    
    def test_get_source_filename_with_path(self):
        """Test get_source_filename extracts filename from path."""
        cli_input = CliInput(
            source_file="examples/subfolder/fib.py",
            output_png="out.png"
        )
        assert cli_input.get_source_filename() == "fib.py"
    
    def test_get_source_filename_without_path(self):
        """Test get_source_filename with no directory path."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="out.png"
        )
        assert cli_input.get_source_filename() == "test.py"
    
    def test_get_output_png_path(self):
        """Test get_output_png_path returns Path object."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="output/graph.png"
        )
        path = cli_input.get_output_png_path()
        assert isinstance(path, Path)
        assert str(path) == "output/graph.png"
    
    def test_get_output_json_path_with_json(self):
        """Test get_output_json_path returns Path when JSON is set."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="out.png",
            output_json="trace.json"
        )
        path = cli_input.get_output_json_path()
        assert isinstance(path, Path)
        assert str(path) == "trace.json"
    
    def test_get_output_json_path_without_json(self):
        """Test get_output_json_path returns None when JSON not set."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="out.png"
        )
        path = cli_input.get_output_json_path()
        assert path is None


# ============================================================================
# CliInput Tests - Immutability
# ============================================================================

class TestCliInputImmutability:
    """Test suite for CliInput immutability."""
    
    def test_is_frozen(self):
        """Test that CliInput is immutable (frozen)."""
        cli_input = CliInput(
            source_file="test.py",
            output_png="out.png"
        )
        
        with pytest.raises(AttributeError):
            cli_input.source_file = "changed.py" # type: ignore
        
        with pytest.raises(AttributeError):
            cli_input.verbose = True # type: ignore


# ============================================================================
# CliOutput Tests - Creation
# ============================================================================

class TestCliOutputCreation:
    """Test suite for CliOutput creation."""
    
    def test_success_creation(self):
        """Test creating success CliOutput with enum."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Trace completed",
            png_path="graph.png",
            json_path="trace.json"
        )
        
        assert output.status == OutputStatus.SUCCESS
        assert output.message == "Trace completed"
        assert output.png_path == "graph.png"
        assert output.json_path == "trace.json"
        assert output.error_details is None
    
    def test_error_creation(self):
        """Test creating error CliOutput with enum."""
        output = CliOutput(
            status=OutputStatus.ERROR,
            message="Execution failed",
            error_details="FileNotFoundError: file.py not found"
        )
        
        assert output.status == OutputStatus.ERROR
        assert output.message == "Execution failed"
        assert output.png_path is None
        assert output.json_path is None
        assert output.error_details == "FileNotFoundError: file.py not found"


# ============================================================================
# CliOutput Tests - Validation
# ============================================================================

class TestCliOutputValidation:
    """Test suite for CliOutput validation."""
    
    def test_wrong_status_type_raises_error(self):
        """Test that string status (not enum) raises TypeError."""
        with pytest.raises(TypeError, match="status must be OutputStatus enum"):
            CliOutput(
                status="success",  # # type: ignore Wrong! Should be OutputStatus.SUCCESS
                message="Test",
                png_path="out.png"
            )
    
    def test_empty_message_raises_error(self):
        """Test that empty message raises ValueError."""
        with pytest.raises(ValueError, match="message cannot be empty"):
            CliOutput(
                status=OutputStatus.SUCCESS,
                message="",
                png_path="out.png"
            )
    
    def test_success_without_png_raises_error(self):
        """Test that SUCCESS status requires png_path."""
        with pytest.raises(ValueError, match="SUCCESS status requires png_path"):
            CliOutput(
                status=OutputStatus.SUCCESS,
                message="Done"
            )


# ============================================================================
# CliOutput Tests - Helper Methods
# ============================================================================

class TestCliOutputHelperMethods:
    """Test suite for CliOutput helper methods."""
    
    def test_is_success(self):
        """Test is_success method."""
        success = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="out.png"
        )
        error = CliOutput(
            status=OutputStatus.ERROR,
            message="Failed"
        )
        
        assert success.is_success() is True
        assert error.is_success() is False
    
    def test_is_error(self):
        """Test is_error method."""
        success = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="out.png"
        )
        error = CliOutput(
            status=OutputStatus.ERROR,
            message="Failed"
        )
        
        assert error.is_error() is True
        assert success.is_error() is False
    
    def test_has_json_output_true(self):
        """Test has_json_output returns True when JSON is set."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="graph.png",
            json_path="trace.json"
        )
        assert output.has_json_output() is True
    
    def test_has_json_output_false(self):
        """Test has_json_output returns False when JSON is None."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="graph.png"
        )
        assert output.has_json_output() is False
    
    def test_get_all_output_paths_both(self):
        """Test get_all_output_paths with both PNG and JSON."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="graph.png",
            json_path="trace.json"
        )
        paths = output.get_all_output_paths()
        assert paths == ["graph.png", "trace.json"]
    
    def test_get_all_output_paths_png_only(self):
        """Test get_all_output_paths with only PNG."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="graph.png"
        )
        paths = output.get_all_output_paths()
        assert paths == ["graph.png"]
    
    def test_get_all_output_paths_error(self):
        """Test get_all_output_paths returns empty list for error."""
        output = CliOutput(
            status=OutputStatus.ERROR,
            message="Failed"
        )
        paths = output.get_all_output_paths()
        assert paths == []


# ============================================================================
# CliOutput Tests - String Representation
# ============================================================================

class TestCliOutputStringRepresentation:
    """Test suite for CliOutput string representation."""
    
    def test_str_success(self):
        """Test __str__ for success output."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Trace completed",
            png_path="out.png"
        )
        result = str(output)
        assert "✅" in result
        assert "Trace completed" in result
    
    def test_str_error(self):
        """Test __str__ for error output."""
        output = CliOutput(
            status=OutputStatus.ERROR,
            message="Execution failed"
        )
        result = str(output)
        assert "❌" in result
        assert "Execution failed" in result


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests combining CliInput and CliOutput."""
    
    def test_workflow_success(self):
        """Test complete workflow: input → success output."""
        # Create input
        cli_input = CliInput(
            source_file="fib.py",
            output_png="fib.callgraph.png",
            output_json="fib.trace.json",
            verbose=True
        )
        
        # Create success output
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Trace completed",
            png_path=cli_input.output_png,
            json_path=cli_input.output_json
        )
        
        # Verify
        assert output.is_success()
        assert output.png_path == "fib.callgraph.png"
        assert output.json_path == "fib.trace.json"
        assert len(output.get_all_output_paths()) == 2
    
    def test_workflow_error(self):
        """Test complete workflow: input → error output."""
        cli_input = CliInput(
            source_file="missing.py",
            output_png="out.png"
        )
        
        output = CliOutput(
            status=OutputStatus.ERROR,
            message="File not found",
            error_details=f"FileNotFoundError: {cli_input.source_file}"
        )
        
        assert output.is_error()
        assert "missing.py" in output.error_details # type: ignore


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and corner scenarios."""
    
    def test_cli_input_special_characters_in_path(self):
        """Test CliInput with special characters in file paths."""
        cli_input = CliInput(
            source_file="examples/test-file_v2.py",
            output_png="output/graph-v1_final.png"
        )
        assert cli_input.source_file == "examples/test-file_v2.py"
        assert cli_input.get_source_filename() == "test-file_v2.py"
    
    def test_cli_input_absolute_path(self):
        """Test CliInput with absolute paths."""
        cli_input = CliInput(
            source_file="/home/user/projects/code-flow/examples/fib.py",
            output_png="/tmp/output.png"
        )
        assert cli_input.source_file.startswith("/")
        assert cli_input.get_source_filename() == "fib.py"
    
    def test_cli_output_long_message(self):
        """Test CliOutput with very long message."""
        long_message = "Error: " + "x" * 1000
        output = CliOutput(
            status=OutputStatus.ERROR,
            message=long_message
        )
        assert len(output.message) == len(long_message)
    
    def test_cli_output_multiline_error_details(self):
        """Test CliOutput with multiline error details."""
        error_details = """Traceback (most recent call last):
  File "test.py", line 10, in <module>
    raise ValueError("Test error")
ValueError: Test error"""
        
        output = CliOutput(
            status=OutputStatus.ERROR,
            message="Execution failed",
            error_details=error_details
        )
        assert "\n" in output.error_details # type: ignore
        assert "Traceback" in output.error_details # type: ignore


# ============================================================================
# Type Safety Tests (Enum-specific)
# ============================================================================

class TestTypeSafety:
    """Test type safety features with Enum."""
    
    def test_enum_type_safe_comparison(self):
        """Test that enum enables type-safe comparison."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="out.png"
        )
        
        # Type-safe comparison with enum
        assert output.status == OutputStatus.SUCCESS
        assert output.status != OutputStatus.ERROR
        
        # Can also access string value
        assert output.status.value == "success"
    
    def test_enum_serialization(self):
        """Test that enum can be serialized to string."""
        output = CliOutput(
            status=OutputStatus.SUCCESS,
            message="Done",
            png_path="out.png"
        )
        
        # Get string value for JSON serialization
        status_str = output.status.value
        assert status_str == "success"
        assert isinstance(status_str, str)
        
        # Can recreate enum from string
        status_enum = OutputStatus(status_str)
        assert status_enum == OutputStatus.SUCCESS