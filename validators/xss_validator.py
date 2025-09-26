from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib.parse import quote

class XSSValidator:
    def __init__(self, url, payload, method='GET', data=None, headers=None):
        self.url = url
        self.payload = payload
        self.method = method
        self.data = data or {}
        self.headers = headers or {}

    def validate(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            if self.method == 'GET':
                encoded_payload = quote(self.payload)
                full_url = f"{self.url}{encoded_payload}"
                driver.get(full_url)
            else: # POST
                # This block was likely empty, causing the IndentationError.
                # The original logic is restored here.
                driver.get(self.url)
                script = f"""
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '{self.url}';
                const data = {self.data};
                for (const key in data) {{
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = data[key].replace('{self.payload}', '{self.payload}');
                    form.appendChild(input);
                }}
                document.body.appendChild(form);
                form.submit();
                """
                driver.execute_script(script.replace(self.payload,self.payload))

            # This part checks for the alert or payload reflection
            try:
                alert = driver.switch_to.alert
                alert.accept()
                return {"vulnerable": True, "reason": "Alert popup detected."}
            except Exception:
                # No alert found, check for the payload in the source
                if self.payload in driver.page_source:
                     return {"vulnerable": True, "reason": "Payload found in page source."}
                return {"vulnerable": False, "reason": "No alert popup and payload not in source."}

        except UnexpectedAlertPresentException:
            return {"vulnerable": True, "reason": "Alert popup detected."}
        except Exception as e:
            return {"vulnerable": False, "reason": f"An error occurred: {e}"}
        finally:
            driver.quit()