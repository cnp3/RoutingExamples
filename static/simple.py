from mininet.log import lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from ipmininet.router.config.base import RouterConfig
from ipmininet.router.config.zebra import StaticRoute, Zebra

"""

This file contains a simple topology with three routers and three hosts


  a ---- r1  ---- r2 ---- r3  ----  b
                   +
                   c

"""


class SimpleTopo(IPTopo):

    def build(self, *args, **kwargs):
        """
        """
        r1_routes = [StaticRoute("::/0", "2001:89ab:12::2")]
        r3_routes = [StaticRoute("::/0", "2001:89ab:23::1")]
        r2_routes = [StaticRoute("2001:7ab:1::/64", "2001:89ab:12::1"),
                     StaticRoute("2001:7ab:3::/64", "2001:89ab:23::2")]
    
        r1 = self.addRouter_v6('r1', r1_routes)
        r2 = self.addRouter_v6('r2', r2_routes)
        r3 = self.addRouter_v6('r3', r3_routes)

        self.addLink(r1, r2, params1={"ip": "2001:89ab:12::1/64"},
                     params2={"ip": "2001:89ab:12::2/64"})
        self.addLink(r2, r3, params1={"ip": "2001:89ab:23::1/64"},
                     params2={"ip": "2001:89ab:23::2/64"})
        self.addLink(r1, self.addHost('a'),
                     params1={"ip": "2001:7ab:1::1/64"},
                     params2={"ip": "2001:7ab:1::a/64"})
        self.addLink(r2, self.addHost('b'),
                     params1={"ip": "2001:7ab:2::1/64"},
                     params2={"ip": "2001:7ab:2::b/64"})
        self.addLink(r3, self.addHost('c'),
                     params1={"ip": "2001:7ab:3::1/64"},
                     params2={"ip": "2001:7ab:3::c/64"})
        super(SimpleTopo, self).build(*args, **kwargs)

    def addRouter_v6(self, name, staticRoutes):
        return self.addRouter(name, use_v4=False, use_v6=True, config=(RouterConfig, {'daemons': [(Zebra, {"static_routes": staticRoutes})]}))

ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

# Start network
net = IPNet(topo=SimpleTopo(), use_v4=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

