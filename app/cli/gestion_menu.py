from rich.console import Console

from app.utils import clear_console
from app.crud.auth_manager import clear_session
from app.controllers.collaborateur_controller import CollaborateurController
from app.controllers.contracts_controller import ContractsController
from app.controllers.events_controller import EventsController
from app.crud.collaborateurs_manager import get_all_collaborateurs
from app.crud.contracts_manager import get_all_contracts
from app.crud.events_manager import get_all_events, get_events_without_support

console = Console()

def gestion_menu(user):
    while True:
        console.print("\n[bold blue]=== Menu Gestionnaire ===[/bold blue]")
        console.print("1. Gestion des collaborateurs")
        console.print("2. Gestion des contrats")
        console.print("3. Gestion des évènements")
        console.print("4. Déconnexion")

        choix = input(">")

        if choix== "1":
            clear_console()
            gestion_collaborateurs(user)
        elif choix == "2":
            clear_console()
            gestion_contrats(user)
        elif choix == "3":
            clear_console()
            gestion_events(user)
        elif choix == "4":
            clear_session()
            console.print("[yellow]Déconnexion réussie.[/yellow]")
            break 
        else:
            console.print("[red]Veuillez entrer une option valide[/red]")
            continue


def gestion_collaborateurs(user):
    collaborateur_controller = CollaborateurController(user)
    while True:
        console.print("[bold blue]=== Gesiton des collaborateurs ===[/bold blue]")
        console.print("1. Afficher les collaborateurs")
        console.print("2. Créer un collaborateur")
        console.print("3. Modifier un collaborateur")
        console.print("4. Supprimer un collaborateur")
        console.print("5. Retour")

        choix = input(">")

        if choix == "1":
            clear_console()
            collaborateurs = get_all_collaborateurs(user)
            collaborateur_controller.collaborateur_table(collaborateurs, "Collaborateurs")
        elif choix== "2":
            clear_console()
            data = collaborateur_controller.prompt_data_collaborateur()
            collaborateur_controller.create_collaborateur(data)
        elif choix == "3":
            clear_console()
            data = collaborateur_controller.prompt_update_collaborateur()
            collaborateur_controller.update_collaborateur(data)
        elif choix == "4":
            collaborateur_controller.delete_collaborateur()
        elif choix.upper() == "5":
            clear_console()
            return 
        else:
            console.print("[red]Veuillez entrer une option valide[/red]")
            continue


def gestion_contrats(user):
    contract_controller = ContractsController(user)
    while True:
        console.print("[bold blue]=== Gesiton des contrats ===[/bold blue]")
        console.print("1. Afficher les contrats")
        console.print("2. Créer un contrat")
        console.print("3. Modifier un contrat")
        console.print("4. Retour")

        choix = input(">")

        if choix == "1":
            clear_console()
            contracts = get_all_contracts(user)
            contract_controller.contract_table(contracts, "Contrats")
        elif choix == "2":
            clear_console()
            contract_controller.create_contract()
        elif choix == "3":
            clear_console()
            contract_controller.update_contract()
        elif choix == "4":
            clear_console()
            break
        else: 
            console.print("[red]Veuillez entrer une option valide[/red]")
            continue



def gestion_events(user):
    event_controller = EventsController(user)
    while True:
        console.print("[bold blue]=== Gesiton des évènements ===[/bold blue]")
        console.print("1. Afficher tous les évènements")
        console.print("2. Afficher tous les évènements qui n'ont pas de support associé")
        console.print("3) Associer un support à un évènement")
        console.print("4. Retour")

        choix = input(">")

        if choix == "1":
            clear_console()
            events = get_all_events(user)
            event_controller.event_table(events, "Évènements")
        elif choix == "2":
            clear_console()
            events = get_events_without_support(user)
            event_controller.event_table(events, "Évènements sans supprot associé")
        elif choix == "3":
            clear_console()
            event_controller.associate_support_to_event()
        elif choix == "4":
            clear_console()
            break
        else: 
            console.print("[red]Veuillez entrer une option valide[/red]")
            continue






