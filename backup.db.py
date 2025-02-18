import os
import shutil
from datetime import datetime

def backup_database():
    source_db = 'site.db'
    if not os.path.exists(source_db):
        print(f"No se encontró la base de datos {source_db}")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_db = f'backup_{timestamp}.db'
    
    shutil.copyfile(source_db, backup_db)
    print(f"Copia de seguridad creada: {backup_db}")

if __name__ == "__main__":
    backup_database()