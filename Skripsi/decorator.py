def is_Admin(user):
    return user.groups.filter(name='Admin').exists()