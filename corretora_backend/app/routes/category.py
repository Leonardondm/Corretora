from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category as CategoryModel
from app.schemas.category import CategoryCreate, Category
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar uma nova categoria
@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Instancia o modelo CategoryModel com os dados fornecidos
    db_category = CategoryModel(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Rota para obter todas as categorias
@router.get("/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(CategoryModel).offset(skip).limit(limit).all()
    return categories

# Rota para obter uma categoria específica
@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_category

# Rota para atualizar uma categoria
@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

# Rota para deletar uma categoria
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(db_category)
    db.commit()
    return None