from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class DoubleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch("s2")
        self.addLink(switch1, switch2, bw=10, delay='5ms',
                     loss=0, max_queue_size=1000, use_htb=True)
        for h in range(n/2):
            host = self.addHost('h%s' % (h + 1), cpu=.5/n)
            self.addLink(host, switch1, bw=10, delay='5ms', loss=0,
                         max_queue_size=1000, use_htb=True)
        for h in range(n/2, n):
            host = self.addHost('h%s' % (h + 1), cpu=.5/n)
            self.addLink(host, switch2, bw=10, delay='5ms', loss=0,
                         max_queue_size=1000, use_htb=True)


def perfTest():
    topo = DoubleSwitchTopo(n=6)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h3"
    h1, h3 = net.get('h1', 'h3')
    net.iperf((h1, h3))
    print "Testing bandwidth between h4 and h6"
    h4, h6 = net.get('h4', 'h6')
    net.iperf((h4, h6))
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
