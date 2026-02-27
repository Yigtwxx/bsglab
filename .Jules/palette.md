## 2025-02-27 - Graceful Exits in CLI Tools
**Learning:** In CLI applications, users often use `Ctrl+C` or `Ctrl+D` to quickly exit an interactive prompt. By default, Python throws a jarring `KeyboardInterrupt` or `EOFError` traceback, which breaks the illusion of a polished application and looks like a crash.
**Action:** Always wrap interactive CLI loops in a `try-except` block to catch `KeyboardInterrupt` and `EOFError`, providing a clean, friendly exit message instead.
