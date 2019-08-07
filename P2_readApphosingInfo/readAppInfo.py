import sys
import telnetlib
import datetime
import time
import re
import os

class AppHosting:
    def __init__(self, args=None):
        if args is None:
            self.host = None
            return
        self.host = args[1]
        self.enaPassword = None

        if len(args) > 5:
            self.userName = args[2]
            self.password = args[3]
            self.enaPassword = args[4]
        else:
            self.userName = args[2]
            self.password = args[3]

        self.hostName = ""
        self.outputlog = ""
        self.appListInfo = dict()
        self.resInfo = dict()
        self.ioxInfo = dict()

        # delete previous file if it exists
        if os.path.exists('./LogInfo.txt'):
            print("removed")
            os.remove('./LogInfo.txt')

    def connectHost(self, host, psw, userName, returnHostName=False):
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
        tn.read_until("Username: ".encode('ascii'))
        userName += '\n'
        tn.write(userName.encode('ascii'))

        # input password
        password = psw + '\n'
        tn.read_until("Password: ".encode('ascii'))
        tn.write(password.encode('ascii'))

        if self.enaPassword is not None:
            # get host name
            hostName = tn.read_until(">".encode('ascii')).decode().split('\r\n')[1].split(">")[0]

            # enable
            tn.write("enable\n".encode('ascii'))
            tn.read_until("Password: ".encode('ascii'))
            self.enaPassword = self.enaPassword + '\n'
            tn.write(self.enaPassword.encode('ascii'))
            tn.read_until((hostName + "#").encode('ascii'))
        else:
            # get host name
            hostName = tn.read_until("#".encode('ascii')).decode().split('\r\n')[1].split("#")[0]

        # term len 0
        tn.write("term len 0\n".encode('ascii'))
        tn.read_until((hostName + "#").encode('ascii'))

        #print("connected!")

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
    def checkApp(self):
        if len(self.appListInfo) == 0:
            return True
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

        i = 0
        while i < len(appRes.split('\r\n')):
            if appRes.split('\r\n')[i] == "CPU:":
                i += 1
                cpuQuota = int(appRes.split('\r\n')[i].split(': ')[1].split('(')[0])
                i += 1
                cpuAvail = int(appRes.split('\r\n')[i].split(': ')[1].split('(')[0])
            elif appRes.split('\r\n')[i] == "Memory:":
                i += 1
                memQuota = int(appRes.split('\r\n')[i].split(': ')[1].split('(')[0])
                i += 1
                memAvail = int(appRes.split('\r\n')[i].split(': ')[1].split('(')[0])
            elif appRes.split('\r\n')[i] == "Storage space:":
                i += 1
                storageQuota = int(appRes.split('\r\n')[i].split(': ')[1].split('(')[0])
                i += 1
                storageAvail = int(appRes.split('\r\n')[i].split(': ')[1].split('(')[0])
            i += 1

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
            for i in self.appListInfo:
                self.outputlog = self.outputlog + i + ' : '
                self.outputlog = self.outputlog + self.appListInfo[i] + '\n'
        else:
            self.outputlog = self.outputlog + "no app is running!\n"
        self.outputlog = self.outputlog + "==============================\n\n"

        # app-interface
        self.outputlog = self.outputlog + "============app interface==========\n"
        if self.checkAppInter():
            self.outputlog = self.outputlog + "Up!\n"
        else:
            self.outputlog = self.outputlog + "Down!\n"
        self.outputlog = self.outputlog + "==============================\n\n"
        with open("LogInfo.txt", "a") as f:
            f.write(self.outputlog)


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

    # check app interface status
    def checkAppInter(self):
        tn = self.connectHost(self.host, self.password, self.userName)
        tn.write("sh ip interface br\n".encode('ascii'))
        log = tn.read_until((self.hostName + "#").encode('ascii')).decode().split("\r\n")
        tn.close()
        print("read:\n")
        print(log)
        for i in log:
            if i[:2] == "Ap":
                return i.split()[-2] == "up"

    # run app interface
    def runAppInter(self):
        tn = self.connectHost(self.host, self.password, self.userName)
        tn.write("config term\n".encode('ascii'))
        tn.read_until("(config)#".encode('ascii'))
        tn.write("inter appGigabit1/0/1\n".encode('ascii'))
        tn.read_until("(config-if)#".encode('ascii'))
        tn.write("no shutdown\n".encode('ascii'))
        tn.read_until("(config-if)#".encode('ascii'))
        tn.write("end\n".encode('ascii'))
        tn.read_until((self.hostName + "#").encode('ascii'))
        print('app interface is up!\n')
        tn.close()


# input as <host> <username> <password>
def main():
    if len(sys.argv) is 4 or len(sys.argv) is 5:
        sys.argv.append("0")
        diag = AppHosting(sys.argv)
        diag.printLog()
        print(diag.outputlog)
    else:
        print("invalid input!")


if __name__ == "__main__":
    main()