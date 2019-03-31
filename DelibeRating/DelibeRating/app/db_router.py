from app.models import CustomUser

ROUTED_MODELS = [CustomUser]


class DBRouter(object):

    def db_for_read(self, model, **hints):
        if model in ROUTED_MODELS:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model in ROUTED_MODELS:
            return 'default'
        return None
