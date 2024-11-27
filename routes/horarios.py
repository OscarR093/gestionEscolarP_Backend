from fastapi import APIRouter, status,Response
from pymongo import MongoClient
from bson.objectid import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import HTTPException

from models.horario import Horario
from database import db
from schemas.horario import userEntity, usersEntity

router = APIRouter()


@router.get('/', response_model=list[Horario], tags=["Horarios"])
async def find_all_horarios():
    # print(list(conn.local.user.find()))
    return usersEntity(db.horarios.find())


@router.post('/', response_model=Horario, tags=["Horarios"])
async def create_horarios(horario: Horario):
    new_horario = dict(horario)
    del new_horario["id"]
    id = db.horarios.insert_one(new_horario).inserted_id
    horario = db.horarios.find_one({"_id": id})
    return userEntity(horario)


@router.get('/{id}', response_model=Horario, tags=["Horarios"])
async def find_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    horario = db.horarios.find_one({"_id": ObjectId(id)})
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    return userEntity(horario)



@router.put("/{id}", response_model=Horario, tags=["Horarios"])
async def update_horario(id: str, horario: Horario):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    existing_horario = db.horarios.find_one({"_id": ObjectId(id)})
    if not existing_horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    # Actualiza el documento
    db.horarios.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(horario)}
    )
    
    # Recupera el documento actualizado
    updated_horario = db.horarios.find_one({"_id": ObjectId(id)})
    return userEntity(updated_horario)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Horarios"])
async def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    existing_horario = db.horarios.find_one({"_id": ObjectId(id)})
    if not existing_horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    # Elimina el documento
    db.horarios.find_one_and_delete({"_id": ObjectId(id)})
    
    # Responde con un código 204 sin contenido
    return Response(status_code=status.HTTP_204_NO_CONTENT)
