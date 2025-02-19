import os
import streamlit as st
from openai import OpenAI
import time

# Page configuration
st.set_page_config(
    page_title="Grok Q&A Assistant",
    page_icon="🤖",
    layout="wide"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_client():
    return OpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1"
    )

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        # Determine CSS class based on role
        css_class = "user-message" if role == "user" else "assistant-message"
        display_name = "You" if role == "user" else "Assistant"
        
        # Display message with styling
        st.markdown(
            f"""
            <div class="chat-message {css_class}">
                <div class="message-header">{display_name}</div>
                <div>{content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def generate_response(prompt):
    try:
        client = get_client()
        messages = [
            {"role": "system", "content": "You are a helpful and knowledgeable assistant. Provide clear, accurate, and engaging responses."},
            {"role": "user", "content": prompt}
        ]
        
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="grok-2-1212",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("🤖 Grok Q&A Assistant")
    st.markdown("""
    Welcome to the Grok Q&A Assistant! Ask any question and get intelligent responses powered by Grok AI.
    """)
    
    # Display chat history
    display_chat_history()
    
    # Input field for user question
    user_input = st.text_area("Ask your question here:", key="user_input", height=100)
    
    # Submit button
    if st.button("Send", key="submit"):
        if user_input.strip():
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Generate response
            response = generate_response(user_input)
            
            if response:
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            # Clear input field (by forcing a rerun)
            st.experimental_rerun()
        else:
            st.warning("Please enter a question.")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("Powered by Grok AI 🚀")

if __name__ == "__main__":
    main()
