import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChatMessage, Product
import requests

OLLAMA_URL = settings.OLLAMA_URL
OLLAMA_MODEL = settings.OLLAMA_MODEL


def home(request):
    chat_message = ChatMessage.objects.all()
    product = Product.objects.all()
    print(product)
    context = {"chat_message": chat_message}
    return render(request, "index.html", context)


# Define your strict context
AI_CONTEXT = """
You are a chatbot for our website. 
You MUST ONLY answer questions related to our products, store policies, orders, and user accounts.
If a question is outside this scope, reply: "Sorry, I can only answer questions about our site and products."
Do NOT give any personal opinions or general AI answers.
"""

# Optional: keywords to further filter responses
ALLOWED_KEYWORDS = [
    "product",
    "order",
    "shipping",
    "price",
    "account",
    "web design",
    "Development",
    "Django",
    "django",
    "python",
]


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            user_message = data.get("message", "")

            if not user_message.strip():
                return JsonResponse({"error": "Empty Message"}, status=400)

            # Combine strict context with user message
            prompt = f"{AI_CONTEXT}\nUser: {user_message}\nAssistant:"
            

            payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}

            # Call API
            response = requests.post(OLLAMA_URL, json=payload)

            ollama_data = response.json()

            answer = ollama_data.get(
                "response"
            )  # If response not found , return next line
            if not answer:
                answer = "Sorry, I couldn’t generate a response. Please try again."
                
        
            return JsonResponse({"answer": answer})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=400)
