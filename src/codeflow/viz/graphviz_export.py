from graphviz import Digraph

from codeflow.core.models import RunResult


def export_callgraph_png(
    result: RunResult,
    out_png: str,
    title: str = "Call Graph",
    hide_module: bool = True
) -> None:
    dot = Digraph("callgraph", format="png")
    dot.attr(label=title, labelloc="t", fontsize="18")

    # Optionnel: cacher le node <module> pour un graphe plus “DP”
    hidden_ids = set()
    if hide_module:
        for n in result.nodes:
            if n.func_name == "<module>":
                hidden_ids.add(n.id)

    # Nodes
    for n in result.nodes:
        if n.id in hidden_ids:
            continue
        label = f"{n.func_name}\\n#{n.id}"
        if n.args:
            # arguments (repr)
            args_str = ", ".join(f"{k}={v}" for k, v in n.args.items())
            label += f"\\n({args_str})"
        if n.return_value is not None:
            label += f"\\nret={n.return_value}"
        if n.exception is not None:
            label += f"\\nEXC: {n.exception}"

        dot.node(str(n.id), label=label, shape="box")

    # Edges
    for e in result.edges:
        if e.parent_id in hidden_ids or e.child_id in hidden_ids:
            # si on cache <module>, on peut soit skip,
            # soit relier les enfants à un root virtuel (plus tard)
            continue
        dot.edge(str(e.parent_id), str(e.child_id))

    # Rendu : graphviz écrit out_png via render()
    # graphviz ajoute un suffixe, on contrôle avec filename sans extension
    if out_png.lower().endswith(".png"):
        out_base = out_png[:-4]
    else:
        out_base = out_png

    dot.render(out_base, cleanup=True)
