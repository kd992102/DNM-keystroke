import json

with open("credentials.json", "r", encoding="utf-8") as f:
    creds = json.load(f)

toml_ready = json.dumps(creds).replace("\\", "\\\\").replace("\"", "\\\"")
print(f'GOOGLE_SHEET_CREDENTIALS = """{toml_ready}"""')
