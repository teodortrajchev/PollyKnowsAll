import os
import json
from openai import OpenAI
import requests

# --------------Пример датабаза-----------------------
# ----------------------------------------------------
# topic: "Tiger"
# statement: "Is it a mammal?"
# answer: "YES"
# embedding: [0.12, -0.55, 0.91, ...]
#
# topic: "Tiger"
# statement: "Can it fly?"
# answer: "NO"
# embedding: [-0.42, 0.88, -0.11, ...]
#
# topic: "France"
# statement: "Is it in Europe?"
# answer: "YES"
# embedding: [0.73, -0.21, 0.33, ...]
#
# topic: "France"
# statement: "Is it a continent?"
# answer: "NO"
# embedding: [-0.14, 0.67, -0.91, ...]
# -------------------------
# 1️⃣ Setup OpenAI Client
# -------------------------
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # replace with your API key

# -------------------------
# 2️⃣ Download Public APIs list
# -------------------------
PUBLIC_APIS_URL = "https://raw.githubusercontent.com/public-apis/public-apis/master/entries.json"

response = requests.get(PUBLIC_APIS_URL)
apis_data = response.json()["entries"]  # list of APIs


# -------------------------
# 3️⃣ Function to generate base questions
# -------------------------
def generate_base_questions(api):
    """
    For each API, generate a few simple yes/no questions
    """
    name = api["API"]
    category = api.get("Category", "General")
    auth = api.get("Auth", "")
    https = api.get("HTTPS", False)

    base_questions = [
        {"topic": name, "question": f"Is the API in the {category} category?", "label": "YES"},
        {"topic": name, "question": f"Does the API require authentication?", "label": "YES" if auth else "NO"},
        {"topic": name, "question": f"Does the API use HTTPS?", "label": "YES" if https else "NO"},
        {"topic": name, "question": f"Is the API free to use?", "label": "YES"},  # assume free unless Auth is mandatory
    ]

    return base_questions


# -------------------------
# 4️⃣ Function to paraphrase using OpenAI
def paraphrase_question(topic, question, n_variations=3):
    prompt = f"""
You are a helpful assistant that rewrites yes/no questions in different ways.
Do not change the meaning.

Original question: "{question}"

Provide {n_variations} paraphrased versions of the question, as a JSON list of strings.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    try:
        paraphrases = json.loads(content)
        return [{"topic": topic, "question": q, "label": None} for q in paraphrases]  # label to fill later
    except Exception:
        # fallback if JSON parsing fails
        return [{"topic": topic, "question": f"{question} (variation)", "label": None}]


# -------------------------
# 5️⃣ Generate full dataset
# -------------------------
dataset = []

for api in apis_data[:50]:  # limit to first 50 APIs for testing
    base_questions = generate_base_questions(api)
    for q in base_questions:
        dataset.append(q)
        # generate paraphrases
        paraphrased = paraphrase_question(q["topic"], q["question"], n_variations=3)
        for p in paraphrased:
            p["label"] = q["label"]  # copy the original label
            dataset.append(p)

# -------------------------
# 6️⃣ Save dataset to JSON
# -------------------------
os.makedirs("dataset", exist_ok=True)
with open("dataset/yes_no_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"Dataset generated with {len(dataset)} entries. Saved to dataset/yes_no_dataset.json")
