import re
import requests
from bs4 import BeautifulSoup
import warnings

# Suppress only the specific InsecureRequestWarning from urllib3
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Define regex patterns for detecting sensitive information
patterns = {
    "email_id": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "phone_number": re.compile(r"\b(?:\+?[1-9]\d{0,2})?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b"),
    "username": re.compile(r"\b(username|user_name|user-id|userid|userID|USERNAME|uname|uid)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?", re.IGNORECASE),
    "password": re.compile(r"\b(password|pass|passwd|pwd|PASSWORD|passw|pswd)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?", re.IGNORECASE),
    "api_key": re.compile(r"\b(apiKey|apikey|APIKEY|api_key|API_KEY|secretApiKey)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?", re.IGNORECASE),
    "session_id": re.compile(r"\b(session_id|SESSION_ID|sessionToken|SESSION_TOKEN)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?", re.IGNORECASE),
    "access_token": re.compile(r"\b(access_token|accessToken|ACCESS_TOKEN)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?", re.IGNORECASE),
}

# Function to fetch the HTML source code of a webpage
def fetch_html_source(url):
    try:
        response = requests.get(url, verify=False)  # Bypass SSL verification
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Function to scan HTML content for sensitive information
def scan_html_content(content):
    # Split content into lines for line number tracking
    lines = content.splitlines()
    findings = []

    for line_number, line in enumerate(lines, 1):
        # Check for sensitive information in the main HTML content
        findings.extend(scan_line(line, line_number, "main content"))

        # Check for sensitive information in comments
        if "<!--" in line:
            # Extract comments from the line
            comments = extract_comments(line)
            for comment in comments:
                findings.extend(scan_line(comment, line_number, "comment"))

    return findings

# Function to scan a line for sensitive information
def scan_line(line, line_number, source_type):
    findings = []
    for pattern_name, pattern in patterns.items():
        matches = pattern.findall(line)
        for match in matches:
            if pattern_name == "phone_number":
                # Ensure phone number is strictly 10 or 12 digits
                if re.fullmatch(r"\b\d{10}\b|\b\d{12}\b", match):
                    findings.append({
                        "pattern": pattern_name,
                        "line_number": line_number,
                        "match": match.strip(),
                        "source": source_type
                    })
            else:
                findings.append({
                    "pattern": pattern_name,
                    "line_number": line_number,
                    "match": match.strip(),
                    "source": source_type
                })
    return findings

# Function to extract comments from a line
def extract_comments(line):
    comments = re.findall(r"<!--(.*?)-->", line, re.DOTALL)
    return comments

# Main function
def main():
    # Ask the user for the application URL
    application_url = input("Enter the application URL: ").strip()

    # Fetch the HTML source code
    html_content = fetch_html_source(application_url)

    if html_content:
        print("Scanning HTML source code for sensitive information...")
        findings = scan_html_content(html_content)

        if findings:
            for item in findings:
                print(f"Sensitive information found in {item['source']} - Pattern: {item['pattern']}, Line: {item['line_number']}, Match: {item['match']}")
        else:
            print("No sensitive information found.")
    else:
        print("Failed to fetch or scan the HTML source code.")

if __name__ == "__main__":
    main()
