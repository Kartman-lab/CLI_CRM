from rich.console import Console
from rich.table import Table
from datetime import datetime

from app.crud.events_manager import create_event_for_client as crud_create_event_for_client, get_event_by_id, assign_event_support, update_event as crud_update_event
from app.crud.contracts_manager import get_contract_by_id
from app.crud.collaborateurs_manager import get_collaborateur_by_id
from app.utils import quit_fonction

console = Console()

class EventsController:
    def __init__(self, current_user):
        self.user = current_user

    def event_table(self, events, title):
        events = sorted(events, key=lambda e: e.id)
        table = Table(show_header=True, header_style="bold magenta", title=title)
        table.add_column("ID")
        table.add_column("Date de début")
        table.add_column("Date de fin")
        table.add_column("Localisation")
        table.add_column("Invités")
        table.add_column("notes")
        """Ajouter les relations ???"""

        for e in events: 
            table.add_row(
                str(e.id),
                str(e.start_date),
                str(e.end_date),
                e.location,
                str(e.attendiees),
                e.notes
            )

        console.print(table)


    def prompt_data_event(self):
        console.print("[bold blue]=== Création d'un évènement ===[/bold blue]")
        contract_id = quit_fonction("Entrer l'id du contrat")
        try:
            get_contract_by_id(self, contract_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return 
        try:
            start_date = datetime.strptime(quit_fonction("Date de début (YYYY-MM-DD)"), "%Y-%m-%d").date()
            end_date = datetime.strptime(quit_fonction("Date de fin (YYYY-MM-DD)"), "%Y-%m-%d").date()
        except ValueError:
            console.print("[red]Format de date invalide. Utilisez YYYY-MM-DD.[/red]")
            return 

        location = quit_fonction("Localisation").strip()
        attendiees = quit_fonction("Nombre d'invités").strip()
        notes = quit_fonction("Notes >").strip()
        support_id = quit_fonction("ID du support").strip()
        support_id = int(support_id) if support_id else None

        try:
            attendiees = int(attendiees)
            if support_id:
                support_id = int(support_id)
        except ValueError:
            console.print("[red]L'identifiant et le nombre d'invités doivent être des nombres.[/red]")
            return 


        return {
            "contract_id": contract_id,
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "attendiees": attendiees,  
            "notes": notes,
            "support_id": support_id
        }


    def create_event_for_client(self):
        data = self.prompt_data_event()
        try:
            crud_create_event_for_client(self.user, **data)
            print("[green]Évènement créé avec succès.[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

    def get_event_id(self):
        console.print("Entrer l'id de l'évènement que vous souhaitez modifier")
        event_id = quit_fonction("")
        try:
            get_event_by_id(event_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return 
        return event_id 
    

    def update_my_event(self, event_id):
        try:
            event = get_event_by_id(event_id)

            start_date_input = quit_fonction("Date de début (YYYY-MM-DD)").strip()
            end_date_input = quit_fonction("Date de fin (YYYY-MM-DD)").strip()

            start_date = datetime.strptime(start_date_input, "%Y-%m-%d").date() if start_date_input else event.start_date
            end_date = datetime.strptime(end_date_input, "%Y-%m-%d").date() if end_date_input else event.end_date

            location = quit_fonction("Localisation").strip() or event.location
            attendiees_input = quit_fonction("Nombre d'invités").strip()
            attendiees = int(attendiees_input) if attendiees_input else event.attendiees
            notes = quit_fonction("Notes >").strip() or event.notes

            updated_data = {
                "contract_id": event.contract_id,
                "start_date": start_date,
                "end_date": end_date,
                "location": location,
                "attendiees": attendiees,  
                "notes": notes,
                "support_id": event.support_contact_id
            }

            crud_update_event(event_id, **updated_data)
            console.print("[green]Évènement mis à jour.[/green]")

        except KeyboardInterrupt as k:
            console.print(f"[yellow]{k}[/yellow]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")




    def associate_support_to_event(self):
        console.print("[bold blue]Associer un support à un évènement[/bold blue]")
        console.print("Appuyer sur 'Q' pour quitter ")
        
        try:
            event_id = quit_fonction("Id de l'évènement")
            commercial_id = quit_fonction("Id du support")

            assign_event_support(self.user, event_id, commercial_id)

        except KeyboardInterrupt as k:
            console.print(f"[yellow]{k}[/yellow]")

        except ValueError as e:
            console.print(f"[red]{e}[/red]")





