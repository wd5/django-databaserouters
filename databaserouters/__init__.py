from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class AppModelRouter(object):
    """
    A router to control all database operations based on APP_MODEL_DATABASE_ROUTING settings.
    """
    def __init__(self, *args, **kwargs):
        self.check_configuration()

    @property
    def settings(self):
        return settings.APP_MODEL_DATABASE_ROUTING

    def check_configuration(self):
        """
        Check that all things needed to run this router have been correctly configured.
        """
        # If no APP_MODEL_DATABASE_ROUTING settings is specified an ImproperlyConfigured
        # exception should be raised.
        try:
            settings.APP_MODEL_DATABASE_ROUTING
        except AttributeError:
            raise ImproperlyConfigured("AppModelRouter requires an APP_MODEL_DATABASE_ROUTING setting.")
        
        # If an invalid APP_MODEL_DATABASE_ROUTING setting is specified an ImproperlConfigured
        # exception should be raised.
        if settings.APP_MODEL_DATABASE_ROUTING.__class__ != dict:
            raise ImproperlyConfigured("AppModelRouter requires a dictionary for APP_MODEL_DATABASE_ROUTING setting.")
            
    def db_for_read(self, model, **hints):
        """
        Read the model from the database specified for it under the db_for_read router. 
        """
        dbs = self.resolve_dbs_for_router_by_model(router='db_for_read', model=model)
        if dbs:
            return dbs[0]
        return None

    def db_for_write(self, model, **hints):
        """
        Write the model to the database specified for it under the db_for_write router. 
        """
        dbs = self.resolve_dbs_for_router_by_model(router='db_for_write', model=model)
        if dbs:
            return dbs[0]
        return None

    def allow_syncdb(self, db, model):
        """
        syncdb for all models specified for the db under the allow_syncdb router. 
        """
        dbs = self.resolve_dbs_for_router_by_model(router='allow_syncdb', model=model)
        return (db in dbs)
        
    def resolve_dbs_for_router_by_model(self, model, router):
        """
        Determines which dbs have been configured for the given router and model.
        """
        dbs = []
        app_model_name = "%s.%s" % (model._meta.app_label, model._meta.object_name.lower())
        try:
            router = self.settings[router]
        except KeyError:
            return dbs
           
        for key, values in router.items():
            if app_model_name in values:
                dbs.append(key)

        return dbs
