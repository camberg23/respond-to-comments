import streamlit as st
from openai import OpenAI

# Set your API key here
api_key = st.secrets['API_KEY']
client = OpenAI(api_key=api_key)

def get_article_text():
    with open('markdown.txt', 'r', encoding='utf-8') as file:
        return file.read()

full_text = get_article_text()

def generate_response(comment):
    """
    Generate a response using GPT-4 with the given comment and article text.
    """
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Article Text: {full_text}\n\n"
                    "Your task is to analyze a user's comment in the context of the article text. "
                    "Generate a response that includes:\n"
                    "1. Distillation: A comprehensive, helpful, and accurate distillation of ALL of the key content of the comment, presenting it as clearly and charitably ('steelmanned') as possible.\n"
                    "2. Sanity check: A sanity check on the comment, evaluating the degree to which this is a good, reasonable, fair comment given your knowledge of the text.\n"
                    "3. Key response points: Key points that should be addressed in response to the comment given your knowledge of the text. IT IS CRITICAL TO USE SPECIFIC INFORMATION FROM THE PIECE IN THE RESPONSE\n"
                    "4. Comment response draft: Draft an actual comment response in a rationalist, LessWrong-style writing given your knowledge of the text/world. Do not overdo this, the key idea here is to be epistemically humble, not flowery or needlessly polite at all, SUCCINCT, highly substantive and concrete, technical, and precise. THIS SHOULD INTEGRATE HIGHLY CONCRETE, OBJECT-LEVEL INSIGHTS FROM 3.\n\n"
                    "Format this full response in Markdown (one labeled bold header exactly as they appear above for each of the requirements above, then normal text/bullets as necessary under each header) for direct nice professional rendering in Streamlit."
                    "PLEASE NOTE: the output is for helping the authors of the piece respond to the comment, not a direct response to the comment, please structure your outputs accordingly."
                )
            },
            {"role": "user", "content": comment}
        ]
    )
    return completion.choices[0].message.content

# Streamlit UI
st.title('LW post: streamlined comment analysis and response tool')

comment = st.text_area("Enter the user's comment:", height=150)

if st.button('Analyze Comment'):
    with st.spinner('Generating response...this will take ~20 seconds'):
        response = generate_response(comment)
        st.markdown(response)