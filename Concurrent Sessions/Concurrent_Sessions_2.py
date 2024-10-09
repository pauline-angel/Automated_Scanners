import requests

# Define user agents for different browsers
USER_AGENTS = {
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
}

def login_and_get_session(login_url, username, password, user_agent):
    # Define the login payload
    payload = {
        'username': username,
        'password': password
    }

    # Create a session and set headers to mimic a specific browser
    session = requests.Session()
    session.headers.update({
        'User-Agent': user_agent,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    })

    # Attempt to log in
    response = session.post(login_url, data=payload)

    # Check if login was successful
    if response.ok and "Welcome" in response.text:  # Adjust the success condition based on the application
        print(f"Login successful. Session ID: {session.cookies.get_dict()}")
        return session
    else:
        print(f"Login failed: {response.text}")
        return None

def check_concurrent_sessions(login_url, protected_url, username, password):
    # Log in to the application with the first session (simulating Chrome browser)
    print("Logging in with Chrome browser...")
    session1 = login_and_get_session(login_url, username, password, USER_AGENTS['chrome'])
    if not session1:
        return

    # Log in to the application with the second session (simulating Firefox browser)
    print("Logging in with Firefox browser...")
    session2 = login_and_get_session(login_url, username, password, USER_AGENTS['firefox'])
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
            print("First session (Chrome) is invalid after second login.")
        if not response2.ok:
            print("Second session (Firefox) is invalid.")

# Usage
login_url = "https://www.hackthissite.org/"  # Replace with the actual login URL
protected_url = "https://www.hackthissite.org/"  # Replace with a protected resource URL
username = "dibili"
password = "Ht5hacking@1128003"

check_concurrent_sessions(login_url, protected_url, username, password)
