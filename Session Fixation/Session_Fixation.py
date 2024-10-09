import requests
from bs4 import BeautifulSoup  # Optional, for parsing HTML

# URL of the login page and other relevant endpoints
login_url = input("Give the Application's Login URL:")
#https://www.hackthissite.org/
#login_url = base_url

# Headers to use in the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Login credentials
login_data = {
    input("Give the username field id:") : input("Give the username:"),
    input("Give the password field id:") : input("Give the password:")
    #"username": "dibili",  # Use the correct name for the username field
    #"password": "Ht5hacking@1128003"  # Use the correct name for the password field
}

# Start a session
session = requests.Session()

# Make a GET request to the login page to retrieve any necessary tokens (e.g., CSRF)
response = session.get(login_url, headers=headers)

# Debug: Print initial cookies and response details
print("Initial cookies:", session.cookies)
#print("Response status code:", response.status_code)
#print("Response headers:", response.headers)

# Extract the initial session ID for the specific domain
original_session_id = session.cookies.get("HackThisSite", domain="www.hackthissite.org")

if original_session_id is None:
    print("Failed to retrieve initial session ID.")
else:
    print(f"Original session ID: {original_session_id}")

    # Manipulate the session ID by changing a few characters
    manipulated_session_id = original_session_id[:5] + "ABCDEF" + original_session_id[11:]
    print(f"Manipulated session ID: {manipulated_session_id}")

    # Set the manipulated session ID for the same domain
    session.cookies.set("HackThisSite", manipulated_session_id, domain="www.hackthissite.org")

    # Debug: Print manipulated cookies
    print("Manipulated cookies:", session.cookies)

    # Check if any tokens are needed (e.g., CSRF)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: CSRF token extraction if needed
    csrf_token = soup.find("input", {"name": "CSRFToken"})  # Replace with actual token field name

    if csrf_token:
        login_data["CSRFToken"] = csrf_token["value"]  # Add CSRF token to login data

    # Perform the login
    response = session.post(login_url, data=login_data, headers=headers)

    # Check if login was successful by looking for a known element or response status
    if "Logout" in response.text or response.status_code == 200:
        print("Login successful")

        # Debug: Print cookies after login
        print("Cookies after login:", session.cookies)

        # Check if the session ID remained the same for the specific domain
        post_login_session_id = session.cookies.get("HackThisSite", domain="www.hackthissite.org")

        if post_login_session_id == manipulated_session_id:
            print("Session fixation possible: Session ID was not changed after login")
        else:
            print("Session fixation mitigated: Session ID was changed after login")
    else:
        print("Login failed")
        print("Response content:", response.text)  # Debug: Print response content
