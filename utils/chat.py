async def create_chat_handler(users_collection, messages_collection, user_a_username, user_b_username):
    existing_user_b = await users_collection.find_one({"username": user_b_username})
    if not existing_user_b:
        return {"error": "There is no such user with such username"}

    existing_chat = await messages_collection.find_one({
        "$or": [
            {"user_a_username": user_a_username, "user_b_username": user_b_username},
            {"user_a_username": user_b_username, "user_b_username": user_a_username}
        ]
    })
    if existing_chat:
        return {"error": "Chat between these users already exists"}

    result = await messages_collection.insert_one(
        {
            "user_a_username": user_a_username,
            "user_b_username": user_b_username,
        }
    )

    await users_collection.update_one(
        {"username": user_a_username},
        {"$addToSet": {"chats": user_b_username}}
    )

    await users_collection.update_one(
        {"username": user_b_username},
        {"$addToSet": {"chats": user_a_username}}
    )

    return str(result.inserted_id)
