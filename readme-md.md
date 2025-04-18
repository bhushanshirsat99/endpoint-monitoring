# Endpoint Monitoring Tool

This tool monitors the availability of HTTP/HTTPS endpoints based on a YAML configuration file and reports cumulative availability percentage by domain.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/endpoint-monitoring.git
   cd endpoint-monitoring
   ```

2. Install the required dependencies:
   ```
   pip install pyyaml requests
   ```

## Usage

Run the monitoring tool with a YAML configuration file:

```
python monitor.py <config_file_path>
```

For example:
```
python monitor.py sample.yaml
```

The tool will check the availability of all endpoints specified in the YAML file every 15 seconds and output the cumulative availability percentage by domain.

To stop the monitoring, press `Ctrl+C`.

## YAML Configuration Format

The YAML configuration file should contain a list of endpoint definitions. Each endpoint should have:

- `name` (string, required): A description of the HTTP endpoint
- `url` (string, required): The URL of the HTTP endpoint
- `method` (string, optional): The HTTP method (defaults to GET if omitted)
- `headers` (dictionary, optional): HTTP headers to include in the request
- `body` (string, optional): JSON-encoded body to include in the request

Example:
```yaml
- name: sample index up
  url: https://example.com/
- name: sample post endpoint
  url: https://example.com/api
  method: POST
  headers:
    content-type: application/json
  body: '{"key":"value"}'
```

## Identified Issues and Implemented Changes

1. **Timeout Handling**
   - Issue: The original code had no timeout enforcement for the 500ms requirement
   - Change: Added a 0.5-second timeout parameter to all requests

2. **Response Time Measurement**
   - Issue: The code didn't measure response time
   - Change: Added time tracking to verify endpoints respond within 500ms

3. **Domain Extraction**
   - Issue: The original domain extraction didn't handle port numbers correctly
   - Change: Implemented proper domain extraction using `urlparse` to remove port numbers

4. **Default HTTP Method**
   - Issue: No default method was set when omitted in the YAML
   - Change: Added a default 'GET' method when not specified

5. **Availability Percentage Format**
   - Issue: Availability percentages included decimal points
   - Change: Modified the code to drop decimals from availability percentages using `int()`

6. **Check Cycle Timing**
   - Issue: The original code didn't ensure checks happen every 15 seconds regardless of processing time
   - Change: Added cycle time tracking and dynamic sleep calculation to maintain consistent 15-second intervals

7. **JSON Body Handling**
   - Issue: The body parameter was passed directly without handling None values
   - Change: Added conditional to only pass body if it exists

## Availability Criteria

An endpoint is considered available only if:
1. The HTTP status code is between 200 and 299
2. The endpoint responds in 500ms or less

The tool calculates availability cumulatively from the start of monitoring and groups results by domain (ignoring port numbers).
