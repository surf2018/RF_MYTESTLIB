import sys
sys.path.append("C:\Python27\Lib")
import os
import time
from ftplib import FTP
class _myFunction(object):
    """some function"""

    def sum_duration(self,duration):
        """
         count the duration of local video.
        Examples:
            | ${seconds} | Sum Duration | ${duration}|"""
        # print duration
        timeArray=duration.strip().split(':')
        if(len(timeArray)==3):
            h,m,s=duration.strip().split(':')
            seconds=int(h) * 3600 + int(m) * 60 + int(s)
        else:
            m, s = duration.strip().split(':')
            seconds = int(m) * 60 + int(s)
        return seconds


#
# if __name__=="__main__":
#
#     n=_myFunction()
#     ss=n.sum_duration("01:27")
#     print ss