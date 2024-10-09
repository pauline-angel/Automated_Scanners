import requests
from bs4 import BeautifulSoup

def check_tab_nabbing(url):
    try:
        # Make a request to the given URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags
        links = soup.find_all('a')

        # Check for tab nabbing vulnerability
        vulnerable_links = []
        for link in links:
            # Check if link has target="_blank" and lacks rel="noopener" or rel="noreferrer"
            if link.get('target') == '_blank':
                rel = link.get('rel')
                if rel is None or ('noopener' not in rel and 'noreferrer' not in rel):
                    vulnerable_links.append(link.get('href'))

        # Print results
        if vulnerable_links:
            print("Tab nabbing (target=_blank) found")
            #print("Potentially vulnerable links found:")
            #for vuln_link in vulnerable_links:
                #print(f"- {vuln_link}")
        else:
            print("No tab nabbing vulnerabilities found.")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

if __name__ == "__main__":
    url = input("Enter the application URL to test for tab nabbing vulnerability: ")
    check_tab_nabbing(url)
