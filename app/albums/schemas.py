def albumEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username": str(item["username"]),
        "title": item["title"],
        "is_active": item["is_active"],
        "created": str(item["created"]),
        "cover":item["cover"],
    }


def albumsEntity(entity) -> list:
    return [albumEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]