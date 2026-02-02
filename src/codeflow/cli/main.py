import argparse
import os

from codeflow.core.runner import Runner
from codeflow.core.serialization import export_json
from codeflow.viz.graphviz_export import  export_callgraph_png


def main():
    parser = argparse.ArgumentParser(description="Trace Python file and export JSON + call graph PNG.")
    parser.add_argument("file", help="Path to a Python file to execute and trace.")
    parser.add_argument("--out-json", default=None, help="Output JSON path (default: <file>.trace.json)")
    parser.add_argument("--out-png", default=None, help="Output PNG path (default: <file>.callgraph.png)")
    parser.add_argument("--show-module", action="store_true", help="Include <module> node in the call graph.")
    args = parser.parse_args()

    py_file = os.path.abspath(args.file)
    if not os.path.exists(py_file):
        raise SystemExit(f"File not found: {py_file}")

    base = os.path.splitext(py_file)[0]
    out_json = args.out_json or (base + ".trace.json")
    out_png = args.out_png or (base + ".callgraph.png")

    runner = Runner()
    result = runner.run_file(py_file)

    export_json(result, out_json)
    export_callgraph_png(
        result,
        out_png,
        title=os.path.basename(py_file),
        hide_module=(not args.show_module),
    )

    print("✅ Done")
    print("status:", result.status)
    print("json  :", out_json)
    print("png   :", out_png)
    if result.error:
        print("\n--- error ---\n")
        print(result.error)


if __name__ == "__main__":
    main()
