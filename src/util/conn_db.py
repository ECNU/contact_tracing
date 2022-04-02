from sqlalchemy import Table, create_engine, MetaData, func
from sqlalchemy.orm import Session


class connDB():
    '''
    https://www.osgeo.cn/sqlalchemy/tutorial/dbapi_transactions.html
    数据库操作
    '''
    def __init__(self,check_engine,echo=False):
        '''初始化连接数据库'''
        # 用户名：密码@host：port/数据库名
        self.engine = create_engine(check_engine,echo=echo)
        self.metadata = MetaData(bind=self.engine)
        self.session = Session(self.engine)

    def get_table_obj(self,table_name,settings_obj):
        '''
        返回数据库表映射的对象
        :param settings_obj:
        :param table_name:
        :return:
        '''
        if hasattr(settings_obj,"oracle_schema"):
            self.metadata.reflect(bind=self.engine, schema=settings_obj.oracle_schema, views=True)
        table_obj = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
        return table_obj

    def select_data(self,sql):
        '''
        使用原生sql进行查询
        :param sql:
        :return:
        '''
        conn = self.engine.connect()
        results = conn.execute(sql)
        result_list = [dict(zip(result.keys(), result)) for result in results]
        conn.close()

        return result_list

    def select_data_list(self, sql):
        '''
        使用原生sql进行查询
        :param sql:
        :return:
        '''
        conn = self.engine.connect()
        results = conn.execute(sql)
        result_list = [result.values() for result in results]
        conn.close()

        return result_list
