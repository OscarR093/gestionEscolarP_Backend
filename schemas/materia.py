def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nombre": item["nombre"],
        "HoraInicio": item["HoraInicio"],
        "HoraFinal": item["HoraFinal"],
        "Asignada":item["Asignada"]
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]