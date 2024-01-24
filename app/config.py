import os

class Config:
    
    SERCRET_KET = os.environ.get('SECRET_KEY') or 'my-very-secret-key'