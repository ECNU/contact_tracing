import pandas as pd
from service import flow_tone
from util import USERID_path, root_path
from util.conn_db import connDB
import datetime, os
from util.logger import logger
from urllib.parse import quote_plus
from settings_class import settings_obj


def get_engine():
    user1 = quote_plus(settings_obj.user)
    password1 = quote_plus(settings_obj.password)
    host1 = quote_plus(settings_obj.host)
    database1 = quote_plus(settings_obj.database)
    if settings_obj.database_type == "mysql":
        engine = f"mysql+pymysql://{user1}:{password1}@{host1}:{settings_obj.port}/{database1}"
    elif settings_obj.database_type == "oracle":
        engine = f"oracle+cx_oracle://{user1}:{password1}@{host1}:{settings_obj.port}/?service_name={database1}"
        # 当数据库为oracle时，将用户输入的所有字段名转为小写
        settings_obj.user_id_field_name = settings_obj.user_id_field_name.lower()
        settings_obj.time_field_name = settings_obj.time_field_name.lower()
        # 提取 schema 用户名
        if len(settings_obj.table_name.split("."))==2:
            settings_obj.oracle_schema = settings_obj.table_name.split(".")[0]
            settings_obj.table_name = settings_obj.oracle_schema + '.' + settings_obj.table_name.split(".")[1].lower()
        else:
            settings_obj.table_name = settings_obj.table_name.lower()
        settings_obj.location_filed_names = [x.lower() for x in settings_obj.location_filed_names]
        settings_obj.result_filed_names = [x.lower() for x in settings_obj.result_filed_names]
    elif settings_obj.database_type == "sqlite":
        # 判断db文件是否存在
        if os.path.exists(settings_obj.db_path):
            engine = f"sqlite:///{settings_obj.db_path}?check_same_thread=False"
        else:
            logger.error(f"{settings_obj.db_path}不存在，无法连接到数据库")
            raise Exception("无法连接到数据库")
    else:
        logger.error(f"仅支持三种数据库类型：mysql、oracle、sqlite，不支持您输入的{settings_obj.database_type}数据库")
        raise Exception("无法连接到数据库")
    return engine


def style_apply(series, color):
    """
    :param series: 传过来的数据是DataFramt中的一行  类型为pd.Series
    :param color: 颜色值
    :return:
    """
    length = len(series)
    if str(series[settings_obj.user_id_field_name]) == str(series["contact_"+settings_obj.user_id_field_name]):
        return ['background-color: ' + color] * length
    else:
        # 不符合规则的背景颜色为白色
        return ["background-color: #FFFFFF"] * length


def output(result_df):
    # 输出结果
    result_folder = os.path.join(root_path, "result")
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    result_path = os.path.join(result_folder, nowTime + ".xlsx")
    # 添加颜色，规则，当user_id_field_name和contact_user_id_field_name列相等时将该行标注为黄色
    style_df = result_df.style.apply(style_apply, color="#FFFF00", axis=1)
    with pd.ExcelWriter(result_path, engine='openpyxl') as writer:
        # 注意： 二级标题的to_excel index 不能为False
        style_df.to_excel(writer, index=False, encoding='utf_8_sig')


def check_result_filed_names():
    if settings_obj.user_id_field_name not in settings_obj.result_filed_names:
        logger.warning(f"您输入的{settings_obj.result_filed_names}不包含{settings_obj.user_id_field_name},自动加上{settings_obj.user_id_field_name}这一列")
        settings_obj.result_filed_names.append(settings_obj.user_id_field_name)


def handle():
    # 读取excel表格中的 USERID.xlsx 中的userid
    df = pd.read_excel(USERID_path)
    user_ids = df.iloc[:,0].astype(str).unique() # 转为str类型和去重
    # 检查result_filed_names中是否包含user_id_field_name，如果不好含就加上
    check_result_filed_names()
    # 数据库操作对象
    conn = connDB(get_engine())
    # 流调查询
    result_df = flow_tone(user_ids,conn)

    output(result_df)  # 输出


if __name__ == "__main__":
    handle()
