import requests

def login_and_get_session(login_url, username, password):
    # Define the login payload
    payload = {
        'username': input('Give the username field ID:'),#username,
        'password': input('Give the password field ID:')#password
    }

    # Create a session and attempt to log in
    session = requests.Session()
    response = session.post(login_url, data=payload)

    # Check if login was successful
    if response.ok:
        print("Login successful. Session ID:", session.cookies.get_dict())
        return session
    else:
        print("Login failed:", response.text)
        return None

def check_concurrent_sessions(login_url, protected_url, username, password):
    # Log in to the application with the first session (simulating first browser)
    session1 = login_and_get_session(login_url, username, password)
    if not session1:
        return

    # Log in to the application with the second session (simulating second browser)
    session2 = login_and_get_session(login_url, username, password)
    if not session2:
        return

    # Access a protected resource with both sessions
    response1 = session1.get(protected_url)
    response2 = session2.get(protected_url)

    # Check if both sessions are valid
    if response1.ok and response2.ok:
        print("Both sessions are valid. Concurrent sessions are allowed.")
    else:
        print("Concurrent sessions are not allowed.")
        if not response1.ok:
            print("First session is invalid after second login.")
        if not response2.ok:
            print("Second session is invalid.")

# Usage
login_url = input("Give the application login URL:")
#"https://www.hackthissite.org/"  # Replace with the actual login URL
protected_url = input("Give the application's dashboard URL:")  # Replace with a protected resource URL
username = input("Enter Username for login:")
#"dibili"
password = input("Enter Password for login:")
#"Ht5hacking@1128003"

check_concurrent_sessions(login_url, protected_url, username, password)
