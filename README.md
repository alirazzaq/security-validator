# Security Validator Toolkit 🛡️

A generic and configurable Python-based toolkit for deterministically validating web security findings.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features-)
- [Installation](#installation-)
- [Usage](#usage-)
  - [Command-Line Arguments](#command-line-arguments)
- [Validator Deep Dive](#validator-deep-dive)
  - [Cross-Site Scripting (XSS)](#1-cross-site-scripting-xss-)
  - [Open Redirect](#2-open-redirect-️)
  - [SQL Injection (SQLi)](#3-sql-injection-sqli-)
  - [Remote Code Execution (RCE) / File Read](#4-remote-code-execution-rce--file-read-)
  - [Server-Side Request Forgery (SSRF)](#5-server-side-request-forgery-ssrf-)
- [Handling Advanced Use Cases](#handling-advanced-use-cases-)
- [AI Assistance](#ai-assistance-)

---

## Overview

This tool helps security professionals, developers, and penetration testers quickly confirm if a potential vulnerability is a **true positive** or a **false positive**. Unlike hardcoded scripts, this toolkit is built to work with any web application by accepting all necessary parameters—such as target URL, credentials, and headers—directly from the command line.

---

## Key Features ✨

* **Completely Generic:** No hardcoded URLs, credentials, or application-specific logic.
* **Modular Design:** Each vulnerability class has its own validator, making the tool easy to maintain and extend.
* **Multiple Vulnerability Classes:** Supports XSS, Open Redirect, SQL Injection, RCE/File Read, and SSRF.
* **Authentication Support:** Test endpoints protected by tokens or cookies using custom HTTP headers.
* **Flexible Output:** Choose between human-readable text or machine-readable JSON.
* **Supports GET & POST:** Validate vulnerabilities in both URL parameters and request bodies.

---

## Installation ⚙️

### **1. Prerequisites**
- Python 3.7+
- Google Chrome browser
- **ChromeDriver**: You must download the ChromeDriver that matches your Chrome browser [here](https://chromedriver.chromium.org/downloads). Ensure the executable is in your system's `PATH`.

### **2. Setup Instructions**
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/alirazzaq/security-validator.git](https://github.com/alirazzaq/security-validator.git)
    cd security-validator
    ```

2.  **Create & Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
---

## Usage 🚀

The toolkit is operated via the command line with a simple and consistent structure.

```bash
python validator.py --type <type> --url <target_url> --payload "<payload>" [options]

## Validator Deep Dive

### 1. Cross-Site Scripting (XSS) 💉
* **How It Works:** The validator launches a headless Chrome browser, navigates to the target URL with the payload, and checks for evidence of JavaScript execution.
* **Theoretical Justification:** The only reliable way to validate XSS is to confirm that an injected script **executes** in a browser environment. Simply checking if a payload is reflected in the HTML source is insufficient, as modern frameworks or Content Security Policies (CSPs) can prevent execution. Using a **headless browser** simulates a real user environment, including a JavaScript engine, providing definitive proof of execution by detecting events like `alert()` popups.
* **Test Cases:**
    * **True Positive:**
        ```bash
        python validator.py --type xss --url "[http://testphp.vulnweb.com/listproducts.php?cat=](http://testphp.vulnweb.com/listproducts.php?cat=)" --payload "<script>alert('xss')</script>"
        ```
        *Expected Output: `Result: True Positive`, `Reason: Alert popup detected.`*

    * **False Positive:**
        ```bash
        python validator.py --type xss --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "<script>alert('xss')</script>"
        ```
        *Expected Output: `Result: False Positive`, `Reason: No alert popup and payload not in source.`*

---
### 2. Open Redirect ↪️
* **How It Works:** The validator sends a request to the target URL with a payload pointing to an external domain. It specifically inspects the `Location` response header to see if the server attempts to redirect the user.
* **Theoretical Justification:** Proper validation requires checking the server's redirect instruction without actually following it. By disabling automatic redirects and inspecting the `Location` header, the validator can reliably confirm if the application can be abused to redirect users to malicious sites, which is the core of the vulnerability.
* **Test Cases:**
    * **True Positive:**
        ```bash
        python validator.py --type open_redirect --url "[http://testphp.vulnweb.com/login.php?from=](http://testphp.vulnweb.com/login.php?from=)" --payload "[https://www.google.com](https://www.google.com)"
        ```
        *Expected Output: `Result: True Positive`, `Reason: Redirected to https://www.google.com`*

    * **False Positive:**
        ```bash
        python validator.py --type open_redirect --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "[https://www.evil.com](https://www.evil.com)"
        ```
        *Expected Output: `Result: False Positive`, `Reason: No redirect detected.`*

---
### 3. SQL Injection (SQLi) 💿
* **How It Works:** The validator probes for vulnerabilities using two distinct methods: error-based (injecting a single quote) and time-based (injecting a sleep/delay command).
* **Theoretical Justification:** Validation relies on **differential analysis**—observing how the application's response changes to different inputs. Leaked database errors from a syntax-breaking character are direct proof of an injection point. For "blind" cases where no errors are shown, forcing a time delay and measuring the response time is a highly reliable method to confirm that the database is executing the injected commands.
* **Test Cases:**
    * **True Positive (Error-Based):**
        ```bash
        python validator.py --type sqli --url "[http://testphp.vulnweb.com/listproducts.php?cat=](http://testphp.vulnweb.com/listproducts.php?cat=)" --payload "1"
        ```
        *Expected Output: `Result: True Positive`, `Reason: Error-based SQLi detected.`*

    * **True Positive (Time-Based):**
        ```bash
        python validator.py --type sqli --url "[http://vulnerable-app.com/items?id=](http://vulnerable-app.com/items?id=)" --payload "1; WAITFOR DELAY '0:0:5'--"
        ```
        *Expected Output: `Result: True Positive`, `Reason: Time-based SQLi detected.`*

---
### 4. Remote Code Execution (RCE) / File Read 💻
* **How It Works:** The validator injects payloads designed to either run a system command (like `id`) or read a common sensitive file (like `/etc/passwd`). It then scans the server's response for the expected output.
* **Theoretical Justification:** This method provides direct, undeniable proof of a vulnerability. Capturing the output of an OS command (e.g., `uid=0(root)`) or the content of a system file (e.g., `root:x:0:0`) confirms that the application is a bridge to executing commands or reading files on the underlying server.
* **Test Cases:**
    * **True Positive (Command Injection):**
        ```bash
        python validator.py --type rce --url "[http://testphp.vulnweb.com/showimage.php?file=](http://testphp.vulnweb.com/showimage.php?file=)" --payload "| id"
        ```
        *Expected Output: `Result: True Positive`, `Reason: RCE/File read detected.`*

    * **True Positive (File Read):**
        ```bash
        python validator.py --type rce --url "[http://vulnerable-app.com/view?page=](http://vulnerable-app.com/view?page=)" --payload "/etc/passwd"
        ```
        *Expected Output: `Result: True Positive`, `Reason: RCE/File read detected.`*

---
### 5. Server-Side Request Forgery (SSRF) 🌐
* **How It Works:** The validator injects a URL that points to an internal-only service (like `localhost` or a cloud metadata endpoint) and checks if the response contains content from that internal service.
* **Theoretical Justification:** If the application can be made to issue a request to an internal IP and return its contents, it confirms the server can be used as a proxy to pivot into an internal network. The validation proves this by successfully fetching content that should not be publicly accessible.
* **Test Cases:**
    * **True Positive (Localhost):**
        ```bash
        python validator.py --type ssrf --url "[https://vulnerable-app.com/proxy?url=](https://vulnerable-app.com/proxy?url=)" --payload "http://localhost/server-status"
        ```
        *Expected Output: `Result: True Positive`, `Reason: SSRF detected.`*

    * **True Positive (Cloud Metadata):**
        ```bash
        python validator.py --type ssrf --url "[https://vulnerable-app.com/proxy?url=](https://vulnerable-app.com/proxy?url=)" --payload "[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)"
        ```
        *Expected Output: `Result: True Positive`, `Reason: SSRF detected.`*

---
## Handling Advanced Use Cases 🛠️

This validator was built to be reliable across different environments.

* **JS Execution for XSS:** As detailed above, the use of a **headless browser** is central to the XSS validator's reliability, ensuring it validates actual script execution, not just reflection.
* **Authenticated Endpoints:** The validator can work with endpoints that require authentication. Use the `--headers` flag to provide session cookies, JWT/Bearer tokens, or API keys. This allows the tool to maintain an authenticated state while testing protected application areas.
    ```bash
    python validator.py --type rce --url "[https://api.myapp.com/v1/tools?cmd=](https://api.myapp.com/v1/tools?cmd=)" --payload "whoami" --headers '{"Authorization": "Bearer eyJhbG...","X-API-Version": "2"}'
    ```
* **POST Requests:** The tool can test for vulnerabilities in POST request bodies using the `--method POST` and `--data` flags, making it versatile for testing forms and APIs.

---
## AI Assistance 🤖

This project and its documentation were developed with assistance from AI. Key prompts used include:

* "Generate a Python class for a generic XSS validator using Selenium that accepts custom URLs, payloads, and headers."
* "Provide the theoretical justification for using differential analysis (time-based and error-based) to validate SQL injection."
* "Create a professional README.md for a Python security tool, including sections for installation, usage, and test cases for common web vulnerabilities."
* "Write a Python script using argparse to create a CLI for a modular security validation tool."
