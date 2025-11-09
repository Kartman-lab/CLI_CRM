from rich.console import Console
from app.crud.contracts_manager import get_all_contracts, get_contract_by_commercial
from app.crud.clients_manager import create_client, get_all_clients
from app.controllers.clients_controller import ClientController
from app.controllers.contracts_controller import ContractsController
from app.controllers.events_controller import EventsController
from app.crud.auth_manager import clear_session

console = Console()

def commercial_menu(user):
    client_controller = ClientController(user)
    contracts_controller = ContractsController(user)
    events_controller = EventsController(user)
    while True:
        console.print("\n[bold blue]=== Menu Commercial ===[/bold blue]")
        console.print("1. Afficher tous les clients")
        console.print("2. Créer un client")
        console.print("3. Modifier un client")
        console.print("4. Afficher tous les contrats")
        console.print("5. Afficher contrats non signés")
        console.print("6. Afficher contrats non payés")
        console.print("7. Créer un événement")
        console.print("8. Déconnexion")

        choix = input("> ")

        if choix == "1":
            clients = get_all_clients(user)
            client_controller.client_talbe(clients, "Clients")
        elif choix == "2":
            data = client_controller.prompt_client_data()
            client_controller.create_client(data)
        elif choix == "3":
            client_id = client_controller.prompt_udpate_client_data()
            client_controller.updates_client(client_id)
        elif choix == "4":
            contracts = get_contract_by_commercial(user, user.id)
            contracts_controller.contract_table(contracts, "Contrats")
        elif choix == "5":
            contracts_controller.show_not_signed_contracts()
        elif choix == "6":
            contracts_controller.show_not_fully_payed_contracts()
        elif choix == "7":
            events_controller.create_event_for_client()
        elif choix == "8":
            clear_session()
            console.print("[yellow]Déconnexion réussie.[/yellow]")
            break 
        else:
            console.print("Entrée invalide")
            continue
        




       