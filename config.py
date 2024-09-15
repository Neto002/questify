from secret import postgreURL

class Config:
    SQLALCHEMY_DATABASE_URI = postgreURL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
