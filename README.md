# contact_tracing
基于行为数据快速追踪密切接触者的脚本方案

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
|f4efde7189962a420d41d7dbc6ba570c0c723b47|
|ad9322aac7896a0479f298541f0bd1f6d48e0220|


## 执行
在 `src` 目录下执行 `main.py`

```bash
cd src/
python3 main.py
```

## 输出

1. 在 `result` 目录下，以运行时间为命名的文件即为流调输出
2. 其中被标注为黄色的行是输入的流调人员的消费记录

<table><tbody>
    <tr>
        <th>USERID</th><th>RECORDTIME</th><th>XIAOQU</th><th>TERMNAME</th><th>TYPE</th><th>contact_USERID</th>
    </tr>
    <tr>
    <td>dbfe97c4ae7999b6c5bb9cb336f5d1c0a70cedd8</td><td>2022-03-01 06:25:18</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td></td>
    </tr>
    <tr><td>32bc3dabc33ab9f833ce7e2c7489fd4083f4f6a0</td><td>2022-03-01 06:27:20</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td></tr>
<tr>
<td>9e6383e5d1b6106411e0cbb067bddbc37e746a1d</td><td>2022-03-01 06:32:28</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>81c99f0ac92fb7a1463fba6fa50ff27cc78f6f81</td><td>2022-03-01 06:35:37</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>5f56be63bde0e5440c73dc1ae47c1fe6b4eec5c7</td><td>2022-03-01 06:35:53</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr style="background-color: yellow"><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td><td>2022-03-01 06:38:33</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>0fddd8486b12f646b4f9d68516f3aeaf31a07d62</td><td>2022-03-01 06:38:43</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>45cd7842331cfeef729eda739e2f017558d4355c</td><td>2022-03-01 06:39:44</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>a96a4375da92f79fdb30ab44c4a263d9a0fc4000</td><td>2022-03-01 06:41:12</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>9cb31f5177c5adc59fb229fbfe480210194184e8</td><td>2022-03-01 06:42:10</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>    
<tr><td>784f7a147eb50759fd08b6f407693d8fdb3379f7</td><td>2022-03-01 06:42:24</td><td>校区A</td><td>A餐厅25#</td><td>餐费支出</td><td>ad9322aac7896a0479f298541f0bd1f6d48e0220</td>
</tr>
</table>

## 运行逻辑
1. 第一步，读取输入的user_id，一个个进行密接查询
2. 查询某个user_id在流调时间内的消费记录
3. 根据每一条记录进行下游查询，查询在该记录中的同一地点同一时间在前后若干分钟内的消费记录，取限定范围的人数。
4. 将所有记录输出到指定表格并高亮输入人员的单元格

## 申明
仓库内的 `example.db` 相关数据均为随机生成的测试数据，仅用于测试验证，没有实际含义。

本项目开发过程中仅使用上述测试数据开发，没有使用任何真实个人信息。

本项目由社区自发开源，不代表官方立场。