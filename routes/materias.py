from bson import ObjectId
from fastapi import APIRouter, status,Response
from bson.objectid import ObjectId
from fastapi import HTTPException
from models.materia import Materia
from models.queryModel import QueryModel
from database import db
from schemas.materia import userEntity, usersEntity

router = APIRouter()


@router.get('/', response_model=list[Materia], tags=["Materias"])
async def find_all_materias():
    # print(list(conn.local.user.find()))
    return usersEntity(db.materias.find())


@router.post('/', response_model=Materia, tags=["Materias"])
async def create_materias(materia: Materia):
    new_materia = dict(materia)
    del new_materia["id"]
    id = db.materias.insert_one(new_materia).inserted_id
    materia = db.materias.find_one({"_id": id})
    return userEntity(materia)


@router.get('/{id}', response_model=Materia, tags=["Materias"])
async def find_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    materia = db.materias.find_one({"_id": ObjectId(id)})
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    return userEntity(materia)



@router.put("/{id}", response_model=Materia, tags=["Materias"])
async def update_materia(id: str, materia: Materia):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    existing_materia = db.materias.find_one({"_id": ObjectId(id)})
    if not existing_materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    # Actualiza el documento
    db.materias.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(materia)}
    )
    
    # Recupera el documento actualizado
    updated_materia = db.materias.find_one({"_id": ObjectId(id)})
    return userEntity(updated_materia)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Materias"])
async def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    
    existing_materia = db.materias.find_one({"_id": ObjectId(id)})
    if not existing_materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    # Elimina el documento
    db.materias.find_one_and_delete({"_id": ObjectId(id)})
    
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
        resultados = list(db.materias.find(filtro))

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
