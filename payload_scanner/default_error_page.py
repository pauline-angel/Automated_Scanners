import requests


def test_error_pages(base_url):
    # List of common keywords found in default error pages
    default_error_keywords = [
        'Not Found', 'Internal Server Error', 'Forbidden', 'nginx',
        'Server Error', 'Apache/1.3.27', 'Server', 'Port 80',
        'Port 40', 'HTTP Status 418', 'Unknown Reason',
        'Apache Tomcat/8.5.14'
    ]

    # List of common error URLs
    error_urls = [
        '/restricted', '/forbidden', '/robots.txt', '/admin', '/etc/passwd', '/assets/js/',
        '/private', '/secure', '/cgi-bin', '/config', '/settings', '/database', '/archive',
        '/port80', '/port443', '/ftp', '/404', '/500', '/403', '/401', '/418', '/default.html',
        '/index.html', '/index.php'
    ]

    # Headers to use for the requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for error_url in error_urls:
        url = base_url.rstrip('/') + error_url
        try:
            response = requests.get(url, headers=headers)

            print(f"Testing URL: {url}")
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.text)} characters")

            # Check if any keyword from the list is present in the response text
            found_keywords = [keyword for keyword in default_error_keywords if keyword in response.text]

            if found_keywords:
                print("This might be a default error page.")
                print("The keywords found in the error page:", ", ".join(found_keywords))
            else:
                print("This might be a custom error page.")

            print("-" * 40)
        except requests.RequestException as e:
            print(f"Request failed for URL: {url}")
            print(f"Error: {e}")
            print("-" * 40)


if __name__ == "__main__":
    base_url = input("Enter the application URL: ")
    test_error_pages(base_url)
