import sys
import telnetlib
import datetime
import time
import re


class AppHosting:
    def __init__(self, args=None):
        if args is None:
            self.host = None
            return
        self.host = args[1]
        self.userName = None
        if len(args) > 4:
            self.userName = args[2]
            self.password = args[3]
        else:
            self.password = args[2]
        self.hostName = ""
        self.outputlog = ""
        self.appListInfo = dict()
        self.resInfo = dict()
        self.ioxInfo = dict()

    def connectHost(self, host, psw, userName=None):
        # connect to switch
        while True:
            try:
                tn = telnetlib.Telnet(host, timeout=5)
                break
            except:
                print('failed to connect! retry in 2 sec')
                time.sleep(2)
                pass

        # input username, if any
        if userName is not None:
            tn.read_until("Username: ".encode('ascii'))
            userName += '\n'
            tn.write(userName.encode('ascii'))

        # input password
        password = psw + '\n'
        tn.read_until("Password: ".encode('ascii'))
        tn.write(password.encode('ascii'))

        if userName is None:
            # get host name
            hostName = tn.read_until(">".encode('ascii')).decode().split('\r\n')[1].split(">")[0]

            # enable
            tn.write("enable\n".encode('ascii'))
            tn.read_until("Password: ".encode('ascii'))
            tn.write(password.encode('ascii'))
            tn.read_until((hostName + "#").encode('ascii'))
        else:
            # get host name
            hostName = tn.read_until("#".encode('ascii')).decode().split('\r\n')[1].split("#")[0]

        # term len 0
        tn.write("term len 0\n".encode('ascii'))
        tn.read_until((hostName + "#").encode('ascii'))

        self.hostName = hostName
        # print("connected!")
        return tn


    # get iox-service info
    def readIoxInfo(self, tn):
        # sh iox-service
        tn.write("sh iox-service\n".encode('ascii'))
        ioxLog = tn.read_until((self.hostName + "#").encode('ascii')).decode()
        self.ioxInfo = dict()
        for info in ioxLog.split('\r\n')[4:]:
            if len(info) < 1:
                break
            self.ioxInfo[info.split(' :')[0]] = info.split(' :')[1].strip()
        return self.ioxInfo

    # check whether iox running
    def checkRunning(self):
        for i in self.ioxInfo:
            if self.ioxInfo[i] == 'Running':
                continue
            else:
                return False
        return True

    # check whether app is running
    def checkAppg(self):
        for i in self.appListInfo:
            if self.appListInfo[i] == 'Running':
                continue
            else:
                return False
        return True

    # get app-hosting list, will return empty dict if no app on the switch
    def readAppList(self, tn):
        # sh app list
        tn.write("sh app-hosting list\n".encode('ascii'))
        appList = tn.read_until((self.hostName + "#").encode('ascii')).decode()
        if len(appList.split('\r\n')) < 5:
            return self.appListInfo
        for i in appList.split('\r\n')[3:]:
            if len(i) < 1:
                break
            self.appListInfo[re.sub(' +', ' ', i).split(' ')[0].strip()] = re.sub(' +', ' ', i).split(' ')[1].strip()
        return self.appListInfo

    # get app-hosting resource
    def readAppRes(self, tn):
        # sh app-hosting resource
        tn.write("sh app-hosting resource\n".encode('ascii'))
        appRes = tn.read_until((self.hostName + "#").encode('ascii')).decode()

        # parse Info
        resInfo = dict()

        if len(appRes.split('\r\n')) < 9:
            return resInfo
        cpuQuota = int(appRes.split('\r\n')[2].split(': ')[1].split('(')[0])
        cpuAvail = int(appRes.split('\r\n')[3].split(': ')[1].split('(')[0])

        memQuota = int(appRes.split('\r\n')[5].split(': ')[1].split('(')[0])
        memAvail = int(appRes.split('\r\n')[6].split(': ')[1].split('(')[0])

        storageQuota = int(appRes.split('\r\n')[8].split(': ')[1].split('(')[0])
        storageAvail = int(appRes.split('\r\n')[9].split(': ')[1].split('(')[0])

        self.resInfo['CPU'] = [cpuQuota, cpuAvail]
        self.resInfo['Memory'] = [memQuota, memAvail]
        self.resInfo['Storage'] = [storageQuota, storageAvail]

        return self.resInfo

    # print log
    def printLog(self):
        tn = self.connectHost(self.host, self.password, self.userName)
        self.readAppList(tn)
        self.readAppRes(tn)
        self.readIoxInfo(tn)
        tn.close()

        self.outputlog = "\n" + str(datetime.datetime.now()) + ': \n'

        # iox info
        self.outputlog = self.outputlog + "==========Iox service Info==========\n"
        self.outputlog = self.outputlog + "Iox-service running status: \n"
        for i in self.ioxInfo:
            self.outputlog = self.outputlog + i + " : " + self.ioxInfo[i] + "\n"
        self.outputlog = self.outputlog + "==============================\n\n"

        # check if iox is running
        if self.resInfo:
            # app-hosting resource info
            cpuQuota = self.resInfo['CPU'][0]
            cpuAvail = self.resInfo['CPU'][1]

            memQuota = self.resInfo['Memory'][0]
            memAvail = self.resInfo['Memory'][1]

            storageQuota = self.resInfo['Storage'][0]
            storageAvail = self.resInfo['Storage'][1]

            self.outputlog = self.outputlog + "===========Resource Info==========\n"
            self.outputlog = self.outputlog + "CPU: {}/{}\n".format(str(cpuAvail), str(cpuQuota))
            self.outputlog = self.outputlog + "Memory: {}/{}\n".format(str(memAvail), str(memQuota))
            self.outputlog = self.outputlog + "Storage: {}/{}\n".format(str(storageAvail), str(storageQuota))
            self.outputlog = self.outputlog + "==============================\n\n"

        else:
            self.outputlog = self.outputlog + "===========Resource Info==========\n"
            self.outputlog = self.outputlog + "warning! iox is not running!\n"
            self.outputlog = self.outputlog + "==============================\n\n"

        # app-hosting list
        self.outputlog = self.outputlog + "==========app-hosting list==========\n"
        if len(self.appListInfo):
            self.outputlog = self.outputlog + self.appListInfo
        else:
            self.outputlog = self.outputlog + "no app is running!\n"
        self.outputlog = self.outputlog + "==============================\n\n"

    # run IOX
    def runIox(self):
        tn = self.connectHost(self.host, self.password, self.userName)
        tn.write("config term\n".encode('ascii'))
        tn.read_until("(config)#".encode('ascii'))
        tn.write("iox\n".encode('ascii'))
        tn.read_until("(config)#".encode('ascii'))
        tn.write("end\n".encode('ascii'))
        tn.read_until((self.hostName + "#").encode('ascii'))
        tn.close()
        print('iox is up!\n')


    # run app interface
    def runAppInter(self):
        tn = self.connectHost(self.host, self.password, self.userName)
        tn.write("config term\n".encode('ascii'))
        tn.read_until((self.hostName + "(config)#").encode('ascii')).decode()
        tn.write("inter appGigabit1/0/1\n".encode('ascii'))
        tn.read_until((self.hostName + "(config-if)#").encode('ascii')).decode()
        tn.write("no shutdown\n".encode('ascii'))
        tn.read_until((self.hostName + "(config-if)#").encode('ascii')).decode()
        tn.write("end\n".encode('ascii'))
        tn.read_until((self.hostName + "#").encode('ascii')).decode()
        print('app interface is up!\n')
        tn.close()


# input as <host> <username> <password>
def main():
    diag = AppHosting(sys.argv)
    diag.printLog()
    print(diag.outputlog)


if __name__ == "__main__":
    main()