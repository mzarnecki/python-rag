import os
import sys

import psycopg2
import psycopg2.extras


class AbstractDocumentRepository:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host='postgres',
                port=5432,
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                cursor_factory=psycopg2.extras.RealDictCursor,
            )
            self.connection.autocommit = True
        except psycopg2.Error as e:
            sys.exit('Connection failed: ' + str(e))
