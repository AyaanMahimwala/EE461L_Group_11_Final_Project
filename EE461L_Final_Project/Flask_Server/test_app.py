"""
EE461L_Final_Project\Flask_Server\Tests\test_app.py

This file will create a simple local mock flask app and test the mongo db accessors
and mutator functionality.
"""

from flask import Flask, request, jsonify

# Bunch of imports required for session management
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect, generate_csrf

import unittest
import os

import json

# Setting the enviorn tag to mock uses a mock mongo db instead of the served db
os.environ["MOCK"] = "True"

from Database.Login_Credentials.login_cred_service import LoginSetService

# TODO
# Need to implement class functions for UserMixin
# Need to wrap the servicer in this class
# https://flask-login.readthedocs.io/en/latest/#your-user-class

def create_app() -> Flask:
    # Create exposed DB entry point
    my_login_set_service_g = LoginSetService()
    # Static folder can house things like images or any backend data not suited for db storage
    app = Flask(__name__, static_folder="public")

    # Set configs
    # Set the server up for session based access
    app.config.update(
        DEBUG=True,
        # Sets the secret key for signing cookies and sessions
        SECRET_KEY="accidentally_leaked",
        # The HttpOnly flag set to True prevents any client-side usage of the session cookie
        SESSION_COOKIE_HTTPONLY=True,
        # limit the cookies to HTTPS traffic only for production.
        REMEMBER_COOKIE_HTTPONLY=True,
        # Lax loosens security a bit so that cookies will be sent cross-domain for the majority of requests.
        SESSION_COOKIE_SAMESITE="Lax",
    )

    # Setup the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    # Setup csrf, add csrf token to meta tag of front end
    # <meta name="csrf-token" content="{{ csrf_token() }}" />
    # Assign when component mounts
    # let csrf = document.getElementsByName("csrf-token")[0].content;
    csrf = CSRFProtect(app)
    cors = CORS(
        app,
        resources={r"*": {"origins": "http://localhost:8080"}},
        expose_headers=["Content-Type", "X-CSRFToken"],
        supports_credentials=True,
    )

    # Register the login routes

    # Default route
    @app.route("/", methods=["GET", "POST", "DELETE", "HEAD", "PUT"])
    def default():
        #print("route default")
        return jsonify("Home"), 200

    # Since front end seperate port and thread from backend we provide a sanity check function to ping the connection
    @app.route("/api/ping", methods=["GET"])
    def home():
        return jsonify({"ping": "pong!"})

    # Get count of users
    @app.route("/api/login_set/count", methods=["GET"])
    def count_login_set():
        return jsonify({"login_count" : my_login_set_service_g.count_login_set()}), 200

    # Find one user by id
    @app.route("/api/login_set/find/", methods=["GET"])
    def find_login_set():
        #print("route find")
        #print(request.url)
        # Get the request user_name arg
        this_user_name = request.args.get("user_name")
        #print(this_user_name)
        # Return the serialized (by marshmallow schema) user
        return jsonify({"login_found" : my_login_set_service_g.find_login_set(this_user_name)}), 200

    # Create one user by id with password
    @app.route("/api/login_set/create/", methods=["GET"])
    def create_login_set():
        #print("route create")
        #print(request.url)
        # Get the request user_name arg
        this_user_name = request.args.get("user_name")
        #print(this_user_name)
        # Get the request user_password arg
        this_user_password = request.args.get("user_password")
        #print(this_user_password)
        # Return the serialized (by marshmallow schema) user
        return jsonify({"login_created" : my_login_set_service_g.create_login_set_for(this_user_name, this_user_password)}), 200

    # Update one user by id with password
    @app.route("/api/login_set/update/", methods=["GET"])
    def update_login_set():
        # Get the request user_name arg
        this_user_name = request.args.get("user_name")
        # Get the request user_password arg
        this_user_password = request.args.get("user_password")
        # Return the serialized (by marshmallow schema) user
        return jsonify({"login_updated" : my_login_set_service_g.update_login_set_with(this_user_name, this_user_password)}), 200

    # Delete one user by id
    @app.route("/api/login_set/delete/", methods=["GET"])
    def delete_login_set():
        # Get the request user_name arg
        this_user_name = request.args.get("user_name")
        # Return the serialized (by marshmallow schema) user
        return jsonify({"login_deleted" : my_login_set_service_g.delete_login_set_for(this_user_name)}), 200

    # Validate one user by id with password
    @app.route("/api/login_set/validate/", methods=["GET"])
    def validate_login_set():
        #print("route create")
        #print(request.url)
        # Get the request user_name arg
        this_user_name = request.args.get("user_name")
        #print(this_user_name)
        # Get the request user_password arg
        this_user_password = request.args.get("user_password")
        #print(this_user_password)
        # Return the serialized (by marshmallow schema) user
        return jsonify({"login_validated" : my_login_set_service_g.validate_login_set(this_user_name, this_user_password)}), 200

    # Fetch data for authenticated user
    @app.route("/api/session/data/", methods=["GET"])
    @login_required
    def get_session_data():
        # Get the request user_name arg
        this_user_name = request.args.get("user_name")
        # Could return any user specific data here
        return jsonify({"user_data" : "This is some private data for {}!".format(this_user_name)})
        print("In session data func")

    # Check if a session exists on our server
    @app.route("/api/session/validate/", methods=["GET"])
    def validate_session():
        if current_user.is_authenticated:
            return jsonify({"login": True})

        return jsonify({"login": False})

    # Create a session if one does not exist

    # This is what generates our csrf token stored as meta data in react app
    @app.route("/api/getcsrf", methods=["GET"])
    def get_csrf():
        token = generate_csrf()
        response = jsonify({"detail": "CSRF cookie set"})
        response.headers.set("X-CSRFToken", token)
        return response

    return app

class TestLoginSet(unittest.TestCase):
    """
    Tester class for login sets
    https://flask.palletsprojects.com/en/1.1.x/reqcontext/
    To run the tests go to top level of flask app and run cmdline "python test_app.py"
    """
    # Create the test client adapter
    client = create_app().test_client()

    def test_empty_count(self):
        print("----------------------------------------------------------------------")
        # Test count
        print("[TEST] Test of empty count")

        response = json.loads(self.client.get("/api/login_set/count", method="GET").get_data())
        #print(response, type(response))
        self.assertEqual(response["login_count"], 0, "This should be 0 as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_empty_find(self):
        print("----------------------------------------------------------------------")
        # Empty find
        print("[TEST] Test of empty find")

        response = json.loads(self.client.get("/api/login_set/find/", method="GET", query_string={"user_name" : "username"}).get_data())
        self.assertEqual(response["login_found"], False, "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_empty_delete(self):
        print("----------------------------------------------------------------------")
        # Test count
        print("[TEST] Test of empty count")

        response = json.loads(self.client.get("/api/login_set/count", method="GET").get_data())
        self.assertEqual(response["login_count"], 0, "This should be 0 as the user has not been posted")

        # Delete
        print("[TEST] Test of empty delete")

        response = json.loads(self.client.get("/api/login_set/delete/", method="GET", query_string={"user_name" : "username"}).get_data())
        self.assertEqual(response["login_deleted"], False, "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_create_and_delete(self):
        print("----------------------------------------------------------------------")
        # Create
        print("[TEST] Test of create and find")

        response = json.loads(self.client.get("/api/login_set/create/", method="GET", query_string={"user_name" : "username", "user_password" : "password"}).get_data())
        self.assertEqual(response["login_created"], True, "This should be true as this is first user post")

        # Test non-empty count
        print("[TEST] Test of non-empty count")

        response = json.loads(self.client.get("/api/login_set/count", method="GET").get_data())
        self.assertEqual(response["login_count"], 1, "This should be 1 as the user has been posted")

        # Test non-empty find
        print("[TEST] Test of non-empty find")

        response = json.loads(self.client.get("/api/login_set/find/", method="GET", query_string={"user_name" : "username"}).get_data())
        self.assertEqual(response["login_found"], True, "This should be true as the user has been posted")

        # Delete and find
        print("[TEST] Test of delete")

        response = json.loads(self.client.get("/api/login_set/delete/", method="GET", query_string={"user_name" : "username"}).get_data())
        self.assertEqual(response["login_deleted"], True, "This should be true as the user has been posted")

        # Test count after delete
        print("[TEST] Test of empty count after delete")

        response = json.loads(self.client.get("/api/login_set/count", method="GET").get_data())
        self.assertEqual(response["login_count"], 0, "This should be 0 as the user has not been posted")
        
        # Empty find after delete
        print("[TEST] Test of empty find after delete")

        response = json.loads(self.client.get("/api/login_set/find/", method="GET", query_string={"user_name" : "username"}).get_data())
        self.assertEqual(response["login_found"], False, "This should be false as the user has not been posted")
        print("----------------------------------------------------------------------")

    def test_validate_and_update_and_delete(self):
        print("----------------------------------------------------------------------")
        # Create
        print("[TEST] Test of create and find")

        response = json.loads(self.client.get("/api/login_set/create/", method="GET", query_string={"user_name" : "username", "user_password" : "password"}).get_data())
        self.assertEqual(response["login_created"], True, "This should be true as this is first user post")

        # Test non-empty count
        print("[TEST] Test of non-empty count")

        response = json.loads(self.client.get("/api/login_set/count", method="GET").get_data())
        self.assertEqual(response["login_count"], 1, "This should be 1 as the user been posted")

        # Test non-empty find
        print("[TEST] Test of non-empty find")

        response = json.loads(self.client.get("/api/login_set/find/", method="GET", query_string={"user_name" : "username"}).get_data())
        self.assertEqual(response["login_found"], True, "This should be true as the user has been posted")

        # Test validate correct
        print("[TEST] Test of validate with correct info")

        response = json.loads(self.client.get("/api/login_set/validate/", method="GET", query_string={"user_name" : "username", "user_password" : "password"}).get_data())
        self.assertEqual(response["login_validated"], True, "This should be true as this is correct info")

        # Test validate incorrect
        print("[TEST] Test of validate with incorrect info")

        response = json.loads(self.client.get("/api/login_set/validate/", method="GET", query_string={"user_name" : "username", "user_password" : "other_password"}).get_data())
        self.assertEqual(response["login_validated"], False, "This should be false as this is incorrect info")

        # Test bad update
        print("[TEST] Test of update with new bad info")

        response = json.loads(self.client.get("/api/login_set/update/", method="GET", query_string={"user_name" : "other_username", "user_password" : "other_password"}).get_data())
        self.assertEqual(response["login_updated"], False, "This should be false as user posted and available for update but this is wrong user")

        # Retest validate correct
        print("[TEST] Retest of validate with correct info after bad update attempt")

        response = json.loads(self.client.get("/api/login_set/validate/", method="GET", query_string={"user_name" : "username", "user_password" : "password"}).get_data())
        self.assertEqual(response["login_validated"], True, "This should be true as this is correct info")

        # Test update
        print("[TEST] Test of update with new info")

        response = json.loads(self.client.get("/api/login_set/update/", method="GET", query_string={"user_name" : "username", "user_password" : "other_password"}).get_data())
        self.assertEqual(response["login_updated"], True, "This should be true as user posted and available for update")

        # Test validate changed correct
        print("[TEST] Test of validate with updated correct info")

        response = json.loads(self.client.get("/api/login_set/validate/", method="GET", query_string={"user_name" : "username", "user_password" : "other_password"}).get_data())
        self.assertEqual(response["login_validated"], True, "This should be true as this is now correct info")
        print("----------------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()
