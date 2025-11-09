from rich.console import Console
import os
import platform

console = Console()

def quit_fonction(label:str):
    value= input(f"{label} >").strip()
    if value.lower() == "q":
        raise KeyboardInterrupt("Opération annulée.")
    return value 


def clear_console():
    """
    Nettoie l'écran du terminal.
    Compatible Windows, macOS et Linux.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")