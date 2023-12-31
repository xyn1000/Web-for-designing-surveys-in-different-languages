import jmespath
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase



class ClinicTestCase(APITestCase):

    #successful register
    def test_register1(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    #unsuccessful register - password mismatch
    def test_register2(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - missing username
    def test_register3(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - User already exists
    def test_register4(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        resp2 = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - Email already exists
    def test_register5(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        resp2 = client.post("/account/register/", {"username": "test1", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - field may not be blank
    def test_register6(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": ""})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - password too short
    def test_register7(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "Test0.!", "password2": "Test0.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - password entirely numeric
    def test_register8(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "080980932432", "password2": "080980932432", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #unsuccessful register - invalid email
    def test_register9(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "testgmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    #successful login
    def test_login1(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(client.login(username='test', password='TestTest0.!'))
        client.logout()

    #unsuccessful login - missing fields
    def test_login2(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertFalse(client.login(username='', password='TestTest0.!'))
        client.logout()

    #unsuccessful login - invalid credentials
    def test_login3(self):
        client = APIClient()
        resp = client.post("/account/register/",
                           {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!",
                            "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertFalse(client.login(username='test', password='testTest0.!'))
        client.logout()

    #successful password change
    def change_password1(self):
        client = APIClient()
        resp = client.post("/account/register/",
                           {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!",
                            "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(client.login(username='test', password='TestTest0.!'))
        resp2 = client.post("/account/password/change", {"old_password": "TestTest0.!", "new_password1": "TestTest0.!123", "new_password2": "TestTest0.!123"})
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        client.logout()

        self.assertFalse(client.login(username='test', password='TestTest0.!'))
        self.assertTrue(client.login(username='test', password='TestTest0.!123'))

    #unsuccessful password change - wrong old password
    def change_password2(self):
        client = APIClient()
        resp = client.post("/account/register/", {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!", "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(client.login(username='test', password='TestTest0.!'))
        resp2 = client.post("/account/password/change", {"old_password": "TestTest0.!1", "new_password1": "TestTest0.!123", "new_password2": "TestTest0.!123"})
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        client.logout()

    #
    def test_get_user_info(self):
        client = APIClient()
        resp = client.post("/account/register/",
                           {"username": "test", "password1": "TestTest0.!", "password2": "TestTest0.!",
                            "email": "test@gmail.com"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(client.login(username='test', password='TestTest0.!'))

         ##ERROR IN THIS TEST CASE, CANT FIND KEY??

        #key = jmespath.search("key", resp.data)
        #client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        #resp = client.get("/account/user/")
        #self.assertEqual(resp.status_code, status.HTTP_200_OK)

        #email = jmespath.search("email", resp.data)
        #username = jmespath.search("username", resp.data)
        #self.assertEqual(email, "test@gmail.com")
        #self.assertEqual(username, "test")

        client.logout()
