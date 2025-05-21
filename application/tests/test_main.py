import unittest
from application.src.main import load_config

class TestFraudDetection(unittest.TestCase):
    def test_load_config(self):
        config = load_config()
        self.assertEqual(config['aws']['region'], 'us-east-1')

if __name__ == '__main__':
    unittest.main()
