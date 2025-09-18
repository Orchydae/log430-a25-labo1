from daos.user_dao_mongo import UserDAOMongo
from models.user import User

dao = UserDAOMongo()
dao.delete_all()  # Nettoyer avant test
if not dao.select_all():  # si vide
    dao.insert(User(None, "Ada Lovelace", "alovelace@example.com"))
    dao.insert(User(None, "Adele Goldberg", "agoldberg@example.com"))
    dao.insert(User(None, "Alan Turing", "aturing@example.com"))

def test_user_select():
    user_list = dao.select_all()
    assert len(user_list) >= 3

def test_user_insert():
    user = User(None, 'Margaret Hamilton', 'hamilton@example.com')
    dao.insert(user)
    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email in emails

def test_user_update():
    user = User(None, 'Charles Babbage', 'cbabbage@example.com')
    assigned_id = dao.insert(user)
    corrected_email = 'cbabbage@newdomain.com'
    user.id = assigned_id
    user.email = corrected_email
    dao.update(user)
    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert corrected_email in emails

def test_user_delete():
    user = User(None, 'Douglas Engelbart', 'douglas@example.com')
    assigned_id = dao.insert(user)
    deleted = dao.delete(assigned_id)
    assert deleted == 1
    # Now verify email is gone
    emails = [u.email for u in dao.select_all()]
    assert 'douglas@example.com' not in emails