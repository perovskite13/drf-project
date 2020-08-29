from django.apps import AppConfig


class EchoConfig(AppConfig):
    name = 'echo'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals