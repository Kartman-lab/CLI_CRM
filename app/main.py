import click
import sentry_sdk
import random
from rich.console import Console
from app.sentry.config_sentry import *
from app.security.permission import require_role
from app.cli.auth_cli import login_view
from app.cli.commecial_menu import commercial_menu as commercial_menu_view
from app.cli.gestion_menu import gestion_menu as gestion_menu_view
from app.cli.support_menu import support_menu as support_menu_view
from app.crud.auth_manager import get_user_from_token, load_session
from app.cli.whoami import whoami_view

console = Console()

@click.group()
def cli():
    """Application CRM en ligne de commande."""
    pass

@click.command()
def login():
    login_view()

def get_user():
    token = load_session()
    if not token:
        console.print("[red]Aucun utilisateur connecté. Veuillez vous connecter d'abord avec 'login'.[/red]")
        return
    
    user = get_user_from_token(token)
    if not user:
        console.print("[red]Session invalide ou expirée. Veuillez vous reconnecter.[/red]")
        return
    
    console.print(f"Vous etes connecté {user.nom} en tant que {user.role.nom}")
    return user 

@click.command()
def whoami():
    """Afficher l'utilisateur actuellement connecté"""
    whoami_view()

@click.command()
def commercial_menu():
    user = get_user()
    if user.role.nom != 'commercial':
        console.print("[red]Accès refusé : vous n'êtes pas commercial[/red]")
        return

    commercial_menu_view(user)

@click.command()
def gestion_menu():
    user = get_user()
    if user.role.nom != 'gestion':
        console.print("[red]Accès refusé : vous n'êtes pas membre de l'équipe de gestion.[/red]")
        return

    gestion_menu_view(user)

@click.command()
def support_menu():
    user = get_user()
    if user.role.nom != 'support':
        console.print("[red]Accès refusé : vous n'êtes pas membre de l'équipe de support.[/red]")
        return
    support_menu_view(user)


cli.add_command(login)
cli.add_command(whoami)
cli.add_command(commercial_menu)
cli.add_command(gestion_menu)
cli.add_command(support_menu)

# simuler un utilisateur CLI pour Release Health
sentry_sdk.set_user({
    "id": random.randint(1, 1000),
    "username": f"user{random.randint(1, 1000)}"
})

# Démarrer une session
sentry_sdk.start_session()

if __name__ == "__main__":
    try:
        cli()  # CRM CLI
    except Exception as e:
        sentry_sdk.capture_exception(e)  # envoie le crash à Sentry
        raise
    finally:
        # Terminer la session pour que Release Health la voie
        sentry_sdk.end_session()