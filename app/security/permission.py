from functools import wraps
from app.crud.auth_manager import load_session

def require_role(*allowed_roles):
   def decorator(func):
        @wraps(func)
        def wrapper(current_user, *args, **kwargs):
            role = getattr(current_user, "role", None)
            if not role:
                print("Accès refusé, vous n'avez pas de rôle.")
                return None
            if role.nom not in allowed_roles:
                print("Accès refusé, vous n'avez pas la permission pour cette action.")
                return None 
            return func(current_user, *args, **kwargs)
        return wrapper
   return decorator

def require_auth(func):
    @wraps(func)
    def wrapper(current_user, *args, **kwargs):
        token = load_session()
        if not token:
            raise PermissionError("Accès refusé : aucune session active.")
        return func(current_user, *args, **kwargs)
    return wrapper
