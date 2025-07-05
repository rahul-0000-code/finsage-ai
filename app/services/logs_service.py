# Dummy logs for illustration
user_logs = {}

async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "rahul@gmail.com"

async def get_conversation_history(user_email):
    return user_logs.get(user_email, [
        {"question": "How to save tax?", "answer": "Invest in 80C instruments."}
    ])
