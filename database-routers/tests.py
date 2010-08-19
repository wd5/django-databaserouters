import unittest

from django.conf import settings

class AppModelRouterTestCase(unittest.TestCase):
    from databaserouter import AppModelRouter

    def test_check_configuration(self):
        
        
        raise NotImplementedError
        
    def test_allow_syncdb(self):
        raise NotImplementedError
    
    def test_db_for_read(self):
        raise NotImplementedError
        
    def test_db_for_write(self):
        raise NotImplementedError
