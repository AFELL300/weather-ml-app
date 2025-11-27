import unittest
from app import app

class TestAppSmoke(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()
	
	# Complete the function below to test a success in running the application
	def test_prediction_route_success(self):
		response = self.client.get('/')

		# Check that the response status is 200, which means the request has succeeded.
		self.assertEqual(response.status_code, 200, "Error: Application is not running successfully.")
		

	# Complete the function below to test a form is rendered
	def test_get_form(self):
		response = self.client.get('/')

		# Search for byte string containing form HTML tag inside the HTML body of the app.
		self.assertTrue(b'<form' in response.data, "Error: Form has not rendered in app body.")
 
if __name__ == '__main__':
	unittest.main()
