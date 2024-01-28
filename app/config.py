import os, random, string

class Config:

    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # set up the App SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase ) for i in range( 32 ))
    
    DB_ENGINE   = os.getenv('DB_ENGINE',    None)
    DB_USERNAME = os.getenv('DB_USERNAME',  None)
    DB_PASS     = os.getenv('DB_PASS',      None)
    DB_HOST     = os.getenv('DB_HOST',      None)
    DB_PORT     = os.getenv('DB_PORT',      None)
    DB_NAME     = os.getenv('DB_NAME',      None)

    USE_SQLITE = True

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:

            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                    DB_ENGINE,
                    DB_USERNAME,
                    DB_PASS,
                    DB_HOST,
                    DB_PORT,
                    DB_NAME
                )
            
            USE_SQLITE = False
        
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e))
            print('Fallback to SQLite ')
    
    if USE_SQLITE:

        # create file in <app> folder
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')


