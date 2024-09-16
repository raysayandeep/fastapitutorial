import requests
import json
import redis
#health check
def health_check():
    health = requests.get('http://localhost:8000/health')
    print(health.status_code)
    print(health.headers)
    print(health.content.decode(encoding='utf-8'))

#get login session
def get_token():
    login_url = 'http://127.0.0.1:8000/auth/token'
    USER_NAME = 'sayan'
    PASSWORD = 'sdr12345'
    login_header = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    login_data = {
    'grant_type': 'password',
    'username': USER_NAME,
    'password': PASSWORD
    }
    response = requests.post(login_url,headers=login_header,data=login_data)
    if response.status_code == 200:
        login = json.loads(response.text)
        auth = f'{login['token_type']} {login['access_token']}'
        print(auth)
        return auth
    else:
        return response.status_code

def get_todos(auth):
    #read all todo
    url = 'http://127.0.0.1:8000/todo/'
    header = {
        'Authorization': auth
    }
    data = requests.get(url,headers=header)
    print(data.text)

if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    auth_token = r.get('auth')
    if not auth_token:
        auth = get_token()
        r.set('auth',auth)
    #print(auth)
    #auth = 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYXlhbiIsImlkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MjYzOTE3NzR9.5VCHtTg89OD-BEmW4OGP6z-aNsVQiynS_kUopQIgL3g'
    print(auth_token)
    get_todos(auth_token)