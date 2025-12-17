from commands import create_user
from monApp.models import User
def test_utilisateur_init():
    user = create_user("1234567890","Bob","mdp",False,False,0)
    assert user.pseudonyme == "Bob"

def test_user_repr(testapp):
    with testapp.app_context():
        user = User.query.get(1)
        assert repr(user) == "<User>"