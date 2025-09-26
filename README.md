# Security Validator Toolkit 🛡️

A generic and configurable Python-based toolkit for deterministically validating web security findings.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features-)
- [Installation](#installation-)
- [Usage](#usage-)
  - [Command-Line Arguments](#command-line-arguments)
- [Validator Deep Dive & Payloads](#validator-deep-dive--payloads)
  - [Cross-Site Scripting (XSS)](#1-cross-site-scripting-xss-)
  - [Open Redirect](#2-open-redirect-️)
  - [SQL Injection (SQLi)](#3-sql-injection-sqli-)
  - [Remote Code Execution (RCE) / File Read](#4-remote-code-execution-rce--file-read-)
  - [Server-Side Request Forgery (SSRF)](#5-server-side-request-forgery-ssrf-)
- [Advanced Usage](#advanced-usage-)
  - [Testing with POST Requests](#testing-with-post-requests)
  - [Testing Authenticated Endpoints](#testing-authenticated-endpoints)
- [Contributing](#contributing-)
- [License](#license-)
- [Disclaimer](#disclaimer-️)

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
- **ChromeDriver**: Download the version that matches your Chrome browser [here](https://chromedriver.chromium.org/downloads). Ensure the executable is in your system's `PATH`.

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


### Command-Line Arguments

| Argument    | Description                                                                                             | Required |
|-------------|---------------------------------------------------------------------------------------------------------|----------|
| `--type`    | Vulnerability to validate: `xss`, `open_redirect`, `sqli`, `rce`, `ssrf`.                               | **Yes** |
| `--url`     | The full target URL, ending at the injection point (e.g., `.../page?param=`).                             | **Yes** |
| `--payload` | The vulnerability payload to test.                                                                      | **Yes** |
| `--method`  | HTTP method to use (`GET` or `POST`). Default is `GET`.                                                 | No       |
| `--data`    | Request body for `POST`. Use `PAYLOAD` as a placeholder (e.g., `comment=PAYLOAD`).                        | No       |
| `--headers` | JSON-formatted string of HTTP headers (e.g., `'{"Authorization": "Bearer ..."}'`).                       | No       |
| `--output`  | Output format (`text` or `json`). Default is `text`.                                                    | No       |

---

## Validator Deep Dive & Payloads

### 1. Cross-Site Scripting (XSS) 💉
* **How It Works:** Uses a headless Chrome browser to visit the target URL. It confirms a vulnerability if a JavaScript `alert()` box is triggered or if the payload is reflected in the page's HTML.
* **True Positive Example:**
    ```bash
    python validator.py --type xss --url "[http://testphp.vulnweb.com/listproducts.php?cat=](http://testphp.vulnweb.com/listproducts.php?cat=)" --payload "<script>alert('xss')</script>"
    ```
* **False Positive Example:**
    ```bash
    python validator.py --type xss --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "<script>alert('xss')</script>"
    ```

---

### 2. Open Redirect ↪️
* **How It Works:** Sends a request with a payload pointing to an external domain and inspects the `Location` response header to confirm a redirect instruction.
* **True Positive Example:**
    ```bash
    python validator.py --type open_redirect --url "[http://testphp.vulnweb.com/login.php?from=](http://testphp.vulnweb.com/login.php?from=)" --payload "[https://www.google.com](https://www.google.com)"
    ```
* **False Positive Example:**
    ```bash
    python validator.py --type open_redirect --url "[https://google.com/search?q=](https://google.com/search?q=)" --payload "[https://www.evil.com](https://www.evil.com)"
    ```

---

### 3. SQL Injection (SQLi) 💿
* **How It Works:** Probes for vulnerabilities using error-based (`'`) and time-based (`WAITFOR DELAY`) techniques.
* **True Positive (Error-Based) Example:**
    ```bash
    python validator.py --type sqli --url "[http://testphp.vulnweb.com/listproducts.php?cat=](http://testphp.vulnweb.com/listproducts.php?cat=)" --payload "1"
    ```
* **True Positive (Time-Based) Example:**
    ```bash
    python validator.py --type sqli --url "[http://vulnerable-app.com/items?id=](http://vulnerable-app.com/items?id=)" --payload "1; WAITFOR DELAY '0:0:5'--"
    ```

---

### 4. Remote Code Execution (RCE) / File Read 💻
* **How It Works:** Injects payloads to run system commands (`id`) or read sensitive files (`/etc/passwd`) and checks the response for expected output.
* **True Positive (Command Injection) Example:**
    ```bash
    python validator.py --type rce --url "[http://testphp.vulnweb.com/showimage.php?file=](http://testphp.vulnweb.com/showimage.php?file=)" --payload "| id"
    ```
* **True Positive (File Read) Example:**
    ```bash
    python validator.py --type rce --url "[http://vulnerable-app.com/view?page=](http://vulnerable-app.com/view?page=)" --payload "/etc/passwd"
    ```

---

### 5. Server-Side Request Forgery (SSRF) 🌐
* **How It Works:** Injects a URL pointing to an internal service (`localhost`, `169.254.169.254`) and checks the response for internal content.
* **True Positive (Localhost) Example:**
    ```bash
    python validator.py --type ssrf --url "[https://vulnerable-app.com/proxy?url=](https://vulnerable-app.com/proxy?url=)" --payload "http://localhost/server-status"
    ```
* **True Positive (Cloud Metadata) Example:**
    ```bash
    python validator.py --type ssrf --url "[https://vulnerable-app.com/proxy?url=](https://vulnerable-app.com/proxy?url=)" --payload "[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)"
    ```

---

## Advanced Usage 🛠️

### Testing with POST Requests
Use `--method POST` and `--data`. The string `PAYLOAD` is replaced with your payload at runtime.
```bash
python validator.py --type xss --method POST --url "[https://vulnerable-app.com/comment](https://vulnerable-app.com/comment)" --data "username=guest&comment=PAYLOAD" --payload "<h1>XSS</h1>"

```bash
python validator.py --type <type> --url <target_url> --payload "<payload>" [options]
