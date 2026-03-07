from google.genai import types
from sentence_transformers import SentenceTransformer

#  Load model (downloads automatically on first run)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Give chatbot response
def get_chatbot_response(client, model_name, messages):
    input_messages = []
    for message in messages:
        input_messages.append(types.Content(role=message['role'], parts=[types.Part.from_text(text=message['content'])]))
    response = client.models.generate_content(
        model=model_name,
        contents=input_messages,
    #     config = types.GenerateContentConfig(
    #     response_mime_type='application/json',
    #     response_schema=responseFormatType,
    # ),
    ).candidates[0].content.parts[0].text
    finalCleanedResponse = cleaned_response(response)
    return finalCleanedResponse

# Clean the output received from gemini
def cleaned_response(response):
    cleaned = response.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()

    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()
    return cleaned 

# Generate embeddings
def get_embeddings(text_input):
    output = model.encode(text_input).tolist()

    embeddings = []
    for embeddings_object in output:
        embeddings.append(embeddings_object)

    return embeddings


def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role":"user","content":prompt}]
    response = get_chatbot_response(client, model_name, messages)

    return response
    