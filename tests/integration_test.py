import os, json
import unittest
import requests
from requests.auth import HTTPBasicAuth

class TestProganAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:8000"  # Update with your actual API URL

    def test_create_user(self):
        url = f"{self.base_url}/api/v1/add_user"
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        }

        response = requests.post(url, data=json.dump(data))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], data["username"])
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), data["content_directory"])))

    def test_read_users_me(self):
        url = f"{self.base_url}/users/me/"
        response = requests.get(url)

        self.assertEqual(response.status_code, 401)  # Unauthorized without token

    def test_login(self):
        url = f"{self.base_url}/api/v1/token"
        data = {"username": "testuser", "password": "testpassword"}

        response = requests.post(url, data=data, auth=HTTPBasicAuth(data["username"], data["password"]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_generate_photo(self):
        url_login = f"{self.base_url}/api/v1/token"
        data_login = {"username": "testuser", "password": "testpassword"}
        response_login = requests.post(url_login, data=data_login, auth=HTTPBasicAuth(data_login["username"], data_login["password"]))

        self.assertEqual(response_login.status_code, 200)
        access_token = response_login.json()["access_token"]

        url_generate = f"{self.base_url}/api/v1/generate_photo"
        data_generate = {"num_imgs": 1, "labels": {"attributes": [-1,-1,-1,1,-1,-1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,1]}}

        headers = {"Authorization": f"Bearer {access_token}"}
        response_generate = requests.post(url_generate, json=data_generate, headers=headers)

        self.assertEqual(response_generate.status_code, 200)
        self.assertIn("image", response_generate.headers["content-type"])

    # Add more test methods as needed for other endpoints

if __name__ == "__main__":
    unittest.main()
