#Libraries needed for this python program
from pathlib import Path

#Sets path where database is present in
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "database" 
DB_PATH = DATA_DIR / "intelligence_platform.db"