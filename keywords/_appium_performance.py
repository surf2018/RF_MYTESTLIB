import sys
sys.path.append("C:\Python27\Lib")
import os
import xlsxwriter
import time
class _app_performance(object):
    """docstring for app_performance"""
    def __init__(self):
        self.__data = {}
        self.__start_time = os.getenv('U_CUSTOM_TEST_TASK_START_TIME',str(int(time.time())))
        # self.__app_package = os.getenv('G_APPIUM_APP_PACKAGE')
        self.__app_package = 'tvunetworks'
        self.__curr_dir = 'D:\\COM_DOC\\robotframwork\\results\\report'
        self.__top = os.getenv('U_TOP_LOG_NAME', 'top.txt')
        self.__meminfo = os.getenv('U_MEMINFO_LOG_NAME', 'meminfo.txt')
        # self.__start_time = str(int(time.time()))
        # self.__app_package = "com.tvunetworks.android.anywhere"
        # self.__curr_dir = 'D:\\COM_DOC\\robotframwork\\results\\report'
        # self.__top = 'top.txt'
        # self.__meminfo = 'meminfo.txt'

    def readTopFile(self, filename=None):
            # Read data from the given file
        cpu = []
        memory = []
        vss = []
        rss = []
        if filename is None:
            filename = os.path.join(self.__curr_dir, self.__top)
        if os.path.exists(filename):
            with open(filename, 'r') as fp:
                lines = fp.readlines()
                for line in lines:
                    if self.__app_package in line:
                        content = line.strip().split()
                        print content
                        if('.' in content[8]):
                            cpu.append(float(content[8]))
                        else:
                            cpu.append(int(content[8]))
                        if('M' in content[5]):
                            vss.append(int(content[5].split('M')[0]))
                        elif('K' in content[5]):
                            vss.append(int(content[5].split('K')[0]))
                        else:
                            vss.append(int(content[5]))
                        if('M' in content[6]):
                            rss.append(int(content[6].split('M')[0]))
                        elif('K' in content[6]):
                            rss.append(int(content[6].split('K')[0]))
                        else:
                            rss.append(int(content[6]))
        self.__data['CPU'] = cpu
        memory.append(vss)
        memory.append(rss)
        self.__data['Memory'] = memory

    def readMeminfoFile(self, filename=None):
        # Read data from the given file
        memory = []
        native_pss = []
        native_private_dirty = []
        native_heap_alloc = []
        dalvik_pss = []
        dalvik_private_dirty = []
        dalvik_heap_alloc = []

        if filename is None:
            filename = os.path.join(self.__curr_dir, self.__meminfo)
        if os.path.exists(filename):
            with open(filename, 'r') as fp:
                lines = fp.readlines()
                for line in lines:
                    if 'Native Heap:' in line:
                        continue
                    elif 'Native Heap' in line:
                        content = line.strip().split()
                        native_pss.append(int(content[2]))
                        native_private_dirty.append(int(content[3]))
                        native_heap_alloc.append(int(content[7]))
                    elif 'Dalvik Heap' in line:
                        content = line.strip().split()
                        dalvik_pss.append(int(content[2]))
                        dalvik_private_dirty.append(int(content[3]))
                        dalvik_heap_alloc.append(int(content[7]))
        memory.append(native_pss)
        memory.append(native_private_dirty)
        memory.append(native_heap_alloc)
        memory.append(dalvik_pss)
        memory.append(dalvik_private_dirty)
        memory.append(dalvik_heap_alloc)
        self.__data['MemoryDetail'] = memory

    def CreateCPUAndMemReport(self, cpu='CPU', mem='Memory', mem_detail=None):
        ''' create usage of phone resources after running app
        Create CPU And Mem Report | mem_detail='MemoryDetail'
        '''
        if mem_detail is not None:
            sheetList = [cpu, mem, mem_detail]
            self.readMeminfoFile()
        elif mem_detail is None:
            sheetList = [cpu, mem]
        self.readTopFile()
        filename = os.path.join(self.__curr_dir, 'appPerformance.xlsx')
        workbook = xlsxwriter.Workbook(filename)
        for sheetName in sheetList:
            print sheetName
            self.createLineChart(workbook, sheetName, self.__data[sheetName])
        workbook.close()

    def createLineChart(self, workbook, sheetName, data):
        items = 1
        worksheet = workbook.add_worksheet(sheetName)
        bold = workbook.add_format({'bold': 1})
        merge_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#D7E4BC',
        })
        if sheetName == 'CPU':
            headings = ['duration', sheetName]
            worksheet.merge_range('A1:{}1'.format(chr(74 + items)), sheetName + self.__start_time, merge_format)
            length = len(data)
            worksheet.write_row('A2', headings, bold)
            worksheet.write_column('A3', xrange(1, length + 1))
            worksheet.write_column('B3', data)
        elif sheetName == 'Memory':
            items += 1
            headings = ['duration', 'VSS', 'RSS']
            worksheet.merge_range('A1:{}1'.format(chr(74 + items)), sheetName + self.__start_time, merge_format)
            length = len(data[0])
            worksheet.write_row('A2', headings, bold)
            worksheet.write_column('A3', xrange(1, length + 1))
            worksheet.write_column('B3', data[0])
            worksheet.write_column('C3', data[1])
        elif sheetName == 'MemoryDetail':
            items += 5
            headings = ['duration', 'Native Pss', 'Native Private Dirty', 'Native Heap Alloc', 'Dalvik Pss',
                        'Dalvik Private Dirty', 'Dalvik Heap Alloc']
            worksheet.merge_range('A1:{}1'.format(chr(74 + items)), sheetName + self.__start_time, merge_format)
            length = len(data[0])
            worksheet.write_row('A2', headings, bold)
            worksheet.write_column('A3', xrange(1, length + 1))
            worksheet.write_column('B3', data[0])
            worksheet.write_column('C3', data[1])
            worksheet.write_column('D3', data[2])
            worksheet.write_column('E3', data[3])
            worksheet.write_column('F3', data[4])
            worksheet.write_column('G3', data[5])

        chart = workbook.add_chart({'type': 'line'})
        for i in xrange(items):
            chart.add_series(
                {
                    # each item define the line chr(66+i) ->(B-G)
                    'name': '={0}!${1}$2'.format(sheetName, chr(66 + i)),
                    'categories': '={0}!$A$3:$A${1}'.format(sheetName, length + 1),
                    'values': '={0}!${1}$3:${1}${2}'.format(sheetName, chr(66 + i), length + 1),
                    'overlap': 10,
                    'line': {
                        'width': 1.25,
                        'dash_type': 'solid',
                    }
                })

        chart.set_title({'name': '{0} Tendency'.format(sheetName)})
        chart.set_x_axis({'name': 'duration'})
        if sheetName == 'CPU':
            chart.set_y_axis({'name': 'capacity (%)'})
        else:
            chart.set_y_axis({'name': 'capacity (K)'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart.set_style(10)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart('{}3'.format(chr(67 + items)), chart)
if __name__=="__main__":
    x=_app_performance()
    x.CreateCPUAndMemReport(mem_detail='MemoryDetail')