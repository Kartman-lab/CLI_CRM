from rich.console import Console
from app.crud.auth_manager import load_session, get_user_from_token

console = Console()

def whoami_view():
    token = load_session()
    if not token:
        console.print("[red]Aucune session trouvée. Veuillez vous connecter.[/red]")
        return

    user = get_user_from_token(token)
    if not user:
        console.print("[red]Session invalide ou expirée. Veuillez vous reconnecter.[/red]")
        return

    console.print(f"[bold green]Utilisateur connecté :[/bold green] {user.prenom} {user.nom}")
    console.print(f"[bold blue]Email :[/bold blue] {user.email}")
    console.print(f"[bold magenta]Rôle :[/bold magenta] {user.role.nom}")
