import streamlit as st
from database import save_to_db, get_history
import requests  # Ensure you have requests installed

# Streamlit UI components
st.title("AI Content Writer")

# Define the inputs
prompt = st.text_area("Enter your prompt:")
tone = st.selectbox("Choose a tone for the content:", ["Formal", "Casual", "Persuasive", "Informative"])
max_length = st.slider("Max Length of the Generated Content", min_value=100, max_value=1000, value=500)

if st.button("Generate Content"):
    if prompt:  # Check if the prompt is not empty
        with st.spinner("Generating content..."):
            # Adjust prompt based on tone
            tone_prefix = ""
            if tone == "Formal":
                tone_prefix = "Write a formal article: "
            elif tone == "Casual":
                tone_prefix = "Write in a casual tone: "
            elif tone == "Persuasive":
                tone_prefix = "Write a persuasive piece: "
            else:
                tone_prefix = "Write an informative piece: "

            # Define final_prompt here
            final_prompt = tone_prefix + prompt

            # Set up the API key and headers
            api_key = "hf_THMRQksToIXRESsVKWOMYHXMlioHByGsTxecho "# AI-Content-Generator" >> README.md
  # Ensure this is in quotes
            headers = {
                "Authorization": f"Bearer {api_key}",  # Correct format
                "Content-Type": "application/json",
            }

            # Call the Together AI API
            response = requests.post(
                "https://api.together.xyz/v1/generate",  # Ensure this is the correct endpoint
                headers=headers,
                json={
                    "model": "llama2",  # Specify the model you want to use
                    "prompt": final_prompt,
                    "max_length": max_length,
                    "temperature": 0.7,  # Adjust based on your needs
                }
            )

            # Get the generated text from the response
            if response.status_code == 200:
                generated_text = response.json().get('text', '').strip()  # Use .get to safely extract 'text'

                # Display the generated content
                st.write(generated_text)

                # Save the prompt, tone, and content to the database
                save_to_db(prompt, tone, generated_text)
            else:
                st.error(f"Error in generating content: {response.status_code}, {response.text}")  # More informative error message

    else:
        st.warning("Please enter a prompt.")

if st.button("View History"):
    st.subheader("Generated Content History")
    history = get_history()

    for row in history:
        st.markdown(f"**Prompt:** {row[0]}")
        st.markdown(f"**Tone:** {row[1]}")
        st.markdown(f"**Content:** {row[2]}")
        st.markdown(f"**Date:** {row[3]}")
        st.markdown("---")
