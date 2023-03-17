
from operator import eq
import os
from supabase import create_client, Client
import json

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Function to Fetch All Notes
def find_all_profiles():
    data = supabase.table("profiles").select("*").execute()
    # Equivalent for SQL Query "SELECT * FROM notes;"
    response_data = data.json()
    json_data = json.loads(response_data)['data']
    return json_data

def login_user(email):
    session = supabase.auth.sign_in_with_password({"email": email ,"password": "GaHP3x8jeCURnmDmStp"})
    response_data = session.json()
    json_data = json.loads(response_data)
    supabase.postgrest.auth(session.session.access_token)
    return json_data

def get_user():
    user = supabase.auth.get_user()
    data = supabase.table("task").select("*").execute()
    print(data)


