import streamlit as st
from csvquery import query
# Function to display user messages with rounded rectangle borders
def user_message(message):
    st.markdown(f'<div class="user-message" style="display: flex; justify-content: flex-end; padding: 5px;">'
                f'<div style="background-color: #f0e2ce; color: black; padding: 10px; border-radius: 10px; font-size:18px; margin-bottom:10px; margin-left:20px;">{message}</div>'
                f'</div>', unsafe_allow_html=True)

# Function to display bot messages with rounded rectangle borders
def bot_message(message):
    st.markdown(f'<div class="bot-message" style="display: flex; padding: 5px;">'
                f'<div style="background-color: #D3D3D3; color: black; padding: 10px; border-radius: 10px; font-size:18px; margin-bottom:10px; margin-right:20px;">{message}</div>'
                f'</div>', unsafe_allow_html=True)
    

# Function to get the bot response based on selected model
def get_bot_response(model, user_input):
    if model == "gemma-7b-it":
        return query(user_input, model="gemma-7b-it").replace("\n", "<br>")
    elif model == "mixtral-8x7b-32768":
        return query(user_input, model="mixtral-8x7b-32768").replace("\n", "<br>")
    elif model == "llama3-70b-8192":
        return query(user_input, model="llama3-70b-8192").replace("\n", "<br>")
    elif model == "llama3-8b-8192":
        return query(user_input, model="llama3-8b-8192").replace("\n", "<br>")
    # elif model == "gpt-3.5-turbo":
    #     return query(user_input, model="gpt-3.5-turbo").replace("\n", "<br>")
    else:
        return "Model not recognized."

# Define the main Streamlit app
def main(i):
    # Dropdown to select the model
    model = st.selectbox("Select Model", ["llama3-8b-8192","llama3-70b-8192","gemma-7b-it", "mixtral-8x7b-32768"])

    st.title("Financial ChatBot")

    # Initialize chat history using session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input field for user to enter a message
    user_input = st.chat_input("Your Message:")
    # Button to send the user's message
    if user_input:
        # Display previous chat messages
        for message, is_bot_response in st.session_state.chat_history:
            if is_bot_response:
                bot_message(message)
            else:
                user_message(message)
        # Add the user's message to the chat history
        st.session_state.chat_history.append((user_input, False))

        # Display the user's message
        user_message(user_input)

        # Bot's static response (you can replace this with a dynamic response generator)
        # bot_response = query(user_input).replace("\n", "<br>")

        # # Get the bot response based on selected model
        bot_response = get_bot_response(model, user_input)

        # Add the bot's response to the chat history
        st.session_state.chat_history.append((bot_response, True))
        
        # Display the bot's response
        bot_message(bot_response)
    
# Run the app
if __name__ == "__main__":
    main(0)

