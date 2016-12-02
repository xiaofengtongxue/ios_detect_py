import config
import data
from modules import *
from Utils import *

class ios():
    def __init__(self):
        data.client = set_ssl_conn(config.mobile_ip, config.port, config.mobile_user, config.mobile_password)
        # data.omp_client = ssh.set_ssl_conn(config.server_ip, config.port, config.server_user, config.server_password)
        self.db = DBServer()
        self.db.on()
        Utils.getInstalledAppList()

    def detect(self):
        Metadata().get_metadata()
        # scan_task = Scan("127.0.0.1", "test_")
        # scan_task.openvas_start()
        # scan_task.creat_target()
        SharedLibrary().get()
        protect_check().check()
        # static_analyzer().do_analyse()
        Plist().get()
        Sql().get()
        String().get_url()
        # openvas().launch()
        # openvas().parse()

    def clean(self):
        data.client.close()
        self.db.down()
        # data.omp_client.close()


ios().detect()