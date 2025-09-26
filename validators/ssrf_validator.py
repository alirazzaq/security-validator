import requests

class SSRFValidator:
    def __init__(self, url, payload, method='GET', data=None, headers=None):
        self.url = url
        self.payload = payload
        self.method = method
        self.data = data or {}
        self.headers = headers or {}

    def validate(self):
        try:
            if self.method == 'GET':
                response = requests.get(f"{self.url}{self.payload}", headers=self.headers, verify=False)
            else: # POST
                post_data = self.data.copy()
                for key, value in post_data.items():
                    if 'PAYLOAD' in value:
                        post_data[key] = value.replace('PAYLOAD', self.payload)
                response = requests.post(self.url, headers=self.headers, data=post_data, verify=False)

            # Check for common indicators of SSRF
            if "localhost" in response.text or "127.0.0.1" in response.text or "metadata" in response.text.lower():
                return {"vulnerable": True, "reason": "SSRF detected."}
            else:
                return {"vulnerable": False, "reason": "No SSRF detected."}
        except requests.exceptions.RequestException as e:
            return {"vulnerable": False, "reason": f"An error occurred: {e}"}