import requests


def post_comment(owner, repo, pull_number, token, comment_body):
    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/issues/{pull_number}/comments"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    payload = {
        "body": comment_body
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("\nCOMMENT API STATUS:", response.status_code)

    try:
        print(response.json())
    except:
        print(response.text)

    return response