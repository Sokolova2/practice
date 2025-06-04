import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.api.accountant.accountant_controller import accountant_routes
import os
from dotenv import load_dotenv

load_dotenv()

class AccountTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.token = os.getenv("JWT_SECRET")
        
    def test_get_orders_validate(self):
        response = self.client.get(
            "/accountant/orders", 
            params={'start_data': '2025-05-04', 'end_data': '2025-06-04'},
            headers={'Authorization': f'Bearer {self.token}'}
            )
        self.assertEqual(response.status_code, 200)
        
    def test_get_orders_invalid(self):
        response = self.client.get(
            "/accountant/orders", 
            params={'start_data': '2025.05.04', 'end_data': '2025.06.04'},
            headers={'Authorization': f'Bearer {self.token}'}
            )
        self.assertEqual(response.status_code, 422)
        
    def test_get_order_unauthorized(self):
        response = self.client.get(
            "/accountant/orders",
            params={'start_data': '2025-05-04', 'end_data': '2025-06-04'}
        )
        self.assertEqual(response.status_code, 401)


