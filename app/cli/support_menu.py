from rich.console import Console
from app.utils import clear_console
from app.controllers.events_controller import EventsController
from app.crud.events_manager import get_my_events
from app.crud.auth_manager import clear_session

console = Console()

def support_menu(user):
    event_controller = EventsController(user)

    while True:
        console.print("\n[bold blue]=== Menu Support ===[/bold blue]")
        console.print("1. Afficher mes évènements")
        console.print("2. Mettre à jour un évènement")
        console.print("3. Déconnexion")

        choix = input(">")

        if choix == "1":
            clear_console()
            events = get_my_events(user)
            if not events:
                console.print("[yellow]Aucun évènement ne vous appartient.[/yellow]")
            else:
                event_controller.event_table(events, "Mes évènements")
        elif choix == "2":
            clear_console()
            event_id = event_controller.get_event_id()
            event_controller.update_my_event(event_id)
        elif choix == "3":
            clear_session()
            console.print("[yellow]Déconnexion réussie.[/yellow]")
            break 
        else:
            console.print("Entrée invalide")
            continue
        

