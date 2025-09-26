import requests

class RCEValidator:
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

            # Check for common indicators of RCE/file read
            if "root:x:0:0" in response.text or "uid=0(root) gid=0(root)" in response.text:
                return {"vulnerable": True, "reason": "RCE/File read detected."}
            else:
                return {"vulnerable": False, "reason": "No RCE/File read detected."}
        except requests.exceptions.RequestException as e:
            return {"vulnerable": False, "reason": f"An error occurred: {e}"}