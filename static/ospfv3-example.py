import argparse
import json
import os
from mininet.log import LEVELS, lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config.zebra import StaticRoute, Zebra
from ipmininet.router.config.base import RouterConfig
from ipmininet.iptopo import IPTopo

from mininet.log import lg, logging

"""This file contains a simple network topology"""


class SimpleTopo(IPTopo):

    def build(self, *args, **kwargs):
        """
        The network topology is the following :

        h1-- ra ---- rb ---- re -- h2
              |      |       |
              +----- rc -----+


        """

        #Routers
        ra = self.addRouter_v6('ra', ra_routes)
        rb = self.addRouter_v6('rb', rb_routes)
        rc = self.addRouter_v6('rc', rc_routes)
        re = self.addRouter_v6('re', re_routes)

        #Links
        self.addLink(ra, rb, params1={"ip": "2001:2345:7::a/64"},
                     params2={"ip": "2001:2345:7::b/64"}, igp_metric=5)
        self.addLink(ra, rc, params1={"ip": "2001:2345:4::a/64"},
                     params2={"ip": "2001:2345:4::c/64"})
        self.addLink(rb, rc, params1={"ip": "2001:2345:5::b/64"},
                     params2={"ip": "2001:2345:5::c/64"})
        self.addLink(rb, re, params1={"ip": "2001:2345:6::b/64"},
                     params2={"ip": "2001:2345:6::e/64"}, igp_metric=5)
        self.addLink(rc, re, params1={"ip": "2001:2345:3::c/64"},
                     params2={"ip": "2001:2345:3::e/64"})

        self.addLink(ra, self.addHost('h1'),
                     params1={"ip": "2001:2345:1::a/64"},
                     params2={"ip": "2001:2345:1::1/64"})
        self.addLink(re, self.addHost('h2'),
                     params1={"ip": "2001:2345:2::e/64"},
                     params2={"ip": "2001:2345:2::2/64"})

    def addRouter_v6(self, name):
        return self.addRouter(name, use_v4=False, use_v6=True)

ipmininet.DEBUG_FLAG = True

os.environ["PATH"] += os.pathsep + "/home/vagrant/quagga/bin" + os.pathsep + "/home/vagrant/quagga/sbin"

# Start network
net = IPNet(topo=SimpleTopo(), use_v4=False, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()

