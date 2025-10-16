from rich.console import Console
from core.interface import SynWeaveInterface


def main():
    try:
        app = SynWeaveInterface()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()