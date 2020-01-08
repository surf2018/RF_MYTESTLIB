import sys
sys.path.append("C:\Python27\Lib")
import os
import time
class _app_shell(object):
    def __init__(self):
        self.__device_name = os.getenv('U_APPIUM_DEVICE_NAME')
        self.__adb_start_server = "adb start-server"
        self.__adb_kill_server = "adb kill-server"
        # Default Log Path:
        self.__curr_dir = os.getenv('G_CURRENTLOG', 'D:\\COM_DOC\\robotframwork\\logs\\current')
        self.__bug_report_dir = 'D:\\COM_DOC\\robotframwork\\logs\\current'
        self.__chkbug_report_dir = os.getenv('G_APPIUM_APP_BUGREPORT_DIR', 'D:\\COM_DOC\\robotframwork\\tools\\bugreport')
        self.__duration=2
        self.__report_dir = 'D:\\COM_DOC\\robotframwork\\results\\report'
        self.__appPackage = os.getenv('G_APPIUM_APP_PACKAGE')

    def __raiseError(self, Message=None):
        # Raise Exception with self-defined message.
        raise Exception, Message

    def kill_adb_process(self):
        """
        Kill ADB Process.
        Examples:
        | Kill Adb Process |
        """
        try:
            rc = self.check_adb_status()
            if rc == True:
                status = os.system('taskkill /f /im adb.exe')
                if status == 0:
                    print 'Pass! Killed ADB Process.'
                else:
                    self.__raiseError('Fail! Could NOT kill ADB Process.')
            else:
                print 'ADB process is already stopped.'
        except Exception as e:
            print str(e)

    def check_adb_status(self):
        """
        Check ADB Status.
        Examples:
        | ${status} | Check Adb Status |
        """
        try:
            content = os.popen('tasklist | findstr adb.exe')
            if 'adb.exe' in content:
                return True
            else:
                return False
        except Exception as e:
            print str(e)

    def start_adb_service(self):
        """
        Start ADB Service.
        Examples:
        | Start Adb Serivce |
        """
        try:
            text = os.popen(self.__adb_start_server)
            time.sleep(3)
            content = text.read()
            print content
            if '5037' not in content:
                self.__raiseError('Error: start ADB server failed. %s' % content)
            else:
                print 'Pass! ADB server started.'
        except Exception, e:
            print str(e)

    def get_device_name(self):
        """
        Get Devices Name through ADB command.
        Examples:
        | ${device_name} | Get Adb Devices |
        """
        device_name = ''
        adb_devices = "adb devices"
        try:
            text = os.popen(adb_devices)
            time.sleep(3)
            content = text.read().strip()
            print content
            res = content.splitlines()
            if 'device' not in content:
                self.__raiseError('Error: Could Not get device -> {}'.format(res[-1].split()[1]))
            device_name = res[-1].split()[0]
        except Exception, e:
            if str(e) == 'list index out of range':
                self.__raiseError(
                    'Error: Could NOT find device! Please check the phone has been attached to TestBed.')
            else:
                print str(e)
        return device_name

    def set_device_name(self, name=None):
        """
        Set Devices Name after get its name through ADB command.
        Examples:
        | Set Device Name |
        """
        if name == None:
            deviceName = self.get_device_name()
        else:
            deviceName = name
        if self.__device_name != '' and self.__device_name == deviceName:
            print '-' * 30
            print 'Pass! Set device name!'
            print 'Device Name:' + self.__device_name
            print '-' * 30
        elif deviceName == '':
            self.__raiseError('FAIL: Could NOT get device name!')
        else:
            self.__device_name = deviceName
            os.environ['U_APPIUM_DEVICE_NAME'] = str(deviceName)
            print '-' * 30
            print 'Pass! Set device name!'
            print 'Device Name: ' + os.getenv('U_APPIUM_DEVICE_NAME')
            print '-' * 30

    def adb_install_package(self, apk=None, package_name=None):
        """
        Install packages through ADB command.
        Examples:
        |     Adb Install Package    | ${apk_name} | ${package_name} |
        """
        if apk == None:
            apk = os.getenv('G_APPIUM_APP_APK')
        else:
            apk = os.path.join(os.getenv('G_APPIUM_APP_DIR'), apk)

        if package_name == None:
            package_name = os.getenv('G_APPIUM_APP_PACKAGE')
        if self.is_package_installed(package_name):
            self.adb_uninstall_package(package_name)
        try:
            cmd = 'adb -s {} install {}'.format(os.getenv('U_APPIUM_DEVICE_NAME'), apk)
            print cmd
            text = os.popen(cmd)
            content = text.read()
            print content
            if 'Success' in content:
                print
                'Pass: Install {} succeeded. \nVersion: {}'.format(package_name, apk)
            else:
                self.__raiseError('Fail: Could NOT intall {}'.format(package_name))
        except Exception, e:
            print
            str(e)


    def adb_uninstall_package(self, package_name=None):
        """
        Uninstall packages through ADB command.
        Examples:
        |    Adb Uninstall Package    | ${package_name} |
        """
        if package_name == None:
            package_name = os.getenv('G_APPIUM_APP_PACKAGE')
        if not self.is_package_installed(package_name):
            self.__raiseError('Fail: APP {} is not installed.'.format(package_name))
        try:
            cmd = 'adb -s {} uninstall {}'.format(os.getenv('U_APPIUM_DEVICE_NAME'), package_name)
            print cmd
            text = os.popen(cmd)
            content = text.read()
            print content
            if 'Success' in content:
                print
                'Pass: Uninstall {} succeeded.'.format(package_name)
            else:
                self.__raiseError('Fail: Could NOT unintall {}'.format(package_name))
        except Exception as e:
            print
            str(e)


    def is_package_installed(self, package_name):
        """
        Check target package is installed through ADB command.
        Examples:
        | ${status} | Is Package Installed |
        """
        packages = self.get_third_party_packages()
        if package_name in packages:
            return True
        else:
            return False


    def get_third_party_packages(self):
        """
        Get Third-party packages through ADB command.
        Examples:
        | ${apk_name} | Get Third Party Packages |
        """
        apks = []
        try:
            f = os.popen('adb shell pm list package -3')
            for x in f.readlines():
                apks.append(x.strip().split(':')[1])
            return apks
        except Exception, e:
            print str(e)
    def top(self,duration=None):
        filename = os.path.join(self.__report_dir, os.getenv('U_TOP_LOG_NAME'))
        # filename="d:\\1.txt"
        print filename
        if duration is None:
            duration = self.__duration
        top_cmd = 'start /b adb shell top -d {} >>{}'.format(duration, filename)
        print top_cmd
        try:
            os.popen(top_cmd)
            print 'Pass! adb top is running...'
        except Exception as e:
            print str(e)

    def meminfo(self, package=None):
        filename = os.path.join(self.__report_dir, os.getenv('U_MEMINFO_LOG_NAME'))
        if package is None:
            package = self.__appPackage
        meminfo = 'start /b adb shell dumpsys meminfo {} >>{}'.format(package, filename)
        print meminfo
        try:
            os.popen(meminfo)
        except Exception as e:
            print str(e)

if __name__=="__main__":
    xx=_app_shell()
    xx.top(2)