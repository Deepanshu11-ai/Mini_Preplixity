# simple in-memory storage

chat_history = []

def add_to_memory(user_query, response):
    chat_history.append({
        "user": user_query,
        "assistant": response
    })

def get_memory():
    history_text = ""
    for chat in chat_history[-5:]:  # last 5 chats only
        history_text += f"User: {chat['user']}\n"
        history_text += f"Assistant: {chat['assistant']}\n\n"
    return history_text