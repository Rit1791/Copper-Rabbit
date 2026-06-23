import json
from github_app.pr_service import get_pr_files
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from github_app.github_client import get_installation_token
from services.gemini_service import review_pr
from github_app.comment_service import post_comment
import hmac
import hashlib
from reviews.models import Review

from django.conf import settings

@csrf_exempt
def github_webhook(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests allowed"},
            status=405
        )
    signature = request.headers.get("X-Hub-Signature-256")
    #print("Signature Present:", bool(signature))
    if not signature:
        return JsonResponse(
            {"error": "Missing signature"},
            status=401
        )
    expected_signature = "sha256=" + hmac.new(
    settings.GITHUB_WEBHOOK_SECRET.encode(),
    request.body,
    hashlib.sha256
    ).hexdigest()

    # print("Signature Match:", hmac.compare_digest(
    #     signature,
    #     expected_signature
    # ))
    if not hmac.compare_digest(
        signature,
        expected_signature
    ):
        return JsonResponse(
            {"error": "Invalid signature"},
            status=401
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
            print("Token Retrieved Successfully")
            pull_number = payload["pull_request"]["number"]
            
            files = get_pr_files(
                owner,
                repo,
                pull_number,
                token
            )
            print(f"\nTotal Files Changed: {len(files)}")
            review_data = []
            for file in files:
                print("\nFILE:", file["filename"])

                review_data.append({
                    "filename": file["filename"],
                    "patch": file.get("patch", "")
                })

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
            Review.objects.create(
                repository=f"{owner}/{repo}",
                pr_number=pull_number,
                review_text=review
            )
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
