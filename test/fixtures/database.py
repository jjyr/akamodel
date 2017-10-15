from sqlalchemy import MetaData, create_engine

metadata = MetaData()
db = create_engine('mysql+pymysql://localhost/test')
