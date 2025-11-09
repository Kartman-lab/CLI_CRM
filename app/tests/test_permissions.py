from app.security.permission import require_role

class FakeUser:
    def __init__(self, role_name):
        self.role = type('Role', (), {'nom': role_name})()

@require_role("commercial")
def get_commercial_menu(current_user):
    return "Menu commercial affiché"

def test_commercial_access():
    user = FakeUser("commercial")
    assert get_commercial_menu(user) == "Menu commercial affiché"

def test_non_commercial_access():
    user = FakeUser("support")
    assert get_commercial_menu(user) is None 