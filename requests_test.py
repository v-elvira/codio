import requests

# put your real credentials here
EMAIL_ADDRESS = "elya_321@mail.ru"
PASSWORD = "pwd"
BASE_URL = "http://localhost:8000/"

anon_post_resp = requests.get(BASE_URL + "api/v1/posts/")
anon_post_resp.raise_for_status()

anon_post_count = anon_post_resp.json()["count"]
print(f"Anon users have {anon_post_count} post{'' if anon_post_count == 1 else 's'}")
# print(anon_post_resp.json())
auth_resp = requests.post(
    BASE_URL + "api/v1/token-auth/",
    json={"username": EMAIL_ADDRESS, "password": PASSWORD},
)
auth_resp.raise_for_status()
token = auth_resp.json()["token"]
# print(token)

# Use the token in a request
authed_post_resp = requests.get(
    BASE_URL + "api/v1/posts/", headers={"Authorization": f"Token {token}"}
)
authed_post_count = authed_post_resp.json()["count"]

print(
    f"Authenticated user has {authed_post_count} post{'' if authed_post_count == 1 else 's'}"
)

# Since requests doesn't remember headers between requests, this next request is unauthenticated again
anon_post_resp = requests.get(BASE_URL + "api/v1/posts/")



#JWT auth:
jwt_auth_resp = requests.post(
    BASE_URL + "api/v1/jwt/",
    json={"email": EMAIL_ADDRESS, "password": PASSWORD},
)
# print(jwt_auth_resp.json())
token = jwt_auth_resp.json()['access']

authed_post_resp = requests.get(
    BASE_URL + "api/v1/posts/", headers={"Authorization": f"JWT {token}"}
)
authed_post_count = authed_post_resp.json()["count"]

print(
    f"Authenticated user has {authed_post_count} post{'' if authed_post_count == 1 else 's'}"
)


# # import json # for data=json.dumps(), not for rest.json()

# # post_data = { "id": 1, "title": "New Title", "body": "Updated Body", "userId": 1}

# # # resp = requests.put("https://jsonplaceholder.typicode.com/posts/1", data=json.dumps(post_data), headers={"Content-Type": "application/json"})
# # resp = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=post_data) #autho convert to json + content-type header

# posts = requests.get("http://127.0.0.1:8000/api/v1/posts/", params={"author": "2", "title": "Ipsum 2"})
# print([(res["slug"], res["title"]) for res in posts.json()['results']])  # ?? (why 3)
# resp = requests.get("http://127.0.0.1:8000/api/v1/posts/", params={"tags": ["1", "3"]})
# print(resp.status_code)
# print(resp.json())
# print(resp.text)
# print(resp.content) #binary
# print(resp.headers)
