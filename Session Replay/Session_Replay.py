import requests
def test_session_replay(base_url, internal_url, credentials):
    # Step 5: Create a session and login to the application
    session = requests.Session()
    login_response = session.post(base_url, data=credentials)

    if login_response.status_code == 200: #and "Logout" in login_response.text:
        print("Login successful!")
    else:
        print("Login failed.")
        return

    # Step 6: Access the internal page that requires login
    internal_page_response = session.get(internal_url)

    if internal_page_response.status_code == 200:
        print("Accessed internal page successfully!")
    else:
        print("Failed to access the internal page.")
        return

    # Step 7: Note down the session ID (assuming it's stored in a cookie named 'sessionid')
    session_id = session.cookies.get('HackThisSite')

    if not session_id:
        print("No session ID found.")
        return

    print(f"Session ID noted: {session_id}")

    # Step 8: Logout by accessing a logout endpoint or invalidating the session manually
    # Since there's no logout URL, let's clear cookies manually and invalidate the session
    session.cookies.clear()
    print("Session cookies cleared!")

    # Optional: Access a public page after logout to ensure the session is really cleared
    public_page_response = session.get(base_url)
    if public_page_response.status_code == 200:
        print("Accessed public page after clearing cookies to confirm logout.")

    # Step 9: Create a new session and set the old session ID
    new_session = requests.Session()
    new_session.cookies.set('HackThisSite', session_id, domain=base_url.replace('http://', '').replace('https://', ''))

    # Step 10: Try to access the internal page with the old session ID
    replay_response = new_session.get(internal_url)

    if replay_response.status_code == 200 and "Login" not in replay_response.text:
        print("The accessed internal page is of the previously logged in session")
        print("Session replay is possible")
    else:
        print("The accessed internal page is not of the previously logged in session")
        print("Session replay is not possible")


if __name__ == "__main__":
    # Example usage
    base_url = "https://www.hackthissite.org/"
    internal_url = "https://www.hackthissite.org/playlevel/1/"
    credentials = {"username": "dibili", "password": "Ht5hacking@1128003"}

    test_session_replay(base_url, internal_url, credentials)
