import sys
import telnetlib
import datetime
import time
from collections import defaultdict
import os


class IntrStatus:
    def __init__(self, args=None):
        if args is None:
            self.host = None
            return
        self.host = args[1]
        self.enaPassword = None
        if len(args) > 5:
            self.userName = args[2]
            self.password = args[3] + '\n'
            if args[4] is not None:
                self.enaPassword = args[4] + '\n'
        else:
            self.userName = args[2]
            self.password = args[3] + '\n'
        self.hostName = ""

        self.outputlog = ""
        self.neighborInfo = dict()
        self.powerInfo = defaultdict(list)
        self.powerSummary = []
        self.intStat = dict()
        self.pd_in = dict()

        # dict for interface err info
        # {interface: [[inputqueue], [outputqueue], inputerr, outputerr, collisions, [errstatus]]
        # errSummary - dict{err name: err num}
        # errintr list of interfaces that err exists
        self.errInfo = dict()
        self.errintr = []

        # delete previous file if it exists
        if os.path.exists('./LogInfo.txt'):
            print("removed")
            os.remove('./LogInfo.txt')

    def connectHost(self, host, userName, returnHostName=False):
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
        tn.read_until("Password: ".encode('ascii'))
        tn.write(self.password.encode('ascii'))

        if self.enaPassword is not None:
            # get host name
            hostName = tn.read_until(">".encode('ascii')).decode().split('\r\n')[1].split(">")[0]

            # enable
            tn.write("enable\n".encode('ascii'))
            tn.write(self.enaPassword.encode('ascii'))
            tn.read_until((hostName + "#").encode('ascii'))
        else:
            # get host name
            hostName = tn.read_until("#".encode('ascii')).decode().split('\r\n')[1].split("#")[0]

        self.hostName = hostName
        # term len 0
        tn.write("term len 0\n".encode('ascii'))
        tn.read_until((hostName + "#").encode('ascii'))

        # print("connected!")

        return tn

    # read interface status  dict{interface: status}
    def readIntStat(self, tn):
        tn.write("sh ip inter brief\n".encode('ascii'))
        intInfo = tn.read_until((self.hostName + "#").encode('ascii')).decode()
        intStat = dict()
        for i in intInfo.split('\r\n')[2:-1]:
            intr = i.split()[0]
            if intr[:4] == 'Vlan':
                continue
            intStat[intr] = ' '.join(i.split()[4:-1])
        return intStat

    # read interface errs return a list of
    # [inputqueue overflow, outputqueue overflow, inputerr, outputerr, collisions, summary]
    def readInterErr(self, tn, intr):
        tn.write(("sh inter " + intr + '\n').encode('ascii'))
        intInfo = tn.read_until((self.hostName + "#").encode('ascii')).decode()

        # input queue status
        inputqueue = intInfo.split('Input queue: ')[1].split(' ')[0].split('/')  # size/max/drops/flushes
        inputstat = int(inputqueue[0] >= inputqueue[1] and inputqueue[1])

        # output queue status
        outputqueue = intInfo.split('Output queue: ')[1].split(' ')[0].split('/')  # size/max/drops/flushes
        outputstat = int(outputqueue[0] >= outputqueue[1] and outputqueue[1])

        # input/output/collision err status
        inputErr = int(intInfo.split('input errors')[0].strip().split(' ')[-1])
        outputErr = int(intInfo.split('output errors')[0].strip().split(' ')[-1])
        colErr = int(intInfo.split('collisions')[0].strip().split(' ')[-1])

        summary = inputstat or outputstat or inputErr or outputErr or colErr

        return [inputstat, outputstat, inputErr, outputErr, colErr], summary

    # get pd detected info
    def readPdDetect(self, tn):
        tn.write("sh log\n".encode('ascii'))

        logs = tn.read_until((self.hostName + "#").encode('ascii')).decode()

        pd_in = dict()
        pd_stat = set()
        for l in logs.split('\r\n'):
            tmp = l.split(' ')

            # collect detected devices
            if 'detected:' in tmp:
                tmpi = l.split(":")[-3].strip().split(' ')[-1]
                if tmpi[:2] == 'Gi':
                    tmpi = 'GigabitEthernet' + tmpi[2:]
                pd_in[tmpi] = l.split(":")[-1].strip()

            # check whether sufficient power
            if 'granted' in tmp or 'insufficient' in tmp:
                if len(tmp) > 12:
                    continue
                if 'granted' in tmp:
                    tmpi = l.split(":")[-2].strip().split(' ')[-1]
                    if tmpi[:2] == 'Gi':
                        tmpi = 'GigabitEthernet' + tmpi[2:]
                    pd_stat.add(tmpi)
                else:
                    tmpi = l.split(":")[-3].strip().split(' ')[-1]
                    if tmpi[:2] == 'Gi':
                        tmpi = 'GigabitEthernet' + tmpi[2:]
                    if tmpi in pd_stat:
                        pd_stat.remove(tmpi)
        # remove invalid devices from pd_in
        for i in pd_in:
            if i not in pd_stat:
                pd_in[i] = 'insufficient power'

        return pd_in

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
                if x[0][:2] == 'Gi':
                    x[0] = 'GigabitEthernet' + x[0][2:]
                powerInfo[x[0]] = x[1:]
        return powerSumary, powerInfo

    # grant power
    def grantPower(self, intr):
        tn = self.connectHost(self.host, self.userName)
        tn.write("config term\n".encode('ascii'))
        tn.read_until("(config)#".encode('ascii'))
        tn.write("int {}\n".format(intr).encode('ascii'))
        tn.read_until("(config-if)#".encode('ascii'))
        tn.write("power inline static max 60000\n".encode('ascii'))
        tn.read_until("(config-if)#".encode('ascii'))
        tn.write("sh\n".encode('ascii'))
        tn.read_until("(config-if)#".encode('ascii'))
        tn.write("no sh\n".encode('ascii'))
        tn.read_until("(config-if)#".encode('ascii'))
        tn.write("end\n".encode('ascii'))
        tn.read_until((self.hostName + "#").encode('ascii'))
        tn.close()
        print('power granted!\n')

    # print log
    def printLog(self):
        tn = self.connectHost(self.host, self.userName)
        self.intStat = self.readIntStat(tn)
        self.powerSummary, self.powerInfo = self.readPowerInfo(tn)
        self.pd_in = self.readPdDetect(tn)
        self.errintr = []
        for i in self.intStat:
            errInfo, summary = self.readInterErr(tn, i)
            self.errInfo[i] = errInfo
            if summary:
                self.errintr.append(i)

        tn.close()

        self.outputlog = "\n" + str(datetime.datetime.now()) + ': \n'

        # interface status
        self.outputlog = self.outputlog + "=========Running Interfaces=========\n"

        for i in self.intStat:
            if self.intStat[i] == 'up':
                self.outputlog = self.outputlog + i + '\n'
        self.outputlog = self.outputlog + "==============================\n\n"

        # interface err info
        self.outputlog = self.outputlog + "===========Interface errs==========\n"
        if len(self.errintr) == 0:
            self.outputlog = self.outputlog + "No err exists!\n"
        else:
            for i in self.errintr:
                self.outputlog += "Unexpected err exits on {}, please check!\n".format(i)

        self.outputlog = self.outputlog + "==============================\n\n"

        # pd detected info
        if len(self.pd_in):
            self.outputlog += "=============Pd Info=============\n"
            for i in self.pd_in:
                self.outputlog += i + " : " + self.pd_in[i] + "\n"
            self.outputlog += "==============================\n\n"

        # power info
        self.outputlog = self.outputlog + "============Power Info===========\n"
        self.outputlog = self.outputlog + "Module: " + self.powerSummary[0] + '\n'
        self.outputlog = self.outputlog + "Available: " + self.powerSummary[1] + '\n'
        self.outputlog = self.outputlog + "Used: " + self.powerSummary[2] + '\n'
        self.outputlog = self.outputlog + "Remaining: " + self.powerSummary[3] + '\n'
        self.outputlog = self.outputlog + "------------------------------------------------------\n"

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
        diag = IntrStatus(sys.argv)
        diag.printLog()
        print(diag.outputlog)
    else:
        print("invalid input!")


if __name__ == "__main__":
    main()
