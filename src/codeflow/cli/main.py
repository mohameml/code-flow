# import argparse
# import os

# from codeflow.core.runner import Runner
# from codeflow.core.serialization import export_json
# from codeflow.viz.graphviz_export import  export_callgraph_png


# def main():
#     parser = argparse.ArgumentParser(description="Trace Python file and export JSON + call graph PNG.")
#     parser.add_argument("file", help="Path to a Python file to execute and trace.")
#     parser.add_argument("--out-json", default=None, help="Output JSON path (default: <file>.trace.json)")
#     parser.add_argument("--out-png", default=None, help="Output PNG path (default: <file>.callgraph.png)")
#     parser.add_argument("--show-module", action="store_true", help="Include <module> node in the call graph.")
#     args = parser.parse_args()

#     py_file = os.path.abspath(args.file)
#     if not os.path.exists(py_file):
#         raise SystemExit(f"File not found: {py_file}")

#     base = os.path.splitext(py_file)[0]
#     out_json = args.out_json or (base + ".trace.json")
#     out_png = args.out_png or (base + ".callgraph.png")

#     runner = Runner()
#     result = runner.run_file(py_file)

#     export_json(result, out_json)
#     export_callgraph_png(
#         result,
#         out_png,
#         title=os.path.basename(py_file),
#         hide_module=(not args.show_module),
#     )

#     print("✅ Done")
#     print("status:", result.status)
#     print("json  :", out_json)
#     print("png   :", out_png)
#     if result.error:
#         print("\n--- error ---\n")
#         print(result.error)


# if __name__ == "__main__":
#     main()
import sys
from typing import Optional

from codeflow.cli.parser import Parser
from codeflow.cli.output import OutputHandler
from codeflow.core.runner import Runner
from codeflow.core.serialization import export_json
from codeflow.viz.graphviz_export import export_callgraph_png


def main(args: Optional[list] = None) -> int:
    """
    CLI entry point.
    
    Orchestrates the entire workflow:
    1. Parse and validate arguments
    2. Execute and trace Python file
    3. Generate visualizations
    4. Display results
    
    Args:
        args: Command-line arguments (None = sys.argv)
        
    Returns:
        Exit code (0 = success, 1 = error)
    """
    try:
        # Step 1: Parse input
        parser = Parser()
        cli_input = parser.parse(args)
        
        # Step 2: Create output handler
        output_handler = OutputHandler(verbose=cli_input.verbose)
        
        # Step 3: Execute and trace
        runner = Runner()
        result = runner.run_file(cli_input.source_file)
        
        # Step 4: Check execution status
        if result.status != "ok":
            output = output_handler.format_error(
                Exception("Execution error"),
                error_details=result.error
            )
            output_handler.display(output)
            return 1
        
        # Step 5: Generate PNG
        export_callgraph_png(
            result,
            cli_input.output_png,
            title=cli_input.source_file,
            hide_module=(not cli_input.show_module)
        )
        
        # Step 6: Generate JSON (if requested)
        if cli_input.output_json:
            export_json(result, cli_input.output_json)
        
        # Step 7: Display success
        output = output_handler.format_success(
            png_path=cli_input.output_png,
            json_path=cli_input.output_json,
            result=result if cli_input.verbose else None
        )
        output_handler.display(output)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1
    
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        if "--verbose" in (args or sys.argv):
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())