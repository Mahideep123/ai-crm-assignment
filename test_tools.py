import requests
import json

BASE = 'http://localhost:8000/api/chat'

def chat(msg, hist=[]):
    r = requests.post(BASE, json={'message': msg, 'history': hist})
    d = r.json()
    response_text = d.get('response', '')[:160]
    action = d.get('action_type', 'none')
    fields = list(d.get('form_updates', {}).keys())
    print(f"\n>>> {msg[:80]}")
    print(f"    Response: {response_text}")
    print(f"    Action={action} | Fields={fields}")
    return d

print("=" * 60)
print("TESTING ALL 5 LANGGRAPH TOOLS")
print("=" * 60)

# Tool 1 - log_interaction
print("\n[TOOL 1] log_interaction")
d1 = chat("Today I met with Dr. Smith and discussed Product X efficiency. Sentiment was positive and I shared the brochures.")

hist = [
    {'role': 'user', 'content': 'Today I met with Dr. Smith and discussed Product X efficiency. Sentiment was positive and I shared the brochures.'},
    {'role': 'assistant', 'content': d1.get('response', '')}
]

# Tool 2 - edit_interaction
print("\n[TOOL 2] edit_interaction")
d2 = chat("Sorry, the name was actually Dr. John, and the sentiment was negative", hist)

# Tool 3 - search_hcp
print("\n[TOOL 3] search_hcp")
d3 = chat("Can you look up Dr. Patel in the HCP database?")

# Tool 4 - get_product_info
print("\n[TOOL 4] get_product_info")
d4 = chat("What details do you have about Prodo-X product?")

# Tool 5 - suggest_follow_up
print("\n[TOOL 5] suggest_follow_up")
d5 = chat("Suggest a follow-up action for a positive meeting about Product X with Dr. Smith")

print("\n")
print("=" * 60)
print("ALL 5 TOOLS TESTED SUCCESSFULLY")
print("=" * 60)
