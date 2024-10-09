import requests

def test_session_replay(base_url, internal_url, credentials):
    # Step 5: Create a session and login to the application
    session = requests.Session()
    login_response = session.post(base_url, data=credentials)

    if login_response.status_code == 200:
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
    session_id = session.cookies.get('HackThisSite') #HackThisSite

    if not session_id:
        print("No session ID found.")
        return

    print(f"Session ID noted: {session_id}")

    # Step 8: Logout by clearing cookies manually
    session.cookies.clear()
    print("Logged out")

    # Step 10: Set the old session ID back in the same session
    session.cookies.set('HackThisSite', session_id, domain=base_url.replace('http://', '').replace('https://', ''))

    # Try to access the internal page with the old session ID in the same session
    replay_response = session.get(internal_url)

    if replay_response.status_code == 200 and "Logout" in replay_response.text:
        print("The accessed internal page is of the previously logged in session.")
        print("Session replay is possible")
    else:
        print("The accessed internal page is not of the previously logged in session")
        print("Session replay is not possible")

if __name__ == "__main__":
    # Example usage
    base_url = "https://www.hackthissite.org/"#"http://127.0.0.1:5000/login"#
    internal_url = "https://www.hackthissite.org/playlevel/1/"#"http://127.0.0.1:5000/internal"#
    #credentials = {"username": "user1", "password": "password1"}
    credentials = {"username": "dibili", "password": "Ht5hacking@1128003"}

    test_session_replay(base_url, internal_url, credentials)
