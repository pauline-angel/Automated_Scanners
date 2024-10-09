import requests
from bs4 import BeautifulSoup

# URL of the login page and other relevant endpoints
login_url = input("Give the Application's Login URL: ")

# Headers to use in the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Login credentials
login_data = {
    input("Give the username field id: "): input("Give the username: "),
    input("Give the password field id: "): input("Give the password: ")
}

# Start a session
session = requests.Session()

# Make a GET request to the login page to retrieve any necessary tokens (e.g., CSRF)
response = session.get(login_url, headers=headers)

# Debug: Print initial cookies and response details
print("Initial cookies:", session.cookies)

# Extract the initial session ID
original_session_id = session.cookies.get("HackThisSite", domain="www.hackthissite.org")

if original_session_id is None:
    print("Failed to retrieve initial session ID.")
else:
    print(f"Original session ID: {original_session_id}")

    # Manipulate the session ID by changing a few characters
    manipulated_session_id = original_session_id[:5] + "ABCDEF" + original_session_id[11:]
    print(f"Manipulated session ID: {manipulated_session_id}")

    # Set the manipulated session ID
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

        # Check if the session ID remained the same
        post_login_session_id = session.cookies.get("HackThisSite", domain="www.hackthissite.org")

        if post_login_session_id == manipulated_session_id:
            print("Session fixation possible: Session ID was not changed after login")
        else:
            print("Session fixation mitigated: Session ID was changed after login")

        # Attempt to find and click the logout button
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to find the logout link/button
        logout_link = soup.find('a', string="Logout")  # Common logout link

        if not logout_link:
            # Try to find the logout form button if the link is not present
            logout_form = soup.find('form', {'id': 'logout_form'})  # Adjust the ID as needed
            if logout_form:
                logout_action = logout_form.get('action')
                logout_url = response.url + logout_action
                print(f"Logout form action found: {logout_url}")
                response = session.post(logout_url, headers=headers)
            else:
                print("Logout form not found")
        else:
            logout_url = logout_link.get('href')
            print(f"Logout link found: {logout_url}")
            response = session.get(logout_url, headers=headers)

        # Check if logout was successful
        if "Login" in response.text or response.status_code == 200:
            print("Logout successful")

            # Debug: Print cookies after logout
            print("Cookies after logout:", session.cookies)

            # Check if the session ID changed after logout
            post_logout_session_id = session.cookies.get("HackThisSite", domain="www.hackthissite.org")

            if post_logout_session_id == post_login_session_id:
                print("Session not invalidated: Session ID remained the same after logout")
            else:
                print("Session invalidated: Session ID changed after logout")
        else:
            print("Logout failed")
            print("Response content:", response.text)  # Debug: Print response content
    else:
        print("Login failed")
        print("Response content:", response.text)  # Debug: Print response content
