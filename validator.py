import argparse
import json
from validators.xss_validator import XSSValidator
from validators.open_redirect_validator import OpenRedirectValidator
from validators.sql_injection_validator import SQLInjectionValidator
from validators.rce_validator import RCEValidator
from validators.ssrf_validator import SSRFValidator

def main():
    parser = argparse.ArgumentParser(description="Security Validator Toolkit")
    parser.add_argument('--type', required=True, choices=['xss', 'open_redirect', 'sqli', 'rce', 'ssrf'], help='Type of vulnerability to validate')
    parser.add_argument('--url', required=True, help='Target URL')
    parser.add_argument('--payload', required=True, help='Payload to test')
    parser.add_argument('--method', default='GET', choices=['GET', 'POST'], help='HTTP method to use')
    parser.add_argument('--data', help='Data for POST requests (e.g., key=value&key2=value2)')
    parser.add_argument('--headers', help='Headers in JSON format (e.g., \'{"Authorization": "Bearer token"}\')')
    parser.add_argument('--output', default='text', choices=['text', 'json'], help='Output format')

    args = parser.parse_args()

    headers = json.loads(args.headers) if args.headers else {}
    data = dict(item.split('=') for item in args.data.split('&')) if args.data else {}

    validator = None
    if args.type == 'xss':
        validator = XSSValidator(args.url, args.payload, method=args.method, data=data, headers=headers)
    elif args.type == 'open_redirect':
        validator = OpenRedirectValidator(args.url, args.payload, method=args.method, data=data, headers=headers)
    elif args.type == 'sqli':
        validator = SQLInjectionValidator(args.url, args.payload, method=args.method, data=data, headers=headers)
    elif args.type == 'rce':
        validator = RCEValidator(args.url, args.payload, method=args.method, data=data, headers=headers)
    elif args.type == 'ssrf':
        validator = SSRFValidator(args.url, args.payload, method=args.method, data=data, headers=headers)

    if validator:
        result = validator.validate()
        if args.output == 'json':
            print(json.dumps(result, indent=4))
        else:
            print(f"Vulnerability: {args.type.upper()}")
            print(f"Target: {args.url}")
            print(f"Payload: {args.payload}")
            print(f"Result: {'True Positive' if result['vulnerable'] else 'False Positive'}")
            print(f"Reason: {result['reason']}")

if __name__ == '__main__':
    main()