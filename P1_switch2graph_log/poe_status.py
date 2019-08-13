import sys
import telnetlib
import datetime
import time
from collections import defaultdict
import os

class POEStatus:
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
        self.inputErrInfo = dict()
        self.outputErrInfo = dict()
        self.neighborInfo = dict()
        self.powerInfo = defaultdict(list)
        self.powerSummary = []
        self.intStat = dict()
        self.pd_in = dict()

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

        self.hostName = hostName
        # term len 0
        tn.write("term len 0\n".encode('ascii'))
        tn.read_until((hostName + "#").encode('ascii'))

        #print("connected!")

        return tn

    # read interface status
    def readIntStat(self, tn):
        tn.write("sh ip inter brief\n".encode('ascii'))
        intInfo = tn.read_until((self.hostName + "#").encode('ascii')).decode()
        intStat = dict()
        for i in intInfo.split('\r\n')[2:-1]:
            intStat[i.split()[0]] = ' '.join(i.split()[4:-1])
        return intStat

    # read interface error info
    def readInterErr(self, tn):
        tn.write("sh inter\n".encode('ascii'))
        intInfo = tn.read_until((self.hostName + "#").encode('ascii')).decode()
        inputErrInfo = dict()
        outputErrInfo = dict()
        for i in intInfo.split('input error'):
            if len(i.split('\nGig')) > 1:
                inter = 'Gig' + i.split('Gig')[1].split()[0]
                inputerr = int(i.strip().split()[-1])
                inputErrInfo[inter] = inputerr
        for i in intInfo.split('output error'):
            if len(i.split('\nGig')) > 1:
                inter = 'Gig' + i.split('Gig')[1].split()[0]
                outputerr = int(i.strip().split()[-1])
                outputErrInfo[inter] = outputerr
        return inputErrInfo, outputErrInfo

    # get pd detected info
    def readPdDetect(self, tn):
        tn.write("sh log\n".encode('ascii'))
        logs = tn.read_until((self.hostName + "#").encode('ascii')).decode()
        pd_in = dict()
        for l in logs.split('\r\n'):
            if 'DETECT' in l:
                pd_in[l.split(":")[-3]] = l.split(":")[-1]
        return pd_in

    # get neighbour info
    def readCdpInfo(self, tn):
        # show cdp neighbour
        tn.write("sh cdp neigh\n".encode('ascii'))
        cdpLog = tn.read_until((self.hostName + "#").encode('ascii')).decode().splitlines()[6:]

        cdpLine = []
        cdpInfo = []
        for i in cdpLog:
            if len(i.split()) == 0:
                break
            line = i.split()
            j = 0
            cap = ""
            while j < len(line):
                if len(line[j]) == 1:  # capability
                    cap += line[j] + ' '
                    j += 1
                    continue
                if line[j] == 'IP':
                    j += 1
                    line[j] = 'IP ' + line[j]
                    continue
                if len(cdpLine) == 1 or len(cdpLine) == 5:  # copmbine port field
                    cdpLine.append(line[j] + line[j + 1])
                    j += 2
                else:
                    if len(cap):
                        cdpLine.append(cap)
                        cap = ""
                    cdpLine.append(line[j])
                    j += 1

            # append into cdpInfo
            if len(cdpLine) == 6:
                cdpInfo.append(cdpLine)
                cdpLine = []

        # separate devices with the same name
        deviceNames = dict()
        for i in cdpInfo:
            if (i[-2], i[-1]) in deviceNames:
                deviceNames[(i[-2], i[-1])] += 1
                i[-2] = i[-2] + '-' + str(deviceNames[(i[-2], i[-1])])
            else:
                deviceNames[(i[-2], i[-1])] = 0

        return cdpInfo

    # get power info
    def readPowerInfo(self, tn):
        powerInfo = defaultdict(list)
        powerSumary = ''
        tn.write("sh power inline\n".encode('ascii'))
        powerLog = tn.read_until((self.hostName + "#").encode('ascii')).decode().split('\r\n')
        if (len(powerLog) > 9):
            powerSumary = powerLog[5].split()
            for i in powerLog[9:-1]:
                x = i.split()
                x[4:-2] = [' '.join(x[4:-2])]
                powerInfo[x[0]] = x[1:]
        return powerSumary, powerInfo

    # print log
    def printLog(self):
        tn = self.connectHost(self.host, self.password, self.userName)

        self.intStat = self.readIntStat(tn)
        self.inputErrInfo, self.outputErrInfo = self.readInterErr(tn)
        self.neighborInfo = self.readCdpInfo(tn)
        self.powerSummary, self.powerInfo = self.readPowerInfo(tn)
        self.pd_in = self.readPdDetect(tn)

        tn.close()

        self.outputlog = "\n" + str(datetime.datetime.now()) + ': \n'

        # interface status
        self.outputlog = self.outputlog + "======Running Interfaces======\n"

        for i in self.intStat:
            if self.intStat[i] == 'up':
                self.outputlog = self.outputlog + i + '\n'
        self.outputlog = self.outputlog + "==============================\n\n"

        # interface err info
        self.outputlog = self.outputlog + "========Interface errs========\n"
        errInter = defaultdict(list)
        for i in self.inputErrInfo:
            if self.inputErrInfo[i] == 0 and self.outputErrInfo[i] == 0:
                continue
            else:
                errInter[i].append(self.inputErrInfo[i])
                errInter[i].append(self.outputErrInfo[i])
        if len(errInter) == 0:
            self.outputlog = self.outputlog + " No Errors!\n"
        else:
            for i in errInter:
                self.outputlog = self.outputlog + i + ': '
                self.outputlog = self.outputlog + str(errInter[i][0]) + " input errs and "
                self.outputlog = self.outputlog + str(errInter[i][1]) + " output errs\n\n"
        self.outputlog = self.outputlog + "==============================\n\n"

        # pd detected
        self.outputlog = self.outputlog + "=====Power Device Detected====\n"
        for i in self.pd_in:
            self.outputlog = self.outputlog + i + ': ' + self.pd_in[i] + '\n'
        self.outputlog = self.outputlog + "==============================\n\n"

        # power info
        self.outputlog = self.outputlog + "==========Power Info==========\n"
        self.outputlog = self.outputlog + "Module: " + self.powerSummary[0] + '\n'
        self.outputlog = self.outputlog + "Available: " + self.powerSummary[1] + '\n'
        self.outputlog = self.outputlog + "Used: " + self.powerSummary[2] + '\n'
        self.outputlog = self.outputlog + "Remaining: " + self.powerSummary[3] + '\n'
        self.outputlog = self.outputlog + "------------------------------ \n\n"

        pd = defaultdict(list)
        for i in self.powerInfo:
            if self.powerInfo[i][-3] != 'n/a':
                pd[i] = self.powerInfo[i]
        if len(pd) == 0:
            self.outputlog = self.outputlog + "No Power Device detected!\n"
        else:
            for i in pd:
                self.outputlog = self.outputlog + i + "\nDevice: " + pd[i][-3] + '\n'
                self.outputlog = self.outputlog + 'Admin: ' + pd[i][0] + '    '
                self.outputlog = self.outputlog + 'Power: ' + pd[i][2] + '/' + pd[i][-1] + '\n\n'
        self.outputlog = self.outputlog + "==============================\n\n"

        # write file
        with open("LogInfo.txt", "a") as f:
            f.write(self.outputlog)


# input as <host> <username> <password>
def main():
    if len(sys.argv) is 4 or len(sys.argv) is 5:
        sys.argv.append("0")
        diag = POEStatus(sys.argv)
        diag.printLog()
        print(diag.outputlog)
    else:
        print("invalid input!")


if __name__ == "__main__":
    main()