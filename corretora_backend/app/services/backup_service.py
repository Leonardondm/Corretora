# app/services/backup_service.py
import os
import subprocess
from datetime import datetime
from fastapi import HTTPException

DATABASE_URL = os.getenv("DATABASE_URL")

def create_backup():
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filename = f"backup_{timestamp}.sql"
        backup_path = os.path.join("backups", backup_filename)
        
        # Ensure the backups directory exists
        os.makedirs("backups", exist_ok=True)
        
        # Use pg_dump to create a backup
        command = f"pg_dump {DATABASE_URL} > {backup_path}"
        subprocess.run(command, shell=True, check=True)
        
        return {"message": f"Backup created successfully: {backup_filename}"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")

def restore_backup(backup_filename: str):
    try:
        backup_path = os.path.join("backups", backup_filename)
        
        if not os.path.exists(backup_path):
            raise HTTPException(status_code=404, detail="Backup file not found")
        
        # Use psql to restore the backup
        command = f"psql {DATABASE_URL} < {backup_path}"
        subprocess.run(command, shell=True, check=True)
        
        return {"message": f"Backup restored successfully: {backup_filename}"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")