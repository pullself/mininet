from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class SingleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost('h%s' % (h + 1), cpu=.5/n)
            # 100 Mbps, 5ms delay, 1% Loss, 1000 packet queue
            self.addLink(host, switch, bw=100, delay='5ms', loss=1,
                         max_queue_size=1000, use_htb=True)


def perfTest():
    topo = SingleSwitchTopo(n=6)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    print "Testing bandwidth between h1 and h6"
    h1, h6 = net.get('h1', 'h6')
    net.iperf((h1, h6))
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
