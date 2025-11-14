from getpass import getpass
from rich.console import Console
from app.crud.auth_manager import login_user

console = Console()

def login_view():
    console.print("[bold blue]=== Connexion === [/bold blue]")
    email = input("Email : ")
    password = getpass("Mot de passe : ")

    user = login_user(email, password)

    if not user:
        console.print("[red] Email ou mot de passe non valide.[/red]")
        return 
    console.print(f"[green] Bienvenue {user.prenom} ({user.role.nom})[/green]")
    return user
