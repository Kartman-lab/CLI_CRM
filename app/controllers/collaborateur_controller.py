from rich.console import Console
from rich.table import Table 

from app.crud.collaborateurs_manager import create_collaborateur as crud_create_collaborateur, get_collaborateur_by_id, update_collaborateur as crud_update_collaborateur
from app.crud.collaborateurs_manager import delete_collaborateur as crud_delete_collaborateur
from app.crud.contracts_manager import get_contract_by_id
from app.utils import quit_fonction


console = Console()

class CollaborateurController:
    def __init__(self, current_user):
        self.user = current_user
    
    def collaborateur_table(self, collaborateurs, title):
        table = Table(show_header=True, header_style="bold magenta", title=title)
        table.add_column("ID")
        table.add_column("Nom")
        table.add_column("Prenom")
        table.add_column("Email")
        table.add_column("Departement")
        table.add_column("Role ID")
        table.add_column("Role")
        
        for c in collaborateurs:
            table.add_row(
                str(c.id),
                c.nom,
                c.prenom,
                c.email,
                c.departement,
                str(c.role_id),
                c.role.nom if c.role else "N/A"
            )

        console.print(table)

    def prompt_data_collaborateur(self):
         console.print("[bold blue]=== Création d'un collaborateur ===[/bold blue]")
         nom = quit_fonction("Nom")
         prenom = quit_fonction("Prenom")
         email = quit_fonction("Email")
         departement = quit_fonction("Departement")
         role = quit_fonction("Role (parmi : 'gestion', 'commercial', 'support')")
         password = quit_fonction("Mot de passe temporaire")

         data = {
             "nom": nom,
             "prenom": prenom,
             "email": email,
             "departement": departement,
             "role": role,
             "password": password
         }

         return data

    def create_collaborateur(self, data):
        try:
            new_collaborateur = crud_create_collaborateur(self.user, **data)
            console.print(f"[green] Nouveau collaborateur '{new_collaborateur.nom}' créé avec succes. [/green]")
        except ValueError as e:
            console.print("[red]{e}[/red]")
            return

    def prompt_update_collaborateur(self):
         console.print("[bold blue]=== Modification d'un client ===[/bold blue]")
         collaborateur_id = input("Entrer l'id du client ('Q' pour retour)")
         return collaborateur_id
    
    def update_collaborateur(self, collaborateur_id):
        try:
            collaborateur = get_collaborateur_by_id(collaborateur_id)
        except ValueError as e:
            console.print("[red]{e}[/red]")
            return
        
        console.print("Entrer les nouveaux champs (laisser vide pour ne pas modifier) :")
        nom = quit_fonction("Nom")
        prenom = quit_fonction("Prenom")
        email = quit_fonction("Email >")
        departement = quit_fonction("Departement")
        role = quit_fonction("Role (parmi : 'gestion', 'commercial', 'support')")
        contract_id = quit_fonction("Id du contrat pour attribuer au commercial")

        if contract_id:
            try:
                contract = get_contract_by_id(contract_id)
            except ValueError as e:
                console.print(f"[red]{e}[/red]")
                return

        updated_data = {
            "nom": nom or collaborateur.nom,
             "premom": prenom or collaborateur.prenom,
             "email": email or collaborateur.email,
             "telephone": departement or collaborateur.departement,
             "role": role or collaborateur.role,
             "contracts": collaborateur.contracts.append(contract) or collaborateur.contracts 
        }

        try:
            update_collaborateur = crud_update_collaborateur(collaborateur_id, updated_data)
            console.print(f"[green]Collaborateur {update_collaborateur.nom} mis à jour.[/greem]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return 
        
    def delete_collaborateur(self):
        console.print("[bold blue]=== Suppression d'un collaborateur ===[/bold blue]")
        collaborateur_id = quit_fonction("Entrer l'id du collaborateur")
        collaborateur = get_collaborateur_by_id(self.user, collaborateur_id)
        confirmation = quit_fonction(f"[orange]Etes vous sur de vouloir supprimer {collaborateur.nom}. (Entrer OUI pour confirmer 'q' pour abandonner)[/orange]")

        if confirmation.upper() == 'OUI':
            crud_delete_collaborateur(self.user, collaborateur_id)
    








        
