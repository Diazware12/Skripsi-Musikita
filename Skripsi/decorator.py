from django.db.models import Q

def is_Admin(user):
    return user.groups.filter(name='Admin').exists()

def is_User(user):
    return user.groups.filter(Q(name='Reg_User') | Q(name='Mus_Store')).exists()