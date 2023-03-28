
import os
from supabase import create_client, Client
from utils import convert_DTO_task_list, convert_DTO_to_task
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

def login_user(email, password):
    # session = supabase.auth.sign_in_with_password({"email": email ,"password": "GaHP3x8jeCURnmDmStp"})
    session = supabase.auth.sign_in_with_password({"email": email ,"password": password})
    response_data = session.json()
    json_data = json.loads(response_data)
    supabase.postgrest.auth(session.session.access_token)
    return json_data

def get_user(token):
    user = supabase.auth.get_user(token)
    response_data = user.json()
    json_data = json.loads(response_data)['user']
    return json_data

def get_task_list(token):
    supabase.postgrest.auth(token)
    data = supabase.table("task").select("id, name, active , inserted_at, name, description, updated_at, duration,frequency,task_note(id, note, inserted_at, time),subtask(id, name, description, complete, inserted_at)")\
        .execute()
    response_data = data.json()
    task_list = json.loads(response_data)['data']
    updated_task_list = convert_DTO_task_list(task_list)
    return updated_task_list

def get_task(token, task_id):
    supabase.postgrest.auth(token)
    data = supabase.table("task")\
        .select("id, name, active , inserted_at, name, description, updated_at, duration,frequency,task_note(id, note, inserted_at, time),subtask(id, name, description, complete, inserted_at)")\
        .eq("id", task_id)\
        .execute()
    response_data = data.json()
    task = json.loads(response_data)['data'][0]
    updated_task = convert_DTO_to_task(task)
    return updated_task
    
def add_scheduled_task(token, task_id):
    supabase.postgrest.auth(token)
    supabase.table("scheduled_task")\
        .upsert({"task_id": task_id, })
