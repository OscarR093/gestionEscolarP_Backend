from bson import ObjectId
from fastapi import APIRouter, status,Response
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt
from starlette.status import HTTP_204_NO_CONTENT
from models.queryModel import QueryModel
from fastapi import HTTPException

from models.user import User
from database import db
from schemas.user import userEntity, usersEntity 

router = APIRouter()


@router.get('/', response_model=list[User], tags=["users"])
async def find_all_users():
    # print(list(db.users.find()))
    return usersEntity(db.users.find())


@router.post('/', response_model=User, tags=["users"])
async def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    id = db.users.insert_one(new_user).inserted_id
    user = db.users.find_one({"_id": id})
    return userEntity(user)


@router.get('/{id}', response_model=User, tags=["users"])
async def find_user(id: str):
    return userEntity(db.users.find_one({"_id": ObjectId(id)}))


@router.put("/{id}", response_model=User, tags=["users"])
async def update_user(id: str, user: User):
    db.users.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(user)
    })
    return userEntity(db.users.find_one({"_id": ObjectId(id)}))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
    db.users.find_one_and_delete({
        "_id": ObjectId(id)
    })
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.post("/search/")
def search_by_field(query: QueryModel):
    """
    Busca documentos en la colección utilizando un campo y valor dinámico.
    """
    try:
        # Construir el filtro dinámico
        filtro = {query.field: query.value}
        resultados = list(db.users.find(filtro))

        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron documentos que coincidan con el criterio")
        
        # Convertir ObjectId a string
        for resultado in resultados:
            if "_id" in resultado:
                resultado["id"] = str(resultado["_id"])
                resultado.pop("_id")

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))