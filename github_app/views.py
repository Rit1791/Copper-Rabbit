import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
                "Title:",
                payload["pull_request"]["title"]
            )
            print(
                "Installation ID:",
                payload["installation"]["id"]
            )
            print("==============================\n")
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