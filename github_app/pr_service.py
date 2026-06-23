import requests

def get_pr_files(owner, repo, pull_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url, headers=headers)
    print(f"GitHub API Status: {response.status_code}")
    return response.json()