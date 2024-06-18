from dotenv import load_dotenv
import os
from twikit import Client 

def load_credentials():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

    dotenv_path = os.path.join(project_root, '.env')

    load_dotenv(dotenv_path)

    user = os.getenv('USERNAME')

    email = os.getenv('EMAIL')

    password = os.getenv('PASSWORD')
    
    secur_code = input('Enter your security code: \n')
    
    real_password = password + secur_code
    
    google_auth = input('Enter your google auth code: \n')
    
    return {
      "user": user,
      "email": email,
      "password": real_password,
      "google_auth": google_auth
    }
    
def client_login():
    credentials = load_credentials()
    client = Client('en-US')
    
    client.login(
      auth_info_1=credentials['user'],
      auth_info_2=credentials['email'],
      password=credentials['password'],
      totp_secret=credentials['google_auth'],
    )
    
    return client
    
try:
    print("Logging in...")
    test_client = client_login()
    print("Login successful")
    test_user = test_client.get_user_by_id("ericsmith1302")
    print(test_user)
except Exception as e:
    print(e)

      