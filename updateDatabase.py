from utils.Yapiutil import Yapi
if __name__ == '__main__':
    yapi = Yapi()
    yapi.update_positive_database()
    yapi.update_negative_database()