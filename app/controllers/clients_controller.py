from app.crud.clients_manager import create_client as crud_create_client, update_client as crud_update_client
from app.crud.clients_manager import get_client_by_id
from app.utils import quit_fonction
from rich.console import Console 
from rich.table import Table

console = Console()

class ClientController:
    def __init__(self, current_user):
        self.user = current_user

    def client_talbe(self, clients, title):
        table = Table(show_header=True, header_style="bold magenta", title=title)
        table.add_column("ID")
        table.add_column("Fullname")
        table.add_column("email")
        table.add_column("Telephone")
        table.add_column("Entreprise")
        table.add_column("Date ce création")
        table.add_column("Dernière mise à jour")

        for c in clients:
            table.add_row(
                str(c.id),
                c.fullname,
                c.email,
                c.telephone,
                c.entreprise,
                str(c.date_created),
                str(c.date_updated) 
            )

        console.print(table)

    def prompt_client_data(self):
        console.print("[bold blue]=== Création d’un nouveau client ===[/bold blue]")
        console.print("'Q' pour quitter")
        fullname = quit_fonction("Nom complet : ")
        email = quit_fonction("Email : ")
        telephone = quit_fonction("Téléphone : ")
        entreprise = quit_fonction("Entreprise : ")
        contract_id = quit_fonction("Id du contrat :")
        event_id = quit_fonction("Id de l'évènement : ")

        data = {
            "fullname": fullname,
            "email": email,
            "telephone": telephone,
            "entreprise": entreprise,
            "commercial_id": self.user.id,
            "contract_id": int(contract_id) if contract_id else None,
            "event_id": int(event_id) if event_id else None
        }
        return data
    
    def prompt_udpate_client_data(self):
        console.print("[bold blue]=== Modification d'un client ===[/bold blue]")
        client_id = quit_fonction("Entrer l'id du client ('Q' pour retour) > ")
        return client_id 
    
    
    def updates_client(self, client_id):
        try:
            client = get_client_by_id(client_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return
        
        console.print("Entrer les nouveaux champs (laisser vide pour ne pas modifier) :")
        fullname = quit_fonction(f"Nom complet [{client.fullname}] : ")
        email = quit_fonction(f"Email [{client.email}] : ")
        telephone = quit_fonction(f"Téléphone [{client.telephone}] : ")
        entreprise = quit_fonction(f"Entreprise [{client.entreprise}] : ")
    
        updated_data = {
            "fullname": fullname or client.fullname,
            "email": email or client.email,
            "telephone": telephone or client.telephone,
            "entreprise": entreprise or client.entreprise,
        }

        try:
            updated_client = crud_update_client(self.user, client_id, **updated_data)
            console.print(f"[green]Client : {updated_client.fullname} correctement mis à jour.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return
            
    

    def create_client(self, data):
        try:
            new_client = crud_create_client(self.user, **data)
            console.print(f"[green]Client {new_client.fullname} créé avec succès ![/green]")
        except Exception as e:
            console.print(f"[red]ERREUR : {e}[/red]")
            return