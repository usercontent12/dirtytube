import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Cloudflare D1 Database Configuration
    D1_ACCOUNT_ID = os.environ.get('D1_ACCOUNT_ID')
    D1_DATABASE_ID = os.environ.get('D1_DATABASE_ID')
    
    # Separate API keys for read and write operations
    D1_READ_API_KEY = os.environ.get('D1_READ_API_KEY')
    D1_WRITE_API_KEY = os.environ.get('D1_WRITE_API_KEY')
    
    # Cloudflare R2 Worker Configuration
    R2_WORKER_URL = os.environ.get('CLOUDFLARE_WORKER_URL')
    
    # Application Settings
    VIDEOS_PER_PAGE = 20