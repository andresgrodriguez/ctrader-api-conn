import unittest
from unittest.mock import patch
from src.utils.config import load_config

class TestConfig(unittest.TestCase):
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret',
        'CTRADER_ACCOUNT_ID': '12345'
    })
    def test_load_config_minimal(self):
        """Test carga de configuración mínima con variables obligatorias"""
        config = load_config()
        self.assertEqual(config.client_id, 'test_id')
        self.assertEqual(config.client_secret, 'test_secret')
        self.assertEqual(config.account_id, 12345)
        self.assertEqual(config.api_host, 'demo.ctraderapi.com')
        self.assertEqual(config.port, 5035)
        self.assertEqual(config.log_level, 'INFO')
        self.assertEqual(config.output_dir, '/app/data/output')
    
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret',
        'CTRADER_ACCOUNT_ID': '12345',
        'CTRADER_API_HOST': 'live',
        'CTRADER_API_PORT': '5036',
        'LOG_LEVEL': 'DEBUG',
        'OUTPUT_DIR': '/custom/output'
    })
    def test_load_config_custom(self):
        """Test carga de configuración con valores personalizados"""
        config = load_config()
        self.assertEqual(config.api_host, 'live.ctraderapi.com')
        self.assertEqual(config.port, 5036)
        self.assertEqual(config.log_level, 'DEBUG')
        self.assertEqual(config.output_dir, '/custom/output')
    
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret'
    })
    def test_load_config_missing_account(self):
        """Test error cuando falta variable obligatoria"""
        with self.assertRaises(ValueError):
            load_config()
    
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret',
        'CTRADER_ACCOUNT_ID': 'not_a_number'
    })
    def test_load_config_invalid_account_id(self):
        """Test error cuando account_id no es un número"""
        with self.assertRaises(ValueError):
            load_config()
    
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret',
        'CTRADER_ACCOUNT_ID': '12345',
        'CTRADER_API_HOST': 'invalid'
    })
    def test_load_config_invalid_host(self):
        """Test error cuando host no es 'demo' o 'live'"""
        with self.assertRaises(ValueError):
            load_config()
    
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret',
        'CTRADER_ACCOUNT_ID': '12345',
        'CTRADER_API_PORT': 'not_a_number'
    })
    def test_load_config_invalid_port(self):
        """Test error cuando port no es un número"""
        with self.assertRaises(ValueError):
            load_config()
    
    @patch.dict('os.environ', {
        'CTRADER_CLIENT_ID': 'test_id',
        'CTRADER_CLIENT_SECRET': 'test_secret',
        'CTRADER_ACCOUNT_ID': '12345'
    })
    def test_load_config_with_args(self):
        """Test sobrescritura de configuración con argumentos CLI"""
        class MockArgs:
            def __init__(self):
                self.host = 'live'
                self.port = 5036
                self.log_level = 'DEBUG'
                self.output_dir = '/custom/output'
        
        config = load_config(MockArgs())
        self.assertEqual(config.api_host, 'live.ctraderapi.com')
        self.assertEqual(config.port, 5036)
        self.assertEqual(config.log_level, 'DEBUG')
        self.assertEqual(config.output_dir, '/custom/output')

if __name__ == '__main__':
    unittest.main() 