
from db import (
    init_db,
    create_conversation,
    get_conversations,
    save_message,
    get_messages
)

init_db()

chat_id = create_conversation("Database Test")

save_message(
    chat_id,
    "user",
    "Explain the OSI Model."
)

save_message(
    chat_id,
    "assistant",
    "The OSI model has seven layers."
)

print("Conversations:")
print(get_conversations())

print("\nMessages:")
print(get_messages(chat_id))

print("\nDatabase test completed!")
