# encoding:utf-8
# dialect+driver://username:password@host:port/database
import os
SECRET_KEY = os.urandom(24)
DEBUG = True
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '10.142.7.8'
PORT = '3306'
DATABASE = 'dibo'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
