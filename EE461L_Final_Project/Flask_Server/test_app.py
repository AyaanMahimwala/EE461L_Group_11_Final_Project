"""
EE461L_Final_Project\Flask_Server\Tests\test_app.py

This file will create a simple local mock flask app and test the mongo db accessors
and mutator functionality.
"""

from flask import Flask, request, jsonify
import unittest
import os

os.environ["MOCK"] = "True"

from Database.Login_Credentials.login_cred_service import LoginSetService

def create_app() -> Flask:
    # Create exposed DB entry point
    my_login_set_service_g = LoginSetService()
    app = Flask(__name__)

    # Register the login routes

    # Default route
    @app.route("/", methods=["GET", "POST", "DELETE", "HEAD", "PUT"])
    def default():
        #print("route default")
        return jsonify("Home"), 200

    # Get count of users
    @app.route("/login_set", methods=["GET"])
    def count_login_set():
        return jsonify(my_login_set_service_g.count_login_set()), 200

    # Find one user by id
    @app.route("/login_set/find/", methods=["GET"])
    def find_login_set():
        #print("route find")
        #print(request.url)
        # Get the request user_id arg
        this_user_id = request.args.get("user_id")
        #print(this_user_id)
        # Return the serialized (by marshmallow schema) user
        return jsonify(my_login_set_service_g.find_login_set(this_user_id)), 200

    # Create one user by id with password
    @app.route("/login_set/create/", methods=["GET"])
    def create_login_set():
        #print("route create")
        #print(request.url)
        # Get the request user_id arg
        this_user_id = request.args.get("user_id")
        #print(this_user_id)
        # Get the request user_password arg
        this_user_password = request.args.get("user_password")
        #print(this_user_password)
        # Return the serialized (by marshmallow schema) user
        return jsonify(my_login_set_service_g.create_login_set_for(this_user_id, this_user_password)), 200

    # Update one user by id with password
    @app.route("/login_set/update/", methods=["GET"])
    def update_login_set():
        # Get the request user_id arg
        this_user_id = request.args.get("user_id")
        # Get the request user_password arg
        this_user_password = request.args.get("user_password")
        # Return the serialized (by marshmallow schema) user
        return jsonify(my_login_set_service_g.update_login_set_with(this_user_id, this_user_password)), 200

    # Delete one user by id
    @app.route("/login_set/delete/", methods=["GET"])
    def delete_login_set():
        # Get the request user_id arg
        this_user_id = request.args.get("user_id")
        # Return the serialized (by marshmallow schema) user
        return jsonify(my_login_set_service_g.delete_login_set_for(this_user_id)), 200

    # Validate one user by id with password
    @app.route("/login_set/validate/", methods=["GET"])
    def validate_login_set():
        #print("route create")
        #print(request.url)
        # Get the request user_id arg
        this_user_id = request.args.get("user_id")
        #print(this_user_id)
        # Get the request user_password arg
        this_user_password = request.args.get("user_password")
        #print(this_user_password)
        # Return the serialized (by marshmallow schema) user
        return jsonify(my_login_set_service_g.validate_login_set(this_user_id, this_user_password)), 200

    return app

class TestLoginSet(unittest.TestCase):
    """
    Tester class for login sets
    https://flask.palletsprojects.com/en/1.1.x/reqcontext/
    """
    # Create the test client adapter
    client = create_app().test_client()

    def test_empty_count(self):
        print("----------------------------------------------------------------------")
        # Test count
        print("[TEST] Test of empty count")

        response = self.client.get("/login_set", method="GET").get_data(as_text=True).strip().replace('"', '')
        self.assertEqual(response, "0", "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_empty_find(self):
        print("----------------------------------------------------------------------")
        # Empty find
        print("[TEST] Test of empty find")

        response = self.client.get("/login_set/find/", method="GET", query_string={"user_id" : "username"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, False, "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_empty_delete(self):
        print("----------------------------------------------------------------------")
        # Test count
        print("[TEST] Test of empty count")

        response = self.client.get("/login_set", method="GET").get_data(as_text=True).strip().replace('"', '')
        self.assertEqual(response, "0", "This should be false as the user has not been posted")

        # Delete
        print("[TEST] Test of empty delete")

        response = self.client.get("/login_set/delete/", method="GET", query_string={"user_id" : "username"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, False, "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_create_and_delete(self):
        print("----------------------------------------------------------------------")
        # Create
        print("[TEST] Test of create and find")

        response = self.client.get("/login_set/create/", method="GET", query_string={"user_id" : "username", "user_password" : "password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as this is first user post")

        # Test non-empty count
        print("[TEST] Test of non-empty count")

        response = self.client.get("/login_set", method="GET").get_data(as_text=True).strip().replace('"', '')
        self.assertEqual(response, "1", "This should be false as the user has not been posted")

        # Test non-empty find
        print("[TEST] Test of non-empty find")

        response = self.client.get("/login_set/find/", method="GET", query_string={"user_id" : "username"}).get_data(as_text=True).strip().replace('"', '')
        #print(response)
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as the user has been posted")

        # Delete and find
        print("[TEST] Test of delete")

        response = self.client.get("/login_set/delete/", method="GET", query_string={"user_id" : "username"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as the user has been posted")

        # Test count after delete
        print("[TEST] Test of empty count after delete")

        response = self.client.get("/login_set", method="GET").get_data(as_text=True).strip().replace('"', '')
        self.assertEqual(response, "0", "This should be false as the user has not been posted")
        
        # Empty find after delete
        print("[TEST] Test of empty find after delete")

        response = self.client.get("/login_set/find/", method="GET", query_string={"user_id" : "username"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, False, "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_validate_and_update_and_delete(self):
        print("----------------------------------------------------------------------")
        # Create
        print("[TEST] Test of create and find")

        response = self.client.get("/login_set/create/", method="GET", query_string={"user_id" : "username", "user_password" : "password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as this is first user post")

        # Test non-empty count
        print("[TEST] Test of non-empty count")

        response = self.client.get("/login_set", method="GET").get_data(as_text=True).strip().replace('"', '')
        self.assertEqual(response, "1", "This should be false as the user has not been posted")

        # Test non-empty find
        print("[TEST] Test of non-empty find")

        response = self.client.get("/login_set/find/", method="GET", query_string={"user_id" : "username"}).get_data(as_text=True).strip().replace('"', '')
        #print(response)
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as the user has been posted")

        # Test validate correct
        print("[TEST] Test of validate with correct info")

        response = self.client.get("/login_set/validate/", method="GET", query_string={"user_id" : "username", "user_password" : "password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as this is correct info")

        # Test validate incorrect
        print("[TEST] Test of validate with incorrect info")

        response = self.client.get("/login_set/validate/", method="GET", query_string={"user_id" : "username", "user_password" : "other_password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, False, "This should be false as this is incorrect info")

        # Test bad update
        print("[TEST] Test of update with new bad info")

        response = self.client.get("/login_set/update/", method="GET", query_string={"user_id" : "other_username", "user_password" : "other_password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, False, "This should be false as user posted and available for update but this is wrong user")

        # Retest validate correct
        print("[TEST] Retest of validate with correct info after bad update attempt")

        response = self.client.get("/login_set/validate/", method="GET", query_string={"user_id" : "username", "user_password" : "password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as this is correct info")

        # Test update
        print("[TEST] Test of update with new info")

        response = self.client.get("/login_set/update/", method="GET", query_string={"user_id" : "username", "user_password" : "other_password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as user posted and available for update")

        # Test validate changed correct
        print("[TEST] Test of validate with updated correct info")

        response = self.client.get("/login_set/validate/", method="GET", query_string={"user_id" : "username", "user_password" : "other_password"}).get_data(as_text=True).strip().replace('"', '')
        result = True if response == "True" else False
        self.assertEqual(result, True, "This should be true as this is now correct info")
        print("----------------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()
