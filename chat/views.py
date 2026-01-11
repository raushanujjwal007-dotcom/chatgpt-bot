import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Use your real API key here
OPENROUTER_API_KEY ='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'

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # Must be Bearer + API key
            "Content-Type": "application/json",
            "Referer": "http://localhost:8000",
            "X-Title": "Django Chatbot"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        # Debug: check status code and response
        print("STATUS CODE:", response.status_code)
        try:
            result = response.json()
            print("OPENROUTER RESPONSE:", result)
        except Exception as e:
            print("JSON ERROR:", e)
            return JsonResponse({"error": "Invalid response from OpenRouter"}, status=500)

        # Check if 'choices' is present
        if "choices" not in result:
            return JsonResponse({"error": result}, status=500)

        ai_message = result["choices"][0]["message"]["content"]

        return JsonResponse({"message": ai_message})

    return render(request, "chat/chat.html")
