import streamlit as st
from agent import respond

# Define a function to format the response as a chat bubble
def format_as_chat_bubble(response):
    return f'<div style="margin: 10px; padding: 10px; border-radius: 15px; border: 1px solid #ccc; background-color: #008000;">{response}</div>'

# application to host a group chat between the user and multiple agents
st.title("Group Chat Demo")

# get user input
user_input = st.text_input("User Input", "")

response = respond(user_input)

# display the response
st.write("Length of response:",len(response.items()))
#st.write("Response:",response)
         
for i, (agent, response) in enumerate(response.items()):
    if i <= 2:
        continue  # Skip the first item
    
    # convert agent from str to list
    agent = eval(agent)
    # agent_name = agent[2]["name"]
    st.write("Agent:",agent)
    # st.write("Response:",response)
    # st.write("Agent Name:",agent_name)
    st.markdown(format_as_chat_bubble(agent[2]['content']), unsafe_allow_html=True)
    