from logging import getLogger, DEBUG,StreamHandler,Formatter,FileHandler,ERROR
import sys,os
from . import root_path

# 创建一个日志器logger并设置其日志级别为DEBUG
logger = getLogger('logger')
logger.setLevel(DEBUG)

log_folder = os.path.join(root_path, "log")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
log_all_file = os.path.join(log_folder,"all.log")
log_error_file = os.path.join(log_folder,"error.log")

file_all_handler = FileHandler(log_all_file,encoding="utf-8")
file_all_handler.setLevel(DEBUG)
file_error_handler = FileHandler(log_error_file,encoding="utf-8")
file_error_handler.setLevel(ERROR)

# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)

# 创建一个格式器formatter并将其添加到处理器handler
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
file_all_handler.setFormatter(formatter)
file_error_handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)
logger.addHandler(file_all_handler)
logger.addHandler(file_error_handler)