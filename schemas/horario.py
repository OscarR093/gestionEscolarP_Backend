def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "id_profesor": item["id_profesor"],
        "id_materia": item["id_materia"],
        "nombre_profesor": item["nombre_profesor"],
        "apellido_profesor": item["apellido_profesor"],
        "nombre_materia":item["nombre_materia"],
        "hora_inicio":item["hora_inicio"],
        "hora_final":item["hora_final"]
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]