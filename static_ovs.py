from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Controller, OVSKernelSwitch, RemoteController
import networkx as nx


class CustomTopology(Topo):
    def __init__(self, nodes, links):
        Topo.__init__(self)

        self.myNet = nx.DiGraph()
        for n in nodes:
            sName = "s{}".format(n)
            hName = "h{}".format(n)
            hIp, hMac = self.generateIpMac(0, n)
            hEthName = "{}-eth{}".format(hName, 0)
            sEthName = "{}-eth{}".format(sName, 1)
            self.myNet.add_node(sName, eths=[sEthName])
            self.myNet.add_node(hName, eth=hEthName, ip=hIp, mac=hMac)
            self.addSwitch(sName, cls=OVSKernelSwitch)
            self.addHost(hName, ip=hIp + "/24")
            self.myNet.add_edge(sName, hName, eth1=sEthName, eth2=hEthName, 
                                              eth1N=1, eth2N=1, 
                                              ip1=0, ip2=hIp, mac1=0, mac2=hMac)
            self.myNet.add_edge(hName, sName, eth1=hEthName, eth2=sEthName, 
                                              eth1N=1, eth2N=1, 
                                              ip1=hIp, ip2=0, mac1=hMac, mac2=0)
            self.addLink(sName, hName)

        for l in links:
            s1Name = "s{}".format(l[0])
            s2Name = "s{}".format(l[1])
            s1EthNum = len(self.myNet.nodes[s1Name]["eths"])
            s2EthNum = len(self.myNet.nodes[s2Name]["eths"])
            s1EthName = "{}-eth{}".format(s1Name, s1EthNum+1)
            s2EthName = "{}-eth{}".format(s2Name, s2EthNum+1)
            self.myNet.add_edge(s1Name, s2Name, eth1=s1EthName, eth2=s2EthName, 
                                                eth1N=s1EthNum+1, eth2N=s2EthNum+1)
            self.myNet.add_edge(s2Name, s1Name, eth1=s2EthName, eth2=s1EthName, 
                                                eth1N=s2EthNum+1, eth2N=s1EthNum+1)
            self.addLink(s1Name, s2Name)
            self.myNet.nodes[s1Name]["eths"].append(s1EthName)
            self.myNet.nodes[s2Name]["eths"].append(s2EthName)

    def generateIpMac(self, hostId, ethId):
        hostIdHex = hex(hostId)[2:]
        hostIdHex = hostIdHex if len(hostIdHex) == 2 else '0' + hostIdHex
        ethIdHex = hex(ethId)[2:]
        ethIdHex = ethIdHex if len(ethIdHex) == 2 else '0' + ethIdHex
        ip = "10.0.{}.{}".format(hostId, ethId)
        mac = "00:00:00:00:{}:{}".format(hostIdHex, ethIdHex)
        return ip, mac
        

def run(nodes, links, paths):        
    topo = CustomTopology(nodes, links)
    net = Mininet(topo, controller=RemoteController)
    net.start()

    for n in nodes:
        hName = "h{}".format(n)
        eth = topo.myNet.nodes[hName]["eth"]
        mac = topo.myNet.nodes[hName]["mac"]
        macCmd = "ip link set dev {} address {}".format(eth, mac)
        print(hName, macCmd)
        info(net[hName].cmd(macCmd))

    # for n in nodes:
    #     hName = "h{}".format(n)
    #     net[hName].cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
    #     net[hName].cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
    #     net[hName].cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
    #     sName = "s{}".format(n)
    #     net[sName].cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
    #     net[sName].cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
    #     net[sName].cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
    #     net[sName].cmd("ovs-vsctl set bridge {} datapath_type=netdev".format(sName))

    for i in range(len(paths)):
        path1 = paths[i]
        path2 = path1[::-1]
        for path in [path1, path2]:
            print(path)
            srcName = "h{}".format(path[0])
            dstName = "h{}".format(path[-1])
            srcEth = topo.myNet.nodes[srcName]["eth"]
            srcIp = topo.myNet.nodes[srcName]["ip"]
            srcMac = topo.myNet.nodes[srcName]["mac"]
            dstIp = topo.myNet.nodes[dstName]["ip"]
            dstMac = topo.myNet.nodes[dstName]["mac"]
            staticArp = "arp -i {} -s {} {}".format(srcEth, dstIp, dstMac)
            print(srcName, staticArp)
            info(net[srcName].cmd(staticArp))
            for j in range(len(path)-1):
                s1 = path[j]
                s2 = path[j+1]
                s1Name = "s{}".format(s1)
                s2Name = "s{}".format(s2)
                outPort = topo.myNet[s1Name][s2Name]["eth1N"]
                forwardCmd = "ovs-ofctl add-flow {} idle_timeout=0,hard_timeout=0,dl_src={},dl_dst={},actions=output:{}".format(
                    s1Name, srcMac, dstMac, outPort
                )
                print(s1Name, forwardCmd)
                net[s1Name].cmd(forwardCmd) 
            s = path[-1]
            sName = "s{}".format(s)
            forwardCmd = "ovs-ofctl add-flow {} idle_timeout=0,hard_timeout=0,dl_src={},dl_dst={},actions=output:{}".format(
                sName, srcMac, dstMac, 1
            )
            print(sName, forwardCmd)
            net[sName].cmd(forwardCmd) 

            

    # net.pingAll()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel('info')

    #      s1 - s6
    #      |    | 
    # s2 - s3 - s4
    #      |
    #      s5

    nodes = [1, 2, 3, 4, 5, 6]
    links = [
        [1, 6],
        [1, 3],
        [2, 3],
        [3, 4],
        [3, 5],
        [6, 4]
    ]
    paths = [
        [1, 3, 2],
        [1, 3, 5],
    ]

    run(nodes, links, paths)