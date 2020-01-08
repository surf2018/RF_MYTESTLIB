import sys
sys.path.append("C:\Python27\Lib")
import os
import time
class _appium_server(object):
    """docstring for appium server"""
    def __init__(self):
        self.__address = os.getenv('G_APPIUM_HOST_ADDRESS','127.0.0.1')
        self.__port = os.getenv('G_APPIUM_HOST_PORT', '4723')
        self.__device_name = os.getenv('U_APPIUM_DEVICE_NAME','SJE5T17B02006511')
        self.__platform_name = os.getenv('G_APPIUM_PLATFORM_NAME', 'Android')
        self.__platform_ver = os.getenv('G_APPIUM_PLATFORM_VERSION','8.0.0')
#        self.__app_package =os.getenv('G_APPIUM_APP_PACKAGE','com.tvunetworks.android.anywhere')
#        self.__app_activity = os.getenv('U_APP_Activity','AppStart')
        self.__auto_name = os.getenv('G_APPIUM_AUTO_NAME', 'Appium')
        reset = os.getenv('G_APPIUM_REINSTALL_RESET', 'False')
        if reset.lower() == 'false':
            self.__reset = '--no-reset'
        elif reset.lower()== 'true':
            self.__reset = '--full-reset'

    def start_appium_server(self):
        """
        Start Appium Server.
        Examples:
        | Start Appium Server |
        """
        reload(sys)
        sys.setdefaultencoding('utf8')
#        print self.__address
        start_cmd = 'start /b appium -a {} -p {} -U {} --platform-name {} --platform-version {} --automation-name {} {} --session-override --command-timeout 1800' \
                    .format(self.__address,
                            self.__port,
                            self.__device_name,
                            self.__platform_name,
                            self.__platform_ver,
 #                           self.__app_package,
 #                           self.__app_activity,
                            self.__auto_name,
                            self.__reset)

        try:
            appium_server_status = self.appium_server_status()
            if appium_server_status.lower() == 'stop' or appium_server_status.lower() == 'warn':
                print start_cmd
                status = os.system(start_cmd)
                if status == 0:
                    print 'Pass! Start Appium Server.'
                else:
                    self.__raiseError('Fail! Could NOT start Appium server.')
            else:
                print 'Appium Server is already started. PID: {}'.format(appium_server_status)
        except Exception as e:
            print str(e)

    def stop_appium_server(self):
        """
        Stop Appium Server.
        Examples:
        | Stop Appium Server |
        """
        try:
            appium_server_status = self.appium_server_status()
            if appium_server_status.lower() == 'stop':
                print 'Appium Server is already stopped.'
            elif appium_server_status.lower() == 'warn':
                self.__raiseError('Warning! Appium Server Error.')
            else:
                pid = appium_server_status
                status = os.system('taskkill /f /pid {}'.format(pid))
                if status == 0:
                    print 'Pass! Stopped Appium Server. PID: {}'.format(pid)
                else:
                    self.__raiseError('Fail! Could NOT Stopp Appium Server.')
        except Exception as e:
            print str(e)

    def appium_server_status(self):
        """
        Check Appium Server Status and return PID if it is running.
        Examples:
        | ${status} | Appium Server Status |
        """
        cmd = 'netstat -nao | findstr {}'.format(self.__port)
        try:
            text = os.popen(cmd)
            content = text.read().strip()
            print '###'
            print 'Appium Server Info: ', content
            print '###'
            if content == '':
                return 'stop'
            elif self.__port in content:
                pid = content.split()[4]
                return pid
            else:
                return 'warn'
        except Exception as e:
            print str(e)
if __name__=="__main__":
    n=_appium_server()
    n.start_appium_server()
    pid=n.appium_server_status()
    print(pid)