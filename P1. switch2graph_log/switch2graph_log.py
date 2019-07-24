import sys
import os
import telnetlib
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import time


def readCdpInfo(host, psw, userName=None, returnHostName=False):
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

    # show cdp neighbour
    tn.write("sh cdp neigh\n".encode('ascii'))
    cdpLog = tn.read_until((hostName + "#").encode('ascii')).decode().splitlines()[6:]

    # close connection
    tn.close()

    if returnHostName:
        return cdpLog, hostName
    else:
        return cdpLog


# parse the cdp info into list of [source device, source port, Hold time, Capability, neighbor ID, neighbor Port ID]
def parseCdpInfo(cdpLog):
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
    return cdpInfo


# parse cdpInfo into edges
def processEdges(cdpInfo):
    edges = set()
    edge_attr = dict()
    # process info to edges
    for info in cdpInfo:
        edge = (info[0], info[-2], info[1], info[-1])
        edges.add(edge)
        edge_attr[edge[0], edge[1]] = {edge[2]: edge[3]}
    return edges, edge_attr


# process edges up and down
def updateEdges(edges, edges_cmp, edge_dict):
    edges_up = []
    edges_down = []
    for e in edges_cmp:
        if e not in edges or edge_dict[e] == 0:
            edges_up.append(e)
            edge_dict[e] = 1
    for e in edge_dict:
        if edge_dict[e] == 1 and e not in edges_cmp:
            edges_down.append(e)
            edge_dict[e] = 0
    return edges_up, edges_down, edge_dict


def printInfo(edges, edges_up=[], edges_down=[], fileOuput=False):
    print(str(datetime.datetime.now()) + ': ')
    for e in (edges - set(edges_down)):
        print(e[0] + ":" + e[2] + ' <-> ' + e[1] + ":" + e[3])
    for e in edges_up:
        print(e[0] + ":" + e[2] + ' <-> ' + e[1] + ":" + e[3] + '---up')
    for e in edges_down:
        print(e[0] + ":" + e[2] + ' <-> ' + e[1] + ":" + e[3] + '---down')
    print('\n')
    if fileOuput:
        with open("cdpInfo.txt", "a") as f:
            f.write(str(datetime.datetime.now()) + ': \n')
            for e in edges:
                f.write(e[0] + ":" + e[2] + ' <-> ' + e[1] + ":" + e[3] + '\n')
            for e in edges_up:
                f.write(e[0] + ":" + e[2] + ' <-> ' + e[1] + ":" + e[3] + '---up\n')
            for e in edges_down:
                f.write(e[0] + ":" + e[2] + ' <-> ' + e[1] + ":" + e[3] + '---down\n')
            f.write('\n')


# input as <host> <password> <timeinterval - sec>(static if 0)
def run():
    host = sys.argv[1]
    userName = None
    if len(sys.argv) > 4:
        userName = sys.argv[2]
        password = sys.argv[3]
        timeIntv = int(sys.argv[4])
    else:
        password = sys.argv[2]
        timeIntv = int(sys.argv[3])
    cdpLog = readCdpInfo(host, password, userName)
    cdpInfo = parseCdpInfo(cdpLog)
    edges, edge_attr = processEdges(cdpInfo)

    # build the graph
    G = nx.Graph()
    edge_dict = dict()
    for e in edges:
        edge_dict[e] = 1
        G.add_edge(e[0], e[1])

    # draw graph
    nx.set_edge_attributes(G, edge_attr)

    # drawImage(G)
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos)

    # save file
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('cdp_image_log.png', dpi=100)
    printInfo(edges, fileOuput=True)
    plt.clf()

    # dynamic with time interval
    if timeIntv > 0:
        while True:
            time.sleep(timeIntv)
            cdpLog_cmp = readCdpInfo(host, password, userName)
            try:
                cdpInfo_cmp = parseCdpInfo(cdpLog_cmp)
            except:
                pass
            edges_cmp, edge_attr_cmp = processEdges(cdpInfo_cmp)
            edges_up, edges_down, edge_dict = updateEdges(edges, edges_cmp, edge_dict)

            # print link info
            printInfo(edges, edges_up, edges_down, True)

            # update edge info
            edges = edges_cmp
            edge_attr = edge_attr_cmp

            if len(edges_down) == 0 and len(edges_up) == 0:
                continue

            if len(edges_up):
                for e in edges_up:
                    G.add_edge(e[0], e[1])
                    edge_attr[e[0], e[1]] = {e[2]: e[3]}
                nx.set_edge_attributes(G, edge_attr)
                pos = nx.planar_layout(G)
                nx.draw(G, pos, with_labels=True, font_weight='bold')
                nx.draw_networkx_edge_labels(G, pos)
                nx.draw_networkx_edges(G, pos, edgelist=edges_up, width=4, edge_color='b')
            if len(edges_down):
                pos = nx.planar_layout(G)
                nx.draw(G, pos, with_labels=True, font_weight='bold')
                nx.draw_networkx_edge_labels(G, pos)
                nx.draw_networkx_edges(G, pos, edgelist=edges_down, width=4, edge_color='r')

            fig = plt.gcf()
            fig.set_size_inches(18.5, 10.5)

            fileName = 'cdp_image_log.png'

            # delete previous file if it exists
            if os.path.exists(fileName):
                os.remove(fileName)

            fig.savefig('cdp_image_log.png', dpi=100)
            plt.clf()


if __name__ == "__main__":
    run()
