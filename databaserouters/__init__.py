from django.core.exceptions import ImproperlyConfigured

class AppModelRouter(object):
    """
    A router to control all database operations based on APP_MODEL_DATABASE_ROUTING settings
    """
    def check_configuration(self):
        """
        Check that all things needed to run this router have been correctly configured
        """
        if not settings.APP_MODEL_DATABASE_ROUTING:
            raise ImproperlyConfigured("AppModelRouter requires am APP_MODEL_DATABASE_ROUTING setting.")

    def db_for_read(self, model, **hints):
        """
        XXX
        """
        if model._meta.app_label == 'myapp':
            return 'other'
        return None

    def db_for_write(self, model, **hints):
        """
        XXX
        """
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'myapp':
            return 'other'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        XXX
        """
        if obj1._meta.app_label == 'myapp' or obj2._meta.app_label == 'myapp':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        XXX
        """
        if db == 'other':
            return model._meta.app_label == 'myapp'
        elif model._meta.app_label == 'myapp':
            return False
        return None

