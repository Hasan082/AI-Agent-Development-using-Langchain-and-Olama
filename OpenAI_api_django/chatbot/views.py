import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChatMessage
import requests

OLLAMA_URL = settings.OLLAMA_URL
OLLAMA_MODEL = settings.OLLAMA_MODEL


def home(request):
    chat_message = ChatMessage.objects.all()
    context = {"chat_message": chat_message}
    return render(request, "index.html", context)


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            
            if not user_message.strip():
                return JsonResponse({"error": "Empty Message"}, status=400)
            
            payload = {
                'model': OLLAMA_MODEL,
                'prompt': user_message,
                'stream': False
            }
            
            # Call API
            response = requests.post(OLLAMA_URL, json=payload)
            ollama_data = response.json()
            
            answer = ollama_data.get("response") # If response not found , return next line
            if not answer:
                answer = "Sorry, I couldn’t generate a response. Please try again."           
            return JsonResponse({"answer": answer})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=400)
