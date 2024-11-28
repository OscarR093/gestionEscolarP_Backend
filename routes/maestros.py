from bson import ObjectId
from fastapi import APIRouter, status,Response
from pymongo import MongoClient
from bson.objectid import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import HTTPException

from models.maestro import Maestro
from models.queryModel import QueryModel
from database import db
from schemas.maestro import userEntity, usersEntity

router = APIRouter()


@router.get('/', response_model=list[Maestro], tags=["Maestros"])
async def find_all_maestros():
    # print(list(conn.local.user.find()))
    return usersEntity(db.maestros.find())


@router.post('/', response_model=Maestro, tags=["Maestros"])
async def create_maestros(maestro: Maestro):
    new_maestro = dict(maestro)
    del new_maestro["id"]
    id = db.maestros.insert_one(new_maestro).inserted_id
    maestro = db.maestros.find_one({"_id": id})
    return userEntity(maestro)


@router.get('/{id}', response_model=Maestro, tags=["Maestros"])
async def find_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    maestro = db.maestros.find_one({"_id": ObjectId(id)})
    if not maestro:
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    
    return userEntity(maestro)



@router.put("/{id}", response_model=Maestro, tags=["Maestros"])
async def update_maestro(id: str, maestro: Maestro):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    existing_maestro = db.maestros.find_one({"_id": ObjectId(id)})
    if not existing_maestro:
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    
    # Actualiza el documento
    db.maestros.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(maestro)}
    )
    
    # Recupera el documento actualizado
    updated_maestro = db.maestros.find_one({"_id": ObjectId(id)})
    return userEntity(updated_maestro)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Maestros"])
async def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    existing_maestro = db.maestros.find_one({"_id": ObjectId(id)})
    if not existing_maestro:
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    
    # Elimina el documento
    db.maestros.find_one_and_delete({"_id": ObjectId(id)})
    
    # Responde con un código 204 sin contenido
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/search/")
def search_by_field(query: QueryModel):
    """
    Busca documentos en la colección utilizando un campo y valor dinámico.
    """
    try:
        # Construir el filtro dinámico
        filtro = {query.field: query.value}
        resultados = list(db.maestros.find(filtro))

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