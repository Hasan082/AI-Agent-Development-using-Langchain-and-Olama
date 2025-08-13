from django.shortcuts import render
import os
from openai import OpenAI


def chatbot(request):

    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, ChatGPT!"}],
    )

    print(response.choices[0].message.content)

    return render(request, "chatbot.html")
