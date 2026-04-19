with open('/home/julio/Codigos/Codigo-6X2/app/src/pages/supabase.py', 'r') as f:
    content = f.read()

content = content.replace('import requests', "import requests\nimport urllib3\nurllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)")

content = content.replace('timeout=1000', 'timeout=1000,\n            verify=False')

with open('/home/julio/Codigos/Codigo-6X2/app/src/pages/supabase.py', 'w') as f:
    f.write(content)
