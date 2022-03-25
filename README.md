# contact_tracing
基于行为数据快速定位密切接触者

## 运行环境
python3

## 依赖安装

```
pip3 install -r requirement.txt
```

## 配置

### 数据库和密接参数
修改 `settings.py` 配置文件，配置基本参数

```ini
# 数据库配置
database_type="sqlite" #支持三种数据库类型：mysql、oracle、sqlite
user = "" # 会进行特殊字符转义
password = "" # 会进行特殊字符转义
host = "" # 会进行特殊字符转义
port="" #数据库连接端口
database="" # 会进行特殊字符转义，当连接 oracle 时，等价于 oracle 连接的 service
db_path="./example.db" # 绝对路径，当数据库为sqlite时需要填写，而user、password、host、port、database不需要填写

# 与数据库表相关
table_name = "example" # 表名
user_id_field_name = "USERID" # 表示用户id的字段名
time_field_name = "RECORDTIME" # 表示时间的字段名
location_filed_names = ["XIAOQU","TERMNAME"] # 表示位置的字段，可能是多个，比如有校区字段加位置字段

# 输出结果字段 (与数据库表中定义的字段名称相关，默认应该为：用户id的字段、时间的字段名、位置的字段；程序内部在自动加上一个与该用户密接的用户id字段；)
result_filed_names = ["USERID","RECORDTIME","XIAOQU","TERMNAME","TYPE"]


# 时间范围
flow_tone_start_time = "2022-03-01 00:00:00"
flow_tone_end_time = "2022-03-10 00:00:00"

# 密接限制人数
close_contact_people_num = 5

# 密接限制时间 （分钟）
close_contact_time = 30
```

### 输入参数
在 `USERID.xlsx` 表格中填入 `userid`，每行一个

|userid|
|---|
|5584f3b2676bacb3be35ae3face871781c2e92f0|
|e04b4e51b82b29abcec68d5ec8dab9c3d7b68591|

## 执行
在 `src` 目录下执行 `main.py`

```bash
cd src/
python3 main.py
```

## 输出

1. 在 `result` 目录下，以运行时间为命名的文件即为流调输出
2. 其中被标注为黄色的行是输入的流调人员的消费记录

## 运行逻辑
`. 第一步，读取输入的user_id，一个个进行密接查询
2. 查询某个user_id在流调时间内的消费记录
3. 根据每一条记录进行下游查询，查询在该记录中的同一地点同一时间在前后若干分钟内的消费记录，取限定范围的人数。
4. 将所有记录输出到指定表格并高亮输入人员的单元格