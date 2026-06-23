import json
from github_app.pr_service import get_pr_files
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from github_app.github_client import get_installation_token
from services.gemini_service import review_pr
from github_app.comment_service import post_comment


@csrf_exempt
def github_webhook(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests allowed"},
            status=405
        )

    try:
        payload = json.loads(request.body)
        event = request.headers.get("X-GitHub-Event")
        print(f"\nEVENT TYPE: {event}")

        if event == "pull_request":
            print("\n===== PULL REQUEST EVENT =====")

            print("Action:", payload.get("action"))

            print(
                "Repository:",
                payload["repository"]["full_name"]
            )
            print(
                "PR Number:",
                payload["pull_request"]["number"]
            )
            print(
                "Title:",
                payload["pull_request"]["title"]
            )
            print(
                "Installation ID:",
                payload["installation"]["id"]
            )
            print("==============================\n")
            owner = payload["repository"]["owner"]["login"]
            repo = payload["repository"]["name"]
            installation_id = payload["installation"]["id"]
            token_data = get_installation_token(installation_id)
            token = token_data["token"]
            pull_number = payload["pull_request"]["number"]
            print("Owner:", owner)
            print("Repo:", repo)
            print("Installation ID Variable:", installation_id)
            print("Token Retrieved Successfully")
            files = get_pr_files(
                owner,
                repo,
                pull_number,
                token
            )
            print("Token Retrieved Successfully")
            print(f"\nTotal Files Changed: {len(files)}")
            review_data = []
            for file in files:
                print("\nFILE:", file["filename"])

                print(
                    "PATCH:",
                    file.get("patch", "No patch available")
                )
                review_data.append({
                    "filename": file["filename"],
                    "patch": file.get("patch", "")
                })
            print("\nREVIEW DATA SUMMARY")

            for item in review_data:
                print(item["filename"])
            print(f"\nReview Data Entries: {len(review_data)}")
            prompt = """
You are an expert senior software engineer.

Review the following pull request diff.

Identify:
1. Bugs
2. Security issues
3. Performance issues
4. Code quality improvements

Provide concise actionable feedback.

PR DIFF:
"""
            review_text = ""
            for item in review_data:
                review_text += f"\nFILE: {item['filename']}\n"
                review_text += f"{item['patch']}\n"
            final_prompt = prompt + review_text
            print("\nGENERATING GEMINI REVIEW...")
            review = review_pr(final_prompt)
            post_comment(
                owner,
                repo,
                pull_number,
                token,
                review[:5000]
            )

            print(f"\nREVIEW GENERATED ({len(review)} characters)")
            print("\nGEMINI REVIEW GENERATED SUCCESSFULLY")
            print(f"Review Length: {len(review)}")
            # print(f"\nReview Text Length: {len(review_text)}")
            # print("\nREVIEW TEXT PREVIEW")
            # print(review_text[:500])
            # print(f"\nFinal Prompt Length: {len(final_prompt)}")
            # print("\nPROMPT PREVIEW")
            # print(final_prompt[:300])
        else:
            print("\n===== GITHUB WEBHOOK RECEIVED =====")
            print(payload)
            print("===================================\n")

        return JsonResponse({"status": "success"})

    except Exception as e:
        print(f"Webhook Error: {e}")

        return JsonResponse(
            {"error": str(e)},
            status=400
        )
