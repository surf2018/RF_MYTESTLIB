#-*-coding:utf-8-*-
import os
from .keywords import *    #导入已经写好的class
from version import VERSION     #导入已经写好的VERSION

__version__=VERSION    #初始化刚才定义的version

class myTestLibrary(_app_shell,_appium_server,_app_performance):    # 新建个类“myTestLibrary”，adb_shell.py中已经写好的类“Install”
    ROBOT_LIBRARY_SCOPE='GLOBAL'    #此句作用是指该库运行的时候会作用在全局。    # 设置这个类中的关键字全局有效
    ROBOT_LIBRARY_VERSION = VERSION
    def __init__(self):
        for base in myTestLibrary.__bases__:
            base.__init__(self)

