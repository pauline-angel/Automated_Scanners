import requests
from urllib.parse import urlencode
import concurrent.futures
import re

def read_payloads(file_path):
    """
    Read payloads from a text file and return them as a list.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def is_vulnerable(response, payload):
    """
    Check if the payload executed successfully by searching for an indicator in the response.
    """
    # Define a unique identifier to search for in the response
    xss_identifier = "XSS"

    # Check if the response contains the identifier, suggesting successful XSS execution
    return xss_identifier in response.text

def test_xss(url, parameter, payloads):
    """
    Test for XSS vulnerability using a list of payloads.
    """
    vulnerable_payloads = []

    for payload in payloads:
        # Construct the URL with the payload as a query parameter
        params = {parameter: payload}
        query_string = urlencode(params)
        test_url = f"{url}?{query_string}"

        try:
            # Send a GET request to the URL
            response = requests.get(test_url, timeout=5)

            # Debug: Print the URL being tested
            print(f"Testing URL: {test_url}")

            # Check if the payload is reflected and executed in the response
            if is_vulnerable(response, payload):
                vulnerable_payloads.append((test_url, payload))
                print(f"Vulnerable URL Found: {test_url}\nPayload: {payload}\n")

        except requests.RequestException as e:
            print(f"Request failed for {test_url}: {e}")

    return vulnerable_payloads

def main():
    url = input("Enter the target URL: ").strip()
    parameter = input("Enter the parameter name to test (e.g., 'q'): ").strip()
    payloads_file = 'C:/Users/C-DAC/Desktop/xss_payloads.txt'

    # Read payloads from the file
    payloads = read_payloads(payloads_file)

    # Use ThreadPoolExecutor for parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Divide payloads into chunks and test concurrently
        futures = [executor.submit(test_xss, url, parameter, payloads[i:i + 100]) for i in range(0, len(payloads), 100)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Flatten the list of results
    vulnerable_results = [item for sublist in results for item in sublist]

    if vulnerable_results:
        print("\nSummary of vulnerable URLs and payloads:")
        for test_url, payload in vulnerable_results:
            print(f"URL: {test_url}\nPayload: {payload}\n")
    else:
        print("No XSS vulnerabilities found.")

if __name__ == '__main__':
    main()
