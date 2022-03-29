# 数据库配置
database_type="sqlite" #支持三种数据库类型：mysql、oracle、sqlite
user = ""
password = ""
host = ""
port=""
database=""
db_path="./example.db" # 绝对路径，当数据库为sqlite时需要填写，而user、password、host、port、database不需要填写

# 与数据库表相关
table_name = "example" # 表名
user_id_field_name = "USERID" # 表示用户id的字段名
time_field_name = "RECORDTIME" # 表示时间的字段名
location_filed_names = ["XIAOQU","TERMNAME"] # 表示位置的字段，可能是多个，比如有校区字段加位置字段

# 输出结果字段 (与数据库表中定义的字段名称相关，默认应该为：用户id的字段、时间的字段名、位置的字段；程序内部在自动加上一个与该用户密接的用户id字段)
result_filed_names = ["USERID","RECORDTIME","XIAOQU","TERMNAME","TYPE"]


# 时间范围
flow_tone_start_time = "2022-03-01 00:00:00"
flow_tone_end_time = "2022-03-10 00:00:00"

# 密接限制人数
close_contact_people_num = 5

# 密接限制时间 （分钟）
close_contact_time = 30