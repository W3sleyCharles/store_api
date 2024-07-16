from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])

# Endpoint para criar um novo produto
@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def criar_produto(
    body: ProductIn = Body(...), 
    usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


# Endpoint para buscar um produto pelo ID
@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def buscar_produto(
    id: UUID4 = Path(alias="id"), 
    usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


# Endpoint para listar todos os produtos
@router.get(path="/", status_code=status.HTTP_200_OK)
async def listar_produtos(
    usecase: ProductUsecase = Depends()
) -> List[ProductOut]:
    return await usecase.query()


# Endpoint para atualizar um produto pelo ID
@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def atualizar_produto(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    return await usecase.update(id=id, body=body)


# Endpoint para deletar um produto pelo ID
@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(
    id: UUID4 = Path(alias="id"), 
    usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
