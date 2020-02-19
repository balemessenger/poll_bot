# In the name of God
import os


class Config:
    token = os.getenv("TOKEN", "{token}")
    base_file_url = os.environ.get("BASE_FILE_URL", "https://tapi.bale.ai/file/")
    base_url = os.environ.get("BASE_URL", "https://tapi.bale.ai/")
    db_user = os.getenv("POSTGRES_USER", "test")
    db_password = os.getenv("POSTGRES_PASSWORD", "test")
    db_name = os.getenv("POSTGRES_DB", "test_db")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", 5432 )
    database_url = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name)
    supported_users = os.environ.get('SUPPORTED_USERS', '1429755505') #for uploading polling and get report
    SUPPORTED_USERS = supported_users.split(',')

