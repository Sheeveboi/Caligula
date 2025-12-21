import requests;

headers = {
    'Database' : 'oppwatch',
    'Function' : 'toggle_pos'
}

json = {
    'username' : 'testing'
}

r = requests.get("http://192.168.1.188/functions", headers = headers, json = json);

print(r.headers);
print(r.content);