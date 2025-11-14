from rich.console import Console 
from rich.table import Table

from app.crud.contracts_manager import create_contract as crud_create_contract, updtate_contract as crud_update_contract
from app.crud.contracts_manager import get_contract_by_id, get_contract_not_signed, get_contracts_not_fully_payed
from app.utils import quit_fonction
console = Console()

class ContractsController:
    def  __init__(self, current_user):
        self.user = current_user

    def contract_table(self, contracts, title):
        table = Table(show_header=True, header_style="bold magenta", title=title)
        table.add_column("ID")
        table.add_column("Client")
        table.add_column("Commercial")
        table.add_column("Montant (€)")
        table.add_column("Montant restant")
        table.add_column("Date de création")
        table.add_column("Statut")

        for c in contracts:
            table.add_row(
                str(c.id),
                c.client.fullname if c.client else "N/A",
                c.commercial.nom if c.commercial_id else "Aucun",
                str(c.total_amount),
                str(c.amount_left),
                str(c.date_created),
                "Signé" if c.statut else "Non signé"
            )
        console.print(table)
           

    def show_not_signed_contracts(self):
        try:
            contracts = get_contract_not_signed(self.user)
            self.contract_table(contracts, "Contrats non signés")
        except PermissionError as e:
            console.print(f"[red]{e}[/red]")
        except ValueError as e:
            console.print(f"[yellow]{e}[/yellow]")

                
    def show_not_fully_payed_contracts(self):
        try:
            contracts = get_contracts_not_fully_payed(self.user)
            self.contract_table(contracts, "Contrats impayés")
        except PermissionError as e:
            console.print(f"[red]{e}[/red]")
        except ValueError as e:
            console.print(f"[yellow]{e}[/yellow]")


    def create_contract(self):
        console.print("[bold blue]=== Création d’un nouveau contrat ===[/bold blue]")
        console.print("'Q' pour quitter")
        
        try:
            total_amout = quit_fonction("Montant total")
            amount_left = total_amout
            client_fullname = quit_fonction("Nom du client")
            commercial_fullname = quit_fonction("Nom du commercial")
    
            data = {
                "total_amount": total_amout, 
                "amount_left": amount_left,
                "client_fullname": client_fullname,
                "commercial_fullname": commercial_fullname
            }

            crud_create_contract(self.user, **data)
            console.print("[green]Nouveau contrat créé avec succès[/green]")

        except KeyboardInterrupt as k:
            console.print(f"[yellow]{k}[/yellow]")
    
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return 

    def promt_update_client(self):
        console.print("[bold blue]=== Modification d'un contrat ===[/bold blue]")
        try:
            contract_id = input("Entrer l'id du contrat ('Q' pour retour) > ")
            return contract_id
        except KeyboardInterrupt as k:
            console.print(f"[yellow]{k}[/yellow]")


      
    def update_contract(self):
        console.print("[bold blue]=== Modification d'un contrat ===[/bold blue]")
        console.print("[orange]Entrer uniquement les champs que vous voulez modifier.[/orange]")
        console.print("'Q' pour quitter")

        try: 
            contract_id = self.promt_update_client()
            contract = get_contract_by_id(contract_id)

            total_amout = quit_fonction("Montant total")
            amount_left = quit_fonction("Montant restant")
            if amount_left is None:
                amount_left = total_amout

            client_fullname = quit_fonction("Nom du client")
            commercial_fullname = quit_fonction("Nom du commercial")

            statut = quit_fonction("Signé (oui/non)")
            if statut.upper() == 'OUI':
                statut = True

            update_data = {
                "total_amount": total_amout or contract.total_amount,
                "amount_left": amount_left or contract.amount_left,
                "client_fullname": client_fullname or contract.client.fullname,
                "commercial_fullname": commercial_fullname or contract.commercial.nom,
                "statut": statut or contract.statut
    
            }

            crud_update_contract(self.user, contract_id, **update_data)

        except KeyboardInterrupt as k:
            console.print(f"[yellow]{k}[/yellow]")

        except ValueError as e:
            console.print(f"[red]{e}[/red]")




        
