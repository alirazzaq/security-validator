# Security Validator Toolkit 🛡️

A generic and configurable Python-based toolkit for deterministically validating web security findings.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

---

### **Disclaimer** ⚠️
This tool is intended for educational purposes and for use by authorized security professionals in controlled environments. Only use it to test systems for which you have explicit, written permission. The developers are not responsible for any misuse or damage caused by this toolkit.

---

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


# Validator README

> A small, reliable CLI validator for common web vulnerabilities: XSS, Open Redirect, SQLi, RCE/File-read, and SSRF.

---

## Table of Contents
- [Command-Line Arguments](#command-line-arguments)
- [Usage Examples](#usage-examples)
- [Validator Deep Dive](#validator-deep-dive)
  - [Cross-Site Scripting (XSS)](#1-cross-site-scripting-xss-)
  - [Open Redirect](#2-open-redirect-)
  - [SQL Injection (SQLi)](#3-sql-injection-sqli-)
  - [Remote Code Execution (RCE) / File Read](#4-remote-code-execution-rce--file-read-)
  - [Server-Side Request Forgery (SSRF)](#5-server-side-request-forgery-ssrf-)
- [Handling Advanced Use Cases](#handling-advanced-use-cases-)
- [Export to Sheets](#export-to-sheets)
- [AI Assistance](#ai-assistance)
- [Contributing](#contributing)
- [License](#license)

---

## Command-Line Arguments

| Argument    | Description                                                                 | Required |
|---|---:|
| `--type`    | Vulnerability to validate: `xss`, `open_redirect`, `sqli`, `rce`, `ssrf`.  | Yes |
| `--url`     | The full target URL, ending at the injection point (e.g., `.../page?param=`). | Yes |
| `--payload` | The vulnerability payload to test.                                         | Yes |
| `--method`  | HTTP method to use (`GET` or `POST`). Default is `GET`.                    | No |
| `--data`    | Request body for POST. Use `PAYLOAD` as placeholder (e.g., `comment=PAYLOAD`). | No |
| `--headers` | JSON-formatted string of HTTP headers (e.g., `{"Authorization":"Bearer ..."}`). | No |
| `--output`  | Output format (`text` or `json`). Default is `text`.                      | No |

---

## Usage Examples

### Basic (GET)
```bash
python validator.py --type xss --url "http://example.com/page?name=" --payload "<script>alert('xss')</script>"

