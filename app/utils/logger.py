def get_logger(name: str):
    class DummyLogger:
        def info(self, msg):
            print(f"[INFO] {msg}")

        def error(self, msg):
            print(f"[ERROR] {msg}")

        def warning(self, msg):
            print(f"[WARNING] {msg}")

    return DummyLogger()


logger = get_logger("default")
