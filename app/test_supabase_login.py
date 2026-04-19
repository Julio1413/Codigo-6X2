import requests

url = "https://ellyuhvkzfwgkyvhktis.supabase.co/rest/v1/login"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsbHl1aHZremZ3Z2t5dmhrdGlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYzMzU5NTYsImV4cCI6MjA4MTkxMTk1Nn0.xTcZbx3fDs_tx_uRVG33yIkzAYLdz_sjTZM87vb5QGE"
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.text)
