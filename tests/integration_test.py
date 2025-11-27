import re
import unittest
from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

	def setUp(self):
		app.testing = True
		self.client = app.test_client()
		
	def test_model_app_integration(self):
		# Valid test input that should work with the trained model
		form_data = {
			'temperature': '275.15',   # Kelvin
			'pressure': '1013',        # hPa
			'humidity': '85',          # %
			'wind_speed': '3.6',       # m/s
			'wind_deg': '180',         # degrees
			'rain_1h': '0',            # mm
			'rain_3h': '0',            # mm
			'snow': '0',               # mm
			'clouds': '20'             # %
		}

		response = self.client.post('/', data=form_data)
	
		# Ensure that the result page (response.data) should include a weather prediction
		response_text = response.data.decode('utf-8')

		# check html that there is a word where the {{ prediction }} variable would be, indicating a prediction exists
		# \s* checks for spaces between the HTML tag
		# (\w+) ensures that there is at least one word present (aka not empty).
		prediction_value = re.search(r"The weather is:</strong>\s*(\w+)", response_text)

		# assert that the text found is not None, proving a prediction is included.
		self.assertIsNotNone(prediction_value, "Error: No prediction found.")
	
		# Ensure that the result page should include a prediction time

		# check html that there is a word where the {{ latency }} variable would be, indicating a prediction exists
		# \s* checks for spaces between the HTML tags and other text (such as ms)
		# ([\d.]+) ensures that there is a floating point value present and that at least one digit exists.
		latency_value = re.search(r'Prediction time:</strong>\s*([\d.]+)\s*ms', response_text)

		# assert that the float found is not None, proving the prediction time is included.
		self.assertIsNotNone(latency_value, "Error: No prediction time found.")

		html_text = response.data.decode('utf-8').lower()
		valid_classes = [
			'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
			'misty', 'rainy', 'smokey', 'thunderstorm'
		]
		found = any(weather in html_text for weather in valid_classes)
		
		# Ensure that classification is in valid classes, provide an error message if not.

		# check if found variable is True, meaning the classifcation is a valid class.
		# return error message if not.
		self.assertTrue(found, f"Prediction class {found} is not a valid class.")
		

if __name__ == '__main__':
	unittest.main()
