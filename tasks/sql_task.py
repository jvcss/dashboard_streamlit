from databases import Database

class SqlTask:
    """
        :param db_url: URL de conexão ao banco de dados (PostgreSQL ou MySQL)
        :param query: Query SQL a ser executada
        :param params: Parâmetros para a query (opcional)
    """
    def __init__(self, db_url, query, params=None):
        self.db_url = db_url
        self.query = query
        self.params = params

    async def execute(self):
        """
            Executa a consulta SQL no banco de dados especificado.
            :return: Resultado da consulta
        """
        database = Database(self.db_url)
        await database.connect()
        try:
            if self.params:
                return await database.fetch_all(self.query, self.params)
            return await database.fetch_all(self.query)
        finally:
            await database.disconnect()
