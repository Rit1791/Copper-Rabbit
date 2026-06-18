from github_app.auth import generate_app_jwt

token = generate_app_jwt()

print(token[:50])
print("JWT Generated Successfully")
