#Import needed to make this module work
import bcrypt

#Class to represent a user in the system
class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""
    
    #Constructor to initialize the user object
    def __init__(self, id, username, password_hash, role):
        self._id = id #ID for the user
        self._username = username #Username for login
        self._password_hash = password_hash #Hashed password for security
        self._role = role #Role of the user

    #Function to get the username
    def get_username(self):
        return self._username

    #Function to get the user's role
    def get_role(self):
        return self._role

    #Function to verify the password
    def verify_password(self, plain_password):
        """Check if a plain-text password matches this user's hash."""
        #Converting string password into bytes
        pass_bytes = plain_password.encode("utf-8")
        stored_bytes = self._password_hash.encode("utf-8")
        #Checking and verifying whether the provided password matches the stored hashed password
        return bcrypt.checkpw(pass_bytes, stored_bytes)

    #User details
    def __str__(self):
        return f"User: {self._username}, role = {self._role}"