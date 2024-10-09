import re
import requests
from bs4 import BeautifulSoup
import warnings

# Suppress only the specific InsecureRequestWarning from urllib3
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Define patterns for detecting sensitive information, jQuery, and Bootstrap versions
patterns = {
    "api_key": re.compile(r"\b(apiKey|apikey|APIKEY|api_key|API_KEY|secretApiKey)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?"),
    "secret_token": re.compile(r"\b(secret|SECRET|token|TOKEN|secretToken|SECRET_TOKEN)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?"),
    "password": re.compile(r"\b(password|pass|passwd|pwd|PASSWORD|passw|pswd)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?"),
    "hardcoded_credentials": re.compile(r"\b(username|user_name|user-id|userid|userID|USERNAME|uname|uid)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?"),
    "email_id": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "session_id": re.compile(r"\b(session_id|SESSION_ID|sessionToken|SESSION_TOKEN)\s*[:=]\s*[\"']?[A-Za-z0-9-_]+[\"']?"),
    "phone_number": re.compile(r"\b(?:\+?[1-9]\d{0,2})?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b"),
    "jquery_version": re.compile(r"jQuery\s*.*?\s*[\(vV]([\d\.]+)[\)]", re.IGNORECASE),
    "bootstrap_version": re.compile(r"bootstrap\s*.*?v([\d\.]+)", re.IGNORECASE),
}

# Function to fetch the latest jQuery version from the jQuery website
def fetch_latest_jquery_version():
    try:
        response = requests.get("https://code.jquery.com/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        version_tags = soup.find_all('a', href=True)

        for tag in version_tags:
            version_match = re.search(r'jquery-(\d+\.\d+\.\d+)\.min\.js', tag['href'])
            if version_match:
                return version_match.group(1)
        return None
    except requests.RequestException as e:
        print(f"Error fetching latest jQuery version: {e}")
        return None

# Function to fetch the latest Bootstrap version from the Bootstrap website
def fetch_latest_bootstrap_version():
    try:
        response = requests.get("https://getbootstrap.com/docs/versions/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        version_tags = soup.find_all('a', href=True)

        for tag in version_tags:
            version_match = re.search(r'v(\d+\.\d+\.\d+)', tag.text)
            if version_match:
                return version_match.group(1)
        return None
    except requests.RequestException as e:
        print(f"Error fetching latest Bootstrap version: {e}")
        return None

# Static list of known vulnerable jQuery versions
vulnerable_jquery_versions = [
    "1.2.3", "1.2.4", "1.2.5", "1.2.6",
    "1.4.0", "1.4.1", "1.4.2", "1.4.3", "1.4.4",
    "1.5.0", "1.5.1", "1.5.2",
    "1.6.0", "1.6.1", "1.6.2", "1.6.3", "1.6.4",
    "1.7.0", "1.7.1", "1.7.2",
    "1.8.0", "1.8.1", "1.8.2", "1.8.3",
    "1.9.0", "1.9.1",
    "1.10.0", "1.10.1", "1.10.2",
    "1.11.0", "1.11.1", "1.11.2", "1.11.3",
    "1.12.0", "1.12.1", "1.12.2", "1.12.3", "1.12.4",
    "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4",
    "2.1.0", "2.1.1", "2.1.2", "2.1.3", "2.1.4",
    "2.2.0", "2.2.1", "2.2.2", "2.2.3", "2.2.4",
    "3.0.0", "3.0.1",
    "3.1.0", "3.1.1",
    "3.2.0", "3.2.1",
    "3.3.0", "3.3.1",
    "3.4.0", "3.4.1"
]

# Static list of known vulnerable Bootstrap versions
vulnerable_bootstrap_versions = [
    "3.0.0", "3.0.1", "3.0.2", "3.0.3", "3.0.4",
    "3.1.0", "3.1.1",
    "3.2.0", "3.2.1",
    "3.3.0", "3.3.1", "3.3.2", "3.3.3", "3.3.4", "3.3.5", "3.3.6", "3.3.7",
    "4.0.0", "4.0.1", "4.0.2", "4.0.3",
    "4.1.0", "4.1.1", "4.1.2", "4.1.3",
    "4.2.0", "4.3.0", "4.3.1",
    "4.4.0", "4.5.0", "4.5.1", "4.5.2", "4.5.3",
    "4.6.0",
    "5.0.0", "5.0.1", "5.0.2"
]

# Function to scan JavaScript content
def scan_js_content(content):
    lines = content.splitlines()
    sensitive_data = []
    jquery_versions = set()
    bootstrap_versions = set()
    phone_numbers = set()

    for line_number, line in enumerate(lines, 1):
        for pattern_name, pattern in patterns.items():
            matches = pattern.findall(line)
            for match in matches:
                if pattern_name == "jquery_version":
                    jquery_versions.add(match)
                elif pattern_name == "bootstrap_version":
                    bootstrap_versions.add(match)
                elif pattern_name == "phone_number":
                    if re.fullmatch(r"\b\d{10}\b|\b\d{12}\b", match):
                        phone_numbers.add(match)
                else:
                    sensitive_data.append({
                        "pattern": pattern_name,
                        "line_number": line_number,
                        "match": match.strip()
                    })

    return sensitive_data, jquery_versions, bootstrap_versions, phone_numbers

# Function to fetch JavaScript file from URL
def fetch_js_file(url):
    try:
        response = requests.get(url, verify=False)  # Bypass SSL verification
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching file: {e}")
        return None

# Function to extract JavaScript file URLs from the main page
def extract_js_urls(base_url):
    try:
        response = requests.get(base_url, verify=False)  # Bypass SSL verification
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        js_urls = []

        # Find all <script> tags and extract the src attribute
        for script in soup.find_all('script', src=True):
            js_url = script['src']
            if not js_url.startswith('http'):
                js_url = requests.compat.urljoin(base_url, js_url)  # Handle relative URLs
            js_urls.append(js_url)

        return js_urls
    except requests.RequestException as e:
        print(f"Error fetching main page: {e}")
        return []

# Function to check jQuery version from URL or file content
def check_jquery_versions(versions, js_url):
    for version in versions:
        print(f"jQuery version {version} found in {js_url}")
        if version in vulnerable_jquery_versions:
            print(f"Warning: jQuery version {version} is known to be vulnerable!")
        if version != latest_jquery_version:
            print(f"Note: jQuery version {version} is not the latest (latest is {latest_jquery_version}).")

# Function to check Bootstrap version from URL or file content
def check_bootstrap_versions(versions, js_url):
    for version in versions:
        print(f"Bootstrap version {version} found in {js_url}")
        if version in vulnerable_bootstrap_versions:
            print(f"Warning: Bootstrap version {version} is known to be vulnerable!")
        if version != latest_bootstrap_version:
            print(f"Note: Bootstrap version {version} is not the latest (latest is {latest_bootstrap_version}).")

# Function to check for jQuery version in URL
def check_jquery_in_url(url):
    version_match = re.search(r'jquery[-\.]([\d\.]+)\.min\.js', url, re.IGNORECASE)
    return version_match.group(1) if version_match else None

# Function to check for Bootstrap version in URL
def check_bootstrap_in_url(url):
    version_match = re.search(r'bootstrap[-\.]([\d\.]+)\.min\.js', url, re.IGNORECASE)
    return version_match.group(1) if version_match else None

# Main function
def main():
    # Fetch the latest versions
    global latest_jquery_version, latest_bootstrap_version
    latest_jquery_version = fetch_latest_jquery_version()
    latest_bootstrap_version = fetch_latest_bootstrap_version()

    # Check if fetching was successful
    if not latest_jquery_version:
        print("Failed to fetch the latest jQuery version.")
        return

    if not latest_bootstrap_version:
        print("Failed to fetch the latest Bootstrap version.")
        return

    # Ask the user for the application URL
    application_url = input("Enter the application URL: ").strip()
    js_urls = extract_js_urls(application_url)

    if js_urls:
        for js_url in js_urls:
            print(f"Scanning {js_url}...")
            content = fetch_js_file(js_url)
            if content:
                sensitive_data, jquery_versions, bootstrap_versions, phone_numbers = scan_js_content(content)

                # Print sensitive information and phone numbers
                for item in sensitive_data:
                    print(f"Sensitive information found - Pattern: {item['pattern']}, Line: {item['line_number']}, Match: {item['match']}")
                for phone_number in phone_numbers:
                    print(f"Phone number found: {phone_number}")

                # Check for jQuery versions in content and URL
                jquery_version_from_url = check_jquery_in_url(js_url)
                if jquery_version_from_url:
                    jquery_versions.add(jquery_version_from_url)
                check_jquery_versions(jquery_versions, js_url)

                # Check for Bootstrap versions in content and URL
                bootstrap_version_from_url = check_bootstrap_in_url(js_url)
                if bootstrap_version_from_url:
                    bootstrap_versions.add(bootstrap_version_from_url)
                check_bootstrap_versions(bootstrap_versions, js_url)
            else:
                print("Failed to fetch or scan the JavaScript file.")
    else:
        print("No JavaScript files found or failed to extract URLs.")

if __name__ == "__main__":
    main()
