from config.settings import get_log_path
import logging
import time
import os

# 控制台输出
STREAM = True


class LogUtil:
    def __init__(self):
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            self.log_name = '{}.log'.format(time.strftime("%Y_%m_%d", time.localtime()))
            self.log_path_file = os.path.join(get_log_path(), self.log_name)
            fh = logging.FileHandler(self.log_path_file, encoding='utf-8', mode='a')
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

            fh.close()

            if STREAM:
                fh_stream = logging.StreamHandler()
                fh_stream.setLevel(logging.DEBUG)
                fh_stream.setFormatter(formatter)
                self.logger.addHandler(fh_stream)

    def log(self):
        # 返回定义好的logger对象
        return self.logger


logger = LogUtil().log()

if __name__ == '__main__':
    logging.error('test')
