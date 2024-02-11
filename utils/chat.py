async def create_chat_handler(users_collection, chat_collection, user_a_username, user_b_username):
    error = True

    existing_user_b = await users_collection.find_one({"username": user_b_username})
    if not existing_user_b:
        return {"error": "There is no such user with such username"}, error

    if user_a_username == user_b_username:
        return {"error": "Can't create a chat room with yourself"}, error

    existing_chat = await chat_collection.find_one({
        "$or": [
            {"user_a_username": user_a_username, "user_b_username": user_b_username},
            {"user_a_username": user_b_username, "user_b_username": user_a_username}
        ]
    })
    if existing_chat:
        return {"error": "Chat between these users already exists"}, error

    result = await chat_collection.insert_one(
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

    error = False

    return str(result.inserted_id), error
