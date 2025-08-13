import openai
from openai import OpenAI
import numpy as np
from django.conf import settings
from ..models import Product, ChatMessage

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_embedding(text):
    resp = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return resp.data[0].embedding

def find_relevant_context(user_query, top_k=3):
    query_embedding = generate_embedding(user_query)
    # pgvector similarity search
    products = Product.objects.order_by(
        (Product.embedding.cosine_distance(query_embedding))
    )[:top_k]
    context = "\n".join([f"{p.name}: {p.description}" for p in products])
    return context

def chat_with_context(user_id, user_message):
    context = find_relevant_context(user_message)
    prompt = f"""
    You are a chatbot for our store. 
    Only answer using the context below. 
    If the question is unrelated, reply: "I can only answer questions about our products."

    Context:
    {context}

    User: {user_message}
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.2
    )

    answer = resp.choices[0].message.content

    # Save chat messages
    ChatMessage.objects.create(user_id=user_id, message=user_message, is_bot=False)
    ChatMessage.objects.create(user_id=user_id, message=answer, is_bot=True)

    return answer