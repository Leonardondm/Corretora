# app/routes/backup_routes.py
from fastapi import APIRouter, HTTPException, Query
from app.services.backup_service import create_backup, restore_backup
from pydantic import BaseModel

router = APIRouter()

class RestoreRequest(BaseModel):
    backup_filename: str

@router.post("/backup/create")
async def create_backup_endpoint():
    return create_backup()

@router.post("/backup/restore")
async def restore_backup_endpoint(request: RestoreRequest):
    return restore_backup(request.backup_filename)