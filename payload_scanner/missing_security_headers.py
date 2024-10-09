import requests
from tabulate import tabulate

# Define a list of important security headers to check for
REQUIRED_SECURITY_HEADERS = {
    "Content-Type": "Can lead to MIME-type sniffing, causing browsers to misinterpret content and potentially execute scripts, resulting in XSS attacks.",
    "Content-Security-Policy": "Without CSP, an application is vulnerable to XSS attacks, clickjacking, and loading of unauthorized resources, which can lead to data theft and code injection.",
    "Strict-Transport-Security": "Users may access the site over HTTP, leading to man-in-the-middle attacks and SSL stripping.",
    "X-Content-Type-Options": "Browsers might execute scripts with incorrect MIME types, leading to execution vulnerabilities.",
    "X-Frame-Options": "Pages could be embedded in iframes, leading to clickjacking attacks and UI redress vulnerabilities.",
    "X-XSS-Protection": "Leaves the application open to XSS attacks that browsers could otherwise block or sanitize.",
    "Referrer-Policy": "Sensitive URLs or data may be exposed to external sites, leading to information leakage and potential privacy violations.",
    "Permissions-Policy": "Unauthorized access to features like camera and microphone, leading to privacy invasions and feature exploitation.",
    "Cross-Origin-Resource-Policy": "Unauthorized origins may access resources, leading to data theft and content leakage.",
    "Access-Control-Allow-Origin": "Cross-origin requests may be blocked, disrupting legitimate access; or if misconfigured, could expose resources to malicious domains."
}

def check_security_headers(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Print the HTTP status code
        print(f"HTTP Status Code: {response.status_code}\n")

        # Check if the response is successful
        if response.status_code == 200:
            # Fetch headers
            headers = response.headers

            # Print received headers
            print("Received Headers:")
            for header, value in headers.items():
                print(f"{header}: {value}")
            print("\n")

            # Check for missing security headers
            missing_headers = []
            for header, description in REQUIRED_SECURITY_HEADERS.items():
                if header not in headers:
                    missing_headers.append((header, description))

            # Display missing headers in a table format
            if missing_headers:
                print("Missing Security Headers:")
                print(tabulate(missing_headers, headers=["Missing Header", "Impact"], tablefmt="pretty", colalign=("left", "left")))
            else:
                print("All required security headers are present.")
        else:
            print("Failed to fetch the URL.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Replace with the URL you want to check
url = input("Enter the URL of the application: ")
check_security_headers(url)
