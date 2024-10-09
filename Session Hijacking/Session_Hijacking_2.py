import requests

def login_and_get_session_id(url, login_route, username, password, protected_route):
    login_url = f"{url}/{login_route}"

    # Step 1: Log in to the application and get the session cookie
    session = requests.Session()
    login_payload = {
        input("Enter the username field ID:"): username,
        # username
        input("Enter the password field ID:"): password
        #password
    }

    print(f"Sending login request to: {login_url}")
    response = session.post(login_url, data=login_payload)

    #print(f"Login response status code: {response.status_code}")
    #print(f"Login response headers: {response.headers}")

    # Check if login was successful and a session cookie is set
    if response.status_code == 200 and 'Set-Cookie' in response.headers:
        # Step 3: Navigate to the protected URL
        protected_url = f"{url}/{protected_route}"
        print("Login Success")
        print(f"Accessing protected URL: {protected_url}")
        protected_response = session.get(protected_url)

        #print(f"Protected URL response status code: {protected_response.status_code}")
        #print(f"Protected URL response headers: {protected_response.headers}")

        if protected_response.status_code == 200:
            # Note down the session ID
            session_cookie = session.cookies.get_dict()
            print(f"Session ID after login and accessing protected URL: {session_cookie}")
            return session_cookie
        else:
            print("Failed to access the protected URL after login.")
            return None
    else:
        print("Login failed or no session cookie set.")
        return None


def hijack_session_and_test(url, protected_route, session_cookie):
    # Step 1 (Browser 2): Open the application URL (simulate by starting a new session)
    new_browser_session = requests.Session()

    # Step 2: Manually set the session ID to the one previously obtained after login
    new_browser_session.cookies.update(session_cookie)

    print(f"Using hijacked session ID: {session_cookie}")

    # Step 3: Attempt to access the protected URL with the hijacked session cookie
    protected_url = f"{url}/{protected_route}"
    print(f"Accessing protected URL with hijacked session: {protected_url}")
    hijacked_response = new_browser_session.get(protected_url)

    # Step 4: Check if the protected page is accessible
    #print(f"Hijacked session response status code: {hijacked_response.status_code}")
    #print(f"Hijacked session response headers: {hijacked_response.headers}")

    if hijacked_response.status_code == 200:#and "Login" in hijacked_response.text:
        print("Protected page accessed without login.")
        print("Session Hijacking Possible")
        #print("Protected page content:")
        #print(hijacked_response.text)
    else:
        print("No session hijacking vulnerability detected.")


# Example usage
application_url = input("Enter the application URL:")#"https://www.hackthissite.org/"
login_route = input("Enter the login page route:")#"https://www.hackthissite.org/"
protected_route = input("Enter the internal page route:")#"playlevel/1/" (route after login)
username = input("Enter Login Username:")#"dibili"
password = input("Enter Login Password:")#"Ht5hacking@1128003"

# Step 1-4: Browser 1 - Login, navigate to protected URL, and note down the session ID
session_cookie = login_and_get_session_id(application_url, login_route, username, password, protected_route)

# Step 1-4: Browser 2 - Use the noted session ID to hijack the session
if session_cookie:
    hijack_session_and_test(application_url, protected_route, session_cookie)
