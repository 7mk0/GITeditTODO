import json, sys, pathlib
DB = pathlib.Path("tasks.json")

def load():
    return json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else []

def save(tasks):
    DB.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")

def add(text):
    tasks = load()
    tasks.append({"text": text, "done": False, "prio": 2, "due": None})
    save(tasks)
    print("Aggiunto:", text)

def list_():
    tasks = sorted(load(), key=lambda t: (t["done"], t["prio"]))
    for i, t in enumerate(tasks, 1):
        status = "✓" if t["done"] else "·"
        prio = f"P{t['prio']}"
        due  = f" (due {t['due']})" if t["due"] else ""
        print(f"{i}. [{status}] {prio} {t['text']}{due}")

def done(i):
    tasks = load()
    idx = int(i)-1
    tasks[idx]["done"] = True
    save(tasks)
    print("Completato:", tasks[idx]["text"])

def prio(i, level):
    tasks = load()
    idx = int(i)-1
    tasks[idx]["prio"] = int(level)
    save(tasks)
    print("Priorità aggiornata:", tasks[idx]["text"], "→ P", level)

def due(i, date_yyyy_mm_dd):
    tasks = load()
    idx = int(i)-1
    tasks[idx]["due"] = date_yyyy_mm_dd
    save(tasks)
    print("Scadenza aggiornata:", tasks[idx]["text"], "→", date_yyyy_mm_dd)

def help_():
    print("Comandi:")
    print("  add <testo>           - aggiunge un task")
    print("  list                  - elenca i task (ordina per done, prio)")
    print("  done <n>              - marca completato")
    print("  prio <n> <1-3>        - imposta priorità (1 alta, 3 bassa)")
    print("  due  <n> <YYYY-MM-DD> - imposta scadenza")
    print("Esempi:")
    print('  python todo.py add "comprare resina"')
    print("  python todo.py prio 1 1")
    print("  python todo.py due  1 2025-12-31")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args: returncode = help_()
    else:
        cmd, *rest = args
        if   cmd == "add":  add(" ".join(rest))
        elif cmd == "list": list_()
        elif cmd == "done": done(rest[0])
        elif cmd == "prio": prio(rest[0], rest[1])
        elif cmd == "due":  due(rest[0],  rest[1])
        else: help_()
