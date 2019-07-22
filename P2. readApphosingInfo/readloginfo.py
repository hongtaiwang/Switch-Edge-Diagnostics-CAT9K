import sys
import telnetlib
import time
import re


def connectHost(host, psw, userName=None, returnHostName=False):
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

    print("connected!")

    return tn, hostName


# get iox-service info
def readIoxInfo(tn, hostName):
    # sh iox-service
    tn.write("sh iox-service\n".encode('ascii'))
    ioxLog = tn.read_until((hostName + "#").encode('ascii')).decode()
    ioxInfo = dict()
    for info in ioxLog.split('\r\n')[4:]:
        if len(info) < 1:
            break
        ioxInfo[info.split(' :')[0]] = info.split(' :')[1].strip()
    return ioxInfo


# check whether iox running
def checkRunning(ioxInfo):
    for i in ioxInfo:
        if ioxInfo[i] == 'Running':
            continue
        else:
            return False
    return True


# get app-hosting list, will return empty dict if no app on the switch
def readAppList(tn, hostName):
    # sh app list
    tn.write("sh app-hosting list\n".encode('ascii'))
    appList = tn.read_until((hostName + "#").encode('ascii')).decode()
    appListInfo = dict()
    if len(appList.split('\r\n')) < 5:
        return appListInfo
    for i in appList.split('\r\n')[3:]:
        if len(i) < 1:
            break
        appListInfo[re.sub(' +', ' ',i).split(' ')[0].strip()] = re.sub(' +', ' ',i).split(' ')[1].strip()
    return appListInfo


# get app-hosting resource
def readAppRes(tn, hostName):
    # sh app-hosting resource
    tn.write("sh app-hosting resource\n".encode('ascii'))
    appRes = tn.read_until((hostName + "#").encode('ascii')).decode()

    #parse Info
    resInfo = dict()

    if len(appRes.split('\r\n')) < 9:
        return resInfo
    cpuQuota = int(appRes.split('\r\n')[2].split(': ')[1].split('(')[0])
    cpuAvail = int(appRes.split('\r\n')[3].split(': ')[1].split('(')[0])

    memQuota = int(appRes.split('\r\n')[5].split(': ')[1].split('(')[0])
    memAvail = int(appRes.split('\r\n')[6].split(': ')[1].split('(')[0])

    storageQuota = int(appRes.split('\r\n')[8].split(': ')[1].split('(')[0])
    storageAvail = int(appRes.split('\r\n')[9].split(': ')[1].split('(')[0])

    resInfo['CPU'] = [cpuQuota, cpuAvail]
    resInfo['Memory'] = [memQuota, memAvail]
    resInfo['Storage'] = [storageQuota, storageAvail]

    return resInfo

''' functions to fix app-hosting issues
# run IOX
def runIox(tn, hostName):
    tn.write("config term\n".encode('ascii'))
    tn.read_until((hostName + "(config)#").encode('ascii')).decode()
    tn.write("iox\n".encode('ascii'))
    tn.read_until((hostName + "(config)#").encode('ascii')).decode()
    tn.write("end\n".encode('ascii'))
    tn.read_until((hostName + "#").encode('ascii')).decode()
    print('iox is up!\n')
    
    
# run app interface   
def runAppInter(tn, hostName):
    tn.write("config term\n".encode('ascii'))
    tn.read_until((hostName + "(config)#").encode('ascii')).decode()
    tn.write("inter appGigabit1/0/1\n".encode('ascii'))
    tn.read_until((hostName + "(config-if)#").encode('ascii')).decode()
    tn.write("no shutdown\n".encode('ascii'))
    tn.read_until((hostName + "(config-if)#").encode('ascii')).decode()
    tn.write("end\n".encode('ascii'))
    tn.read_until((hostName + "#").encode('ascii')).decode()
    print('app interface is up!\n')
'''



# input as <host> <username> <password>
def main():
    host = sys.argv[1]
    userName = None
    if len(sys.argv) > 3:
        userName = sys.argv[2]
        password = sys.argv[3]
    else:
        password = sys.argv[2]

    # connect to switch
    tn, hostName = connectHost(host, password, userName)

    #get app-hosting info
    appListInfo = readAppList(tn, hostName)
    resInfo = readAppRes(tn, hostName)
    ioxInfo = readIoxInfo(tn, hostName)

    # **remember to close the connection**
    tn.close()

    #use any info if needed

    print("==========app-hosting list==========")
    print(appListInfo)
    print("====================================\n")

    cpuQuota = resInfo['CPU'][0]
    cpuAvail = resInfo['CPU'][1]

    memQuota = resInfo['Memory'][0]
    memAvail = resInfo['Memory'][1]

    storageQuota = resInfo['Storage'][0]
    storageAvail = resInfo['Storage'][1]

    print("===========Resource Info============")
    print("CPU: {}/{}".format(str(cpuAvail), str(cpuQuota)))
    print("Memory: {}/{}".format(str(memAvail), str(memQuota)))
    print("Storage: {}/{}".format(str(storageAvail), str(storageQuota)))
    print("====================================\n")

    # check is all iox services are running
    print("==========Iox service Info==========")
    print("Iox-service running status: ")
    print(checkRunning(ioxInfo))
    print("====================================\n")


if __name__ == "__main__":
    main()