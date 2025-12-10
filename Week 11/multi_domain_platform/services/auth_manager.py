#Import needed to make this module work
import bcrypt
import string
import secrets
from datetime import datetime, timedelta
from services.database_manager import DatabaseManager
from models.users import User

#Class to handle user authentication and validation
class AuthManager:
    """Handles user registration, login and validation."""

    #Constructor to initialize the manager with database access
    def __init__(self, db: DatabaseManager):
        self._db = db

    #Function for password strength
    def check_password_strength(self, password):
        #Flags to check if each character is present
        special = string.punctuation
        has_lower = False
        has_upper = False
        has_digit = False
        has_special = False
        
        #Length check
        if len(password) < 8:
            return "Weak"
        
        #Character checks
        for char in password:
            if char.islower():
                has_lower = True
            elif char.isupper():
                has_upper = True
            elif char.isdigit():
                has_digit = True
            elif char in special:
                has_special = True
        
        #Final check
        if has_lower and has_upper and has_digit and has_special:
            if len(password) >= 12:
                return "Strong"
            else: 
                return "Medium"
        else:
            return "Weak"

    #Function to check if valid username format
    def validate_user(self, username):
        if len(username) < 3 or len(username) > 20:
            return False, 'Error: Username should be between 3 and 20 characters long.'
        for char in username:
            if not char.isalnum():
                return False, 'Error: Username can only contain letters and numbers.'
        return True, ""

    #Function to check if valid password format
    def validate_pass(self, password):
        if len(password) < 6 or len(password) > 50:
            return False, 'Error: Password should be between 6 and 50 characters long.'
        return True, ""

    #Function to login user
    def login_user(self, username, password):
        #Check if user is locked out
        is_locked, msg = self.check_lockout(username)
        if is_locked:
            return None, msg

        #Check whether the username is correct
        row = self._db.fetch_one("SELECT id, username, password_hash, role FROM users WHERE username = ?", (username,))
        
        if not row:
            return None, "Incorrect username or this user doesn't exist."
        
        #Create User object from the database row
        user = User(row[0], row[1], row[2], row[3])

        #Check for password match using User model method
        if user.verify_password(password):
            #If password is correct, resets whatever lockout
            self.reset_lockout(username)
            
            #Create and log session token
            token = self._create_session(username)
            
            return user, token, f'Successfully logged in {username}. Session Token: {token}'
        else:
            #Records attempt, if it hits 3, automatically locks out user
            self.record_failed_attempt(username)
            attempts, last_time = self.get_lockout_status(username)
            if attempts >= 3:
                return None, None, f"User - {username} is now locked out due to three failed attempts.\nPlease try again after 5 minutes."
            return None, None, "Incorrect password, please try again."
    
    #Function to create and log a session token
    def _create_session(self, username):
        token = secrets.token_hex(16)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._db.execute_query(
            "INSERT INTO sessions (username, token, created_at) VALUES (?, ?, ?)", 
            (username, token, created_at)
        )
        return token

    #Function to register user
    def register_user(self, username, password, group_choice):
        #Check if username already exists 
        if self._db.fetch_one("SELECT 1 FROM users WHERE username = ?", (username,)):
            return False, f'Username {username} already exists, please enter a different one.'
        
        # Hashing the password
        pass_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashpass = bcrypt.hashpw(pass_bytes, salt).decode("utf-8")
        
        #Group assignment
        group_map = {
            "Cybersecurity Analyst": "Cybersecurity Analyst",
            "Data Scientist": "Data Scientist",
            "IT Administrator": "IT Administrator"
        }
        role = group_map.get(group_choice, "user")
            
        #Storing in database
        self._db.execute_query("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, hashpass, role))
        return True, f"User: {username} is now registered."

    #Function for lockout status
    def get_lockout_status(self, username):
        row = self._db.fetch_one("SELECT failed_attempts, last_attempt_time FROM lockout WHERE username = ?", (username,))
        if row:
            last_time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            return (row[0], last_time) 
        return (0, None)

    #Function to increment amount of failed attempts
    def record_failed_attempt(self, username):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #If record doesn't exist, creates it 
        self._db.execute_query("INSERT OR IGNORE INTO lockout (username, failed_attempts, last_attempt_time) VALUES (?, 0, ?)", (username, now_str))
        #Update the records
        self._db.execute_query("UPDATE lockout SET failed_attempts = failed_attempts + 1, last_attempt_time = ? WHERE username = ?", (now_str, username))

    #Function to reset lockout if they get password correct or if 5 minutes has passed
    def reset_lockout(self, username):
        self._db.execute_query("DELETE FROM lockout WHERE username = ?", (username,))

    #Function to check if the user is currently locked out
    def check_lockout(self, username):
        attempts, last_time = self.get_lockout_status(username)
        
        if attempts >= 3:
            if last_time and (datetime.now() - last_time < timedelta(minutes=5)):
                return True, f"Your account '{username}' is locked, please try again 5 minutes after you have been locked out."
            else:
                #If lockout is expired, reset it
                self.reset_lockout(username)
                return False, ""
        return False, ""