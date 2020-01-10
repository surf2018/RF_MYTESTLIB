import sys
sys.path.append("C:\Python27\Lib")
import os
import time
from ftplib import FTP
class _downloadApk(object):
    """downlaod latest apk from ftp"""
    def __init__(self):
        """
        init ftp
        host:ftp host ip
        username: ftp user
        password: ftp password
        port: ftp port
        """
        self.__host = os.getenv('G_FTPHOSTIP')
        self.__port='21'
        self.__username = os.getenv('G_FTPUSER')
        self.__password = os.getenv('G_FTPPASS')
        self.__apkName= os.getenv('U_APP_ApkName')
        self.__ftp_file_path = os.getenv('G_FTPFILEPATH')
        self.__dst_file_path = os.getenv('G_APPIUM_APP_DIR')
        # self.__host = '10.12.32.163'
        # self.__port='21'
        # self.__username = 'ftpuser'
        # self.__password = 'tvu123admin'
        # self.__apkName= 'TVUAnywhere_V8.0.9.290_2001101334_release.apk'
        # self.__ftp_file_path = '/AnywhereShare/android_release/anywhere/'
        # self.__dst_file_path = 'D:\\AutoTest\\androidApk\\'

    def ftp_connect(self,host,user,pwd):
        """
        connect ftp
        return:
        """
        print host,user,pwd
        ftp = FTP()
        ftp.set_debuglevel(1) #diable debug
        ftp.connect(host=host, port=self.__port) #connect ftp
        ftp.login(user, pwd) #login ftp
        return ftp

    def download_apk(self,package=None,ftp_file_path=None,dst_file_path=None,host=None,user=None,pwd=None):
        """
        download file from ftp server
        param ftp_file_path: ftp download file path
        param dst_file_path: local path
        return:
        """
        """
        Download Apk.
        Examples:
        | Download_Apk | ${package}| ${ftp_file_path} |${dst_file_path}| ${host}|${user}|${pwd}|
        """
        if package is None:
            package = self.__apkName
        if ftp_file_path is None:
            ftp_file_path=self.__ftp_file_path
        if dst_file_path is None:
            dst_file_path=self.__dst_file_path
        if host is None:
            host = self.__host
        if user is None:
            user=self.__username
        if pwd is None:
            pwd=self.__password
        buffer_size = 10240 #default:8192
        ftp = self.ftp_connect(host,user,pwd)
        print ftp.getwelcome() #dispaly ftp login info
        file_list = ftp.nlst(ftp_file_path)
        # print file_list
        ftp_file = os.path.join(ftp_file_path, package)
        print ftp_file
        if(ftp_file in file_list):
            write_file = os.path.join(dst_file_path,package)
            #print write_file
            if not os.path.exists(write_file):
                    print "file_name:"+write_file
                    #ftp_file = os.path.join(ftp_file_path, file_name)
                    #write_file = os.path.join(dst_file_path, file_name)
                    with open(write_file, "wb") as f:
                            ftp.retrbinary('RETR {0}'.format(ftp_file), f.write, buffer_size)
                    f.close()
            else:
                print " file_name is already exist."
        else:
            print "no latest apk in ftp server"

        ftp.quit()

#
if __name__=="__main__":

    n=_downloadApk()
    n.download_apk()