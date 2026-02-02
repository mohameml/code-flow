import json
from dataclasses import asdict

# Adapte l'import selon ton projet, ex:
# from core.runner import Runner
# Ici j'assume que Runner est accessible directement.

from codeflow.core.runner import Runner

def dump_runresult(result, title: str, max_events: int = 40):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print("STATUS:", result.status)
    if result.error:
        print("ERROR:\n", result.error)

    print(f"\nNodes: {len(result.nodes)} | Edges: {len(result.edges)} | Events: {len(result.events)}")

    # Affiche quelques nodes
    print("\n--- First nodes ---")
    for n in result.nodes[:10]:
        print(
            f"node#{n.id} func={n.func_name} args={n.args} "
            f"return={n.return_value} exc={n.exception}"
        )

    # Affiche quelques edges
    print("\n--- First edges ---")
    for e in result.edges[:15]:
        print(f"{e.parent_id} -> {e.child_id}")

    # Affiche quelques events
    print("\n--- First events ---")
    for ev in result.events[:max_events]:
        print(
            f"ev#{ev.id} {ev.type:<9} node={ev.node_id} "
            f"{ev.func_name}:{ev.lineno} locals={ev.locals} arg={ev.arg}"
        )

    # Dump JSON (optionnel)
    payload = {
        "status": result.status,
        "error": result.error,
        "nodes": [asdict(n) for n in result.nodes],
        "edges": [asdict(e) for e in result.edges],
        "events": [asdict(ev) for ev in result.events],
    }
    print("\n--- JSON preview (truncated) ---")
    s = json.dumps(payload, ensure_ascii=False)
    # print(s[:1200] + ("..." if len(s) > 1200 else ""))
    print(s)


def test_simple_function():
    runner = Runner()

    code = """
a = 1
def f(n):
    x = n + 1
    return x

# exécution directe (pas besoin d'entrypoint)
print("f(2) =", f(2))
"""
    result = runner.run(code ,"<user-code>")

    # Assertions basiques
    assert result.status == "ok"
    assert len(result.events) > 0
    assert any(ev.type == "call" and ev.func_name == "f" for ev in result.events)
    assert any(ev.type == "return" and ev.func_name == "f" for ev in result.events)

    dump_runresult(result, "TEST 1 — Simple function f(n)")


def test_recursive_fib():
    runner = Runner()

    code = """
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print("fib(4) =", fib(4))
"""
    result = runner.run(code  ,"<user-code>")

    # Assertions basiques
    assert result.status == "ok"
    assert any(ev.type == "call" and ev.func_name == "fib" for ev in result.events)
    assert any(ev.type == "return" and ev.func_name == "fib" for ev in result.events)
    assert len(result.nodes) >= 1
    assert len(result.edges) >= 1  # récursion => normalement des edges

    dump_runresult(result, "TEST 2 — Recursive Fibonacci fib(4)")


if __name__ == "__main__":
    # test_simple_function()
    test_recursive_fib()
    print("\n✅ All tests passed.")
