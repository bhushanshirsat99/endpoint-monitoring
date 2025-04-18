import yaml
import requests
import time
from collections import defaultdict
import sys
from urllib.parse import urlparse

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')  # Default to GET if method not specified
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    try:
        # Using timeout of 0.5 seconds (500ms) as per requirements
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body if body else None, timeout=0.5)
        response_time = time.time() - start_time
        
        # Check if status code is between 200-299 and response time <= 500ms
        if 200 <= response.status_code < 300 and response_time <= 0.5:
            return "UP"
        else:
            return "DOWN"
    except (requests.RequestException, requests.Timeout):
        return "DOWN"

# Function to extract domain name without port
def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.split(':')[0]  # Remove port number if present

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    try:
        while True:
            cycle_start_time = time.time()
            
            for endpoint in config:
                domain = extract_domain(endpoint["url"])
                result = check_health(endpoint)

                domain_stats[domain]["total"] += 1
                if result == "UP":
                    domain_stats[domain]["up"] += 1

            # Log cumulative availability percentages
            for domain, stats in domain_stats.items():
                # Drop any availability after the decimal point as required
                availability = int(100 * stats["up"] / stats["total"])
                print(f"{domain} has {availability}% availability percentage")

            print("---")
            
            # Calculate how long to sleep to ensure 15-second cycles
            elapsed_time = time.time() - cycle_start_time
            sleep_time = max(0, 15 - elapsed_time)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
