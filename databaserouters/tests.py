import unittest

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TestModel(models.Model):
    pass
models.register_models('databaserouters', TestModel)

class AppModelRouterTestCase(unittest.TestCase):

    def setUp(self):
        from databaserouters import AppModelRouter
        settings.APP_MODEL_DATABASE_ROUTING = {}
        self.router = AppModelRouter()

    def test_check_configuration(self):
        # If no APP_MODEL_DATABASE_ROUTING settings is specified an ImproperlyConfigured
        # exception should be raised.
        try:
            del settings.APP_MODEL_DATABASE_ROUTING
        except AttributeError:
            pass
        self.assertRaises(ImproperlyConfigured, self.router.check_configuration)     

        # If an invalid APP_MODEL_DATABASE_ROUTING setting is specified an ImproperlConfigured
        # exception should be raised.
        settings.APP_MODEL_DATABASE_ROUTING = None
        self.assertRaises(ImproperlyConfigured, self.router.check_configuration)     
        
    def test_allow_syncdb(self):
        # Return False if the model is not specified for the allow_syncdb router.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {'default': []},
        }
        self.failIf(self.router.allow_syncdb(db='default', model=TestModel))
        
        # Return False if the model is specified for the allow_syncdb router but not for the database.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {'invalid_database': ['databaserouters.testmodel']},
        }
        self.failIf(self.router.allow_syncdb(db='default', model=TestModel))
        
        # Return True if the model is specified for the allow_syncdb router and database.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {'default': ['databaserouters.testmodel']},
        }
        self.failUnless(self.router.allow_syncdb(db='default', model=TestModel))
    
    def test_db_for_read(self):
        # Return None if the the model is not specified for the db_for_read router
        settings.APP_MODEL_DATABASE_ROUTING = {
            'db_for_read': {
                'default': [],
            },
        }
        self.failIf(self.router.db_for_read(model=TestModel))
        
        # Return the first database the the model is specified for under the db_for_read router
        settings.APP_MODEL_DATABASE_ROUTING = {
            'db_for_read': {
                'default': ['databaserouters.testmodel'],
                'some_other_database': ['databaserouters.testmodel'],
            },
        }
        self.failUnless(self.router.db_for_read(model=TestModel) == 'default')
    
    def test_db_for_write(self):
        # Return None if the the model is not specified for the db_for_write router
        settings.APP_MODEL_DATABASE_ROUTING = {
            'db_for_write': {
                'default': [],
            },
        }
        self.failIf(self.router.db_for_write(model=TestModel))
        
        # Return the first database the the model is specified for under the db_for_write router
        settings.APP_MODEL_DATABASE_ROUTING = {
            'db_for_write': {
                'default': ['databaserouters.testmodel'],
                'some_other_database': ['databaserouters.testmodel'],
            },
        }
        self.failUnless(self.router.db_for_write(model=TestModel) == 'default')
   
    def test_resolve_dbs_for_router_by_model(self):
        # Return the empty list if an invalid router is specified.
        self.failUnless(self.router.resolve_dbs_for_router_by_model(model=TestModel, router='invalid_router') == [])
        
        # Return the empty list if an valid router is specified but without any databases.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {}
        }
        self.failUnless(self.router.resolve_dbs_for_router_by_model(model=TestModel, router='allow_syncdb') == [])
        
        # Return the empty list if an valid router is specified with a database but without any models.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {'default': []}
        }
        self.failUnless(self.router.resolve_dbs_for_router_by_model(model=TestModel, router='allow_syncdb') == [])
        
        # Return the empty list if an valid router is specified with a database but with an invalid model.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {'default': ['invalid.model']}
        }
        self.failUnless(self.router.resolve_dbs_for_router_by_model(model=TestModel, router='allow_syncdb') == [])
        
        # Return the list of databases if a valid router is specified with a database and models.
        settings.APP_MODEL_DATABASE_ROUTING = {
            'allow_syncdb': {'default': ['databaserouters.testmodel']}
        }
        self.failUnless('default' in self.router.resolve_dbs_for_router_by_model(model=TestModel, router='allow_syncdb'))
