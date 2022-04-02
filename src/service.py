'''
流调查询
'''
from settings_class import settings_obj
import pandas as pd
from util.logger import logger
from sqlalchemy import desc
from datetime import datetime,timedelta


def get_forward_backward_time(current_time, minutes):
    # 获取向前和向后的时间
    if isinstance(current_time,str):
        current = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    else:
        current =current_time
    backward_time = current + timedelta(minutes=minutes)
    forward_time = current - timedelta(minutes=minutes)
    return forward_time, backward_time


def get_forward_contact(forward_time, current_time, location_condition_str, user_id, conn,table_obj,close_contact_record_num):
    '''
    先向前查询,逻辑为 查询在向前时间到当前时间范围内，在该校区和该地点内的，并以时间倒序排序查询的限制close_contact_record_num
    :return:
    '''
    # 查（在限制的时间范围内）close_contact_record_num 条记录
    s = f"conn.session.query({settings_obj.result_filed_names_str}).filter(table_obj.c[settings_obj.user_id_field_name]!=user_id, table_obj.c[settings_obj.time_field_name]>=forward_time, table_obj.c[settings_obj.time_field_name]<=current_time, {location_condition_str}).order_by(desc(table_obj.c[settings_obj.time_field_name])).limit(close_contact_record_num).all()"
    records = eval(s)
    forward_results = [list(result) for result in records]
    return forward_results


def get_backward_contact(backward_time,current_time,location_condition_str,user_id,conn,table_obj,close_contact_record_num):
    '''
    再向后查询,逻辑为 查询在当前时间到向后时间范围内，在该校区和该地点内的，并以时间正序排序查询的限制close_contact_record_num 条消费记录
    :param close_contact_record_num:
    :param backward_time:
    :param current_time:
    :param location_condition_str:
    :param user_id:
    :param conn:
    :return:
    '''
    # 先查（在限制的时间范围内））close_contact_record_num 条记录
    s =f"conn.session.query({settings_obj.result_filed_names_str}).filter(table_obj.c[settings_obj.user_id_field_name]!=user_id, table_obj.c[settings_obj.time_field_name]>=current_time, table_obj.c[settings_obj.time_field_name]<=backward_time, {location_condition_str}).order_by(table_obj.c[settings_obj.time_field_name]).limit(close_contact_record_num).all()"
    records = eval(s)
    backward_results = [list(result) for result in records]
    return backward_results


def get_backward_contacts(backward_time, current_time, location_condition_str, user_id, conn,table_obj, close_contact_record_num=settings_obj.close_contact_people_num, backward_result_df=None):
    if backward_result_df is None:
        backward_result_df = pd.DataFrame(columns=settings_obj.result_filed_names)
    backward_results = get_backward_contact(backward_time, current_time, location_condition_str, user_id, conn,table_obj, close_contact_record_num)
    if len(backward_results)>0:
        tem_df = pd.DataFrame(backward_results,columns=backward_result_df.columns)
        backward_result_df = pd.concat([backward_result_df, tem_df], ignore_index=True)
    backward_result_df.sort_values(by=settings_obj.time_field_name, inplace=True, ascending=True) # 升序
    if len(backward_results)>=close_contact_record_num:
        close_contact_record_num  = settings_obj.close_contact_people_num - backward_result_df[settings_obj.user_id_field_name].nunique()
        if close_contact_record_num>0 and len(backward_result_df)>0:
            current_time = backward_result_df.loc[len(backward_result_df)-1,settings_obj.time_field_name]
            user_id = backward_result_df.loc[len(backward_result_df)-1,settings_obj.user_id_field_name]
            backward_result_df = get_backward_contacts(backward_time,current_time, location_condition_str, user_id, conn,table_obj,close_contact_record_num=close_contact_record_num,backward_result_df=backward_result_df)
    return backward_result_df


def get_forward_contacts(forward_time, current_time, location_condition_str, user_id, conn, table_obj, close_contact_record_num=settings_obj.close_contact_people_num, forward_result_df=None):
    '''
    递归查询
    :param table_obj:
    :param forward_time:
    :param current_time:
    :param location_condition_str:
    :param user_id:
    :param conn:
    :param close_contact_record_num:
    :param forward_result_df:
    :return: 返回dataframe格式
    '''
    if forward_result_df is None:
        forward_result_df = pd.DataFrame(columns=settings_obj.result_filed_names)
    forward_results = get_forward_contact(forward_time, current_time, location_condition_str, user_id, conn,table_obj,close_contact_record_num)
    if len(forward_results)>0:
        tem_df = pd.DataFrame(forward_results, columns=forward_result_df.columns)
        forward_result_df = pd.concat([forward_result_df, tem_df], ignore_index=True)
    forward_result_df.sort_values(by=settings_obj.time_field_name, inplace=True, ascending=True) # 升序
    if len(forward_results)>=close_contact_record_num:
        # 这时候在forward_time, current_time时间范围内所有记录都已经被查询出
        close_contact_record_num  = settings_obj.close_contact_people_num - forward_result_df[settings_obj.user_id_field_name].nunique()
        if close_contact_record_num>0 and len(forward_result_df)>0:
            current_time = forward_result_df.loc[0,settings_obj.time_field_name]
            user_id = forward_result_df.loc[0,settings_obj.user_id_field_name]
            forward_result_df = get_forward_contacts(forward_time,current_time, location_condition_str, user_id, conn, table_obj,close_contact_record_num=close_contact_record_num,forward_result_df=forward_result_df)
    return forward_result_df


def change_time_type(time,table_obj):
    '''
    转换str_time的类型
    :param time: 字符串或者datetime两种类型
    :param table_obj:
    :return:
    '''
    if isinstance(time,datetime) or isinstance(time,str):
        if table_obj.c[settings_obj.time_field_name].type.python_type==datetime:
            if isinstance(time,str):
                return datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        else:
            if isinstance(time,datetime):
                return str(time)
    return time


def change_userid_type(user_id,table_obj):
    if table_obj.c[settings_obj.user_id_field_name].type.python_type==int:
        return int(user_id)
    return str(user_id)


def get_contact(user_id, conn, table_obj):
    # 针对user_id进行密接查询
    # 首先查询user_id在flow_tone_start_time和flow_tone_end_time时间内的消费记录
    # 因为user_id对应的消费记录也需要输出，所以查询时要查出包括location_filed_names、time_field_name、result_filed_names中的所有字段
    flow_tone_start_time = change_time_type(settings_obj.flow_tone_start_time, table_obj)
    flow_tone_end_time = change_time_type(settings_obj.flow_tone_end_time, table_obj)
    user_id = change_userid_type(user_id,table_obj)
    s = f"conn.session.query({settings_obj.filed_names_str}).filter(table_obj.c[settings_obj.user_id_field_name]== user_id, table_obj.c[settings_obj.time_field_name]>=flow_tone_start_time, table_obj.c[settings_obj.time_field_name]<=flow_tone_end_time).order_by(table_obj.c[settings_obj.time_field_name]).all()"
    records = eval(s)
    result_df = pd.DataFrame(columns=settings_obj.result_filed_names)
    for record in records:
        # 针对每一条消费记录，分别查询在该时间前后close_contact_time分钟内在该地点消费的相关记录，不超过多少人
        current_time = record[settings_obj.time_field_name]
        forward_time, backward_time = get_forward_backward_time(current_time, settings_obj.close_contact_time)
        forward_time = change_time_type(forward_time, table_obj)
        backward_time = change_time_type(backward_time, table_obj)
        current_time = change_time_type(current_time, table_obj)
        location_condition_list = []
        for location_filed_name in settings_obj.location_filed_names:
            location_condition = f"table_obj.c['{location_filed_name}']=='{record[location_filed_name]}'"
            location_condition_list.append(location_condition)
        location_condition_str = ", ".join(location_condition_list)
        # 先向前查询
        forward_results = get_forward_contacts(forward_time,current_time,location_condition_str,user_id,conn,table_obj)
        forward_results.drop_duplicates(subset=[settings_obj.user_id_field_name], keep ='last', inplace = True) # 去重
        # 先向后查询
        backward_results = get_backward_contacts(backward_time,current_time,location_condition_str,user_id,conn,table_obj)
        backward_results.drop_duplicates(subset=[settings_obj.user_id_field_name], keep ='first', inplace = True)
        # 放在一起
        result_df = pd.concat([result_df, forward_results], ignore_index=True)
        userid_result = [record[i] for i in settings_obj.result_filed_names]
        result_df.loc[len(result_df)] = userid_result # 记录user_id对应的消费记录
        result_df = pd.concat([result_df, backward_results], ignore_index=True)
    result_df["contact_" + settings_obj.user_id_field_name] = user_id
    return result_df


def change_settings_obj():
    '''
    将settings_obj 中的列表参数转为字符串
    :return:
    '''
    tmp_result_filed_names2 = settings_obj.result_filed_names.copy()
    tmp_result_filed_names2.append(settings_obj.time_field_name)
    tmp_result_filed_names2.extend(settings_obj.location_filed_names)
    tmp_result_filed_names2= ["table_obj.c['"+i+"']" for i in set(tmp_result_filed_names2)]
    filed_names_str = ", ".join(tmp_result_filed_names2)
    settings_obj.filed_names_str = filed_names_str
    tmp_result_filed_names3= ["table_obj.c['"+i+"']" for i in settings_obj.result_filed_names]
    result_filed_names_str = ", ".join(tmp_result_filed_names3)
    settings_obj.result_filed_names_str = result_filed_names_str


def flow_tone(user_ids, conn):
    # 定义输出的df
    tmp_result_filed_names = settings_obj.result_filed_names.copy()
    result_columns = tmp_result_filed_names.append("contact_" + settings_obj.user_id_field_name)
    result_df = pd.DataFrame(columns=result_columns)
    change_settings_obj()
    # 获取数据库表的对象
    table_obj = conn.get_table_obj(settings_obj.table_name,settings_obj)
    for user_id in user_ids:
        # 针对每一条 user_id 进行密接查询
        logger.info(f"针对 {settings_obj.user_id_field_name} 为 {user_id} 的人员进行密接查询")
        sub_result_df = get_contact(user_id, conn, table_obj)
        result_df = pd.concat([result_df, sub_result_df], ignore_index=True)
    return result_df
