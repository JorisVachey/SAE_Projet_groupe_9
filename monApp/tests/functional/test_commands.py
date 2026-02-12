import pytest
from monApp.app import app
from monApp.models import User, Plat
from monApp.commands import create_user

def test_create_user_command(session):
    """Vérifie la fonction utilitaire de création d'utilisateur."""
    user = create_user("0700000000", "NewUser", "password", False, False, 0)
    assert user.idUser is not None
    assert user.pseudonyme == "NewUser"
    # Vérification du hash sha256
    assert user.mdp != "password" 

def test_loaddb_command(testapp):
    """Teste la commande CLI 'loaddb'."""
    runner = testapp.test_cli_runner()
    
    # On lance la commande (assure-toi d'avoir un fichier yaml de test ou utilise le vrai)
    # Ici on teste si la commande se lance sans erreur
    result = runner.invoke(args=["loaddb"])
    
    # Si le fichier n'existe pas dans l'env de test, on vérifie le message d'erreur prévu
    if "introuvable" in result.output:
        assert result.exit_code == 0
    else:
        assert "Insertion" in result.output



def test_drop_bd_command(testapp):
    """Teste la commande CLI 'drop_bd'."""
    runner = testapp.test_cli_runner()
    result = runner.invoke(args=["drop-db"])

    assert result.exit_code == 0
    assert "Tables supprimées" in result.output

def test_init_db_command(testapp):
    runner = testapp.test_cli_runner()
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "Tables crées avec succès" in result.output


def test_loaddb_introuable(testapp):
    runner = testapp.test_cli_runner()
    result = runner.invoke(args=["loaddb","--file", "fichier_qui_n_existe_pas.yaml"])
    assert "introuvable" in result.output


""" def test_newuser_command(testapp):
    runner = testapp.test_cli_runner()
    args = ["newuser", "0699999999", "cli_user", "password123", "--admin"]
    result = runner.invoke(args=args)
    #assert result.exit_code == 0
    assert "User 0699999999 created!" in result.output """