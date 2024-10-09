import requests
import difflib


def test_session_replay(base_url, internal_url, credentials):
    # Create a session
    session = requests.Session()

    # Step 5: Login to the application
    login_response = session.post(base_url, data=credentials)
    if login_response.status_code == 200:
        print("Login successful!")
    else:
        print("Login failed.")
        return

    # Step 6: Access the internal page that requires login
    internal_page_response = session.get(internal_url)
    if internal_page_response.status_code == 200:
        internal_page_content = internal_page_response.text
        print("Accessed internal page successfully!")
    else:
        print("Failed to access the internal page.")
        return

    # Debug: Show part of the internal page content for verification
    print("Internal page content length before logout:", len(internal_page_content))

    # Step 7: Note down the session ID (assuming it's stored in a cookie named 'session_id')
    session_id = session.cookies.get('HackThisSite')
    if not session_id:
        print("No session ID found.")
        return

    print(f"Session ID noted: {session_id}")

    # Step 8: Logout by clearing cookies manually
    session.cookies.clear()
    print("Session cookies cleared!")

    # Debug: Verify cookies after clearing
    print(f"Session cookies after logout: {session.cookies}")

    # Step 9: Attempt to access the internal page again with the same session
    replay_response = session.get(internal_url)
    print(f"Accessing internal URL after clearing cookies: {internal_url}")

    # Step 10: Compare the HTML content of the internal page
    if replay_response.status_code == 200:
        replay_page_content = replay_response.text
        print("Replayed internal page content length:", len(replay_page_content))

        if replay_page_content == internal_page_content:
            print("The HTML content matches the previous session content")
            print("Session replay is possible")
        else:
            print("The HTML content does not match the previous session content")
            print("Session replay is not possible")

            # Print differences
            diff = difflib.unified_diff(
                internal_page_content.splitlines(),
                replay_page_content.splitlines(),
                fromfile='Original Content',
                tofile='Replayed Content'
            )

            print("\n".join(diff))
    else:
        print(f"Failed to access internal URL after logout. Status code: {replay_response.status_code}")
        print("Session replay is not possible")


if __name__ == "__main__":
    # Example usage
    base_url = "https://www.hackthissite.org/"
    internal_url = "https://www.hackthissite.org/playlevel/1/"
    credentials = {"username": "dibili", "password": "Ht5hacking@1128003"}

    test_session_replay(base_url, internal_url, credentials)
