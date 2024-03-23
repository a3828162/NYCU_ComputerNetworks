from mininet.net import Mininet
import sys
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.topo import Topo

class Lab2_Topo( Topo ):
    def __init__( self ):
        Topo.__init__( self )
        
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )
        h6 = self.addHost( 'h6' )
        h7 = self.addHost( 'h7' )
        h8 = self.addHost( 'h8' )
        h9 = self.addHost( 'h9' )
        
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )

        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        self.addLink( s1, s2 )
        self.addLink( s2, h3 )
        self.addLink( s2, s3 )
        self.addLink( s3, h4 )
        self.addLink( s3, h5 )
        self.addLink( s1, s4 )
        self.addLink( s4, h6 )
        self.addLink( s4, s5 )
        self.addLink( s5, h7 )
        self.addLink( s5, s6 )
        self.addLink( s6, h8 )
        self.addLink( s6, h9 )

def runIperf(net:Mininet, iperf_session:dict, duration=10):
    print("Starting iperf session from {} to {} with bandwidth limit {} Mbps".format(
        iperf_session['src'], iperf_session['dst'], iperf_session['bw_limit']))
    # TODO (runIperf function)
    client, server = net.get(iperf_session['src'], iperf_session['dst'])
    
    server.cmd( 'killall -9 iperf' )
    client.cmd( 'killall -9 iperf' )

    server.cmd("iperf -s -D")
    print(client.cmd("iperf -c %s -b %sMb" % (server.IP(), iperf_session['bw_limit'])))


def createTopo():
    topos = Lab2_Topo()
    
    net = Mininet(topo=topos, controller=None, switch=OVSSwitch, link=TCLink)
    
    REMOTE_CONTROLLER_IP = "127.0.0.1"
    net.addController("c0",
                      controller=RemoteController,
                      ip=REMOTE_CONTROLLER_IP,
                      port=6653)
    
    # TODO (Generate Topology)

    print("Starting network")
    net.start()

    # TODO (Set up iperf sessions)
    iperf_session1 = dict(src='h1',dst='h2',bw_limit=5)
    iperf_session2 = dict(src='h1',dst='h3',bw_limit=10)
    iperf_session3 = dict(src='h4',dst='h5',bw_limit=15)
    iperf_session4 = dict(src='h6',dst='h8',bw_limit=20)

    runIperf(net, iperf_session1, 10)
    runIperf(net, iperf_session2, 10)
    runIperf(net, iperf_session3, 10)
    runIperf(net, iperf_session4, 10)

    print("Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    createTopo()
