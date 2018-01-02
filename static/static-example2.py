from mininet.log import lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from ipmininet.router.config.base import RouterConfig
from ipmininet.router.config.zebra import StaticRoute, Zebra

"""This file contains a simple network topology"""


class SimpleTopo(IPTopo):

    def build(self, *args, **kwargs):
        """
        """

        #Routes 
        ra_routes = [ StaticRoute("::/0", "2001:2345:4::c") ]

        rb_routes = [ StaticRoute("::/0", "2001:2345:5::c") ]

        re_routes = [ StaticRoute("::/0", "2001:2345:3::c") ]

        rc_routes = [ StaticRoute("2001:2345:1::/48", "2001:2345:4::a"),
                      StaticRoute("2001:2345:7::/48", "2001:2345:5::b"),
                      StaticRoute("2001:2345:6::/48", "2001:2345:5::b"),
                      StaticRoute("2001:2345:2::/48", "2001:2345:3::e")
                      ]

        #Routers
        ra = self.addRouter_v6('ra', ra_routes)
        rb = self.addRouter_v6('rb', rb_routes)
        rc = self.addRouter_v6('rc', rc_routes)
        re = self.addRouter_v6('re', re_routes)

        #Links
        self.addLink(ra, rb, params1={"ip": "2001:2345:7::a/64"},
                     params2={"ip": "2001:2345:7::b/64"})
        self.addLink(ra, rc, params1={"ip": "2001:2345:4::a/64"},
                     params2={"ip": "2001:2345:4::c/64"})
        self.addLink(rb, rc, params1={"ip": "2001:2345:5::b/64"},
                     params2={"ip": "2001:2345:5::c/64"})
        self.addLink(rb, re, params1={"ip": "2001:2345:6::b/64"},
                     params2={"ip": "2001:2345:6::e/64"})
        self.addLink(rc, re, params1={"ip": "2001:2345:3::c/64"},
                     params2={"ip": "2001:2345:3::e/64"})

        self.addLink(ra, self.addHost('h1'),
                     params1={"ip": "2001:2345:1::a/64"},
                     params2={"ip": "2001:2345:1::1/64"})
        self.addLink(re, self.addHost('h2'),
                     params1={"ip": "2001:2345:2::e/64"},
                     params2={"ip": "2001:2345:2::2/64"})
        super(SimpleTopo, self).build(*args, **kwargs)

    def addRouter_v6(self, name, staticRoutes):
        return self.addRouter(name, use_v4=False, use_v6=True, config=(RouterConfig, {'daemons': [(Zebra, {"static_routes": staticRoutes})]}))

ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

# Start network
net = IPNet(topo=SimpleTopo(), use_v4=False, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()

