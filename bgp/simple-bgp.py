import argparse
import json
import os
from mininet.log import LEVELS, lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config.zebra import StaticRoute, Zebra
from ipmininet.iptopo import IPTopo

from ipmininet.router.config import RouterConfig, BGP, iBGPFullMesh, AS, bgp_peering
import ipmininet.router.config.bgp as _bgp


"""This file contains a simple network using BGP"""

class BGPConfig(RouterConfig):
    """A simple config with only a BGP daemon"""
    def __init__(self, node, *args, **kwargs):
        super(BGPConfig, self).__init__(node,
                                        daemons=((BGP, defaults),),
                                        *args, **kwargs)


class SimpleBGP(IPTopo):

    def build(self, *args, **kwargs):
        """
                     h2
                     ||
       h1 = ra ----- rb ----- rd = h4
            |        |
            +------ rc = h3
        """

        # BGP routers

        as1ra = self.bgp('as1ra',['2001:1234:1::/64'])
        as2rb = self.bgp('as2rb',['2001:1234:2::/64'])
        as3rc = self.bgp('as3rc',['2001:1234:3::/64'])
        as4rd = self.bgp('as4rd',['2001:1234:4::/64'])

       # Set AS-ownerships

        self.addOverlay(AS(1, (as1ra,)))
        self.addOverlay(AS(2, (as2rb,)))
        self.addOverlay(AS(3, (as3rc,)))
        self.addOverlay(AS(4, (as4rd,)))

        # Inter-AS links

        self.addLink(as1ra, as2rb,                      
                     params1={"ip": "2001:12::a/64"},
                     params2={"ip": "2001:12::b/64"})
        self.addLink(as1ra, as3rc,                      
                     params1={"ip": "2001:13::a/64"},
                     params2={"ip": "2001:13::c/64"})
        self.addLink(as2rb, as3rc,                      
                     params1={"ip": "2001:23::b/64"},
                     params2={"ip": "2001:23::c/64"})
        self.addLink(as2rb, as4rd,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})

        # Add eBGP peering
        bgp_peering(self, as1ra, as2rb)
        bgp_peering(self, as1ra, as3rc)
        bgp_peering(self, as2rb, as3rc)
        bgp_peering(self, as2rb, as4rd)


        # hosts attached to the routers

        self.addLink(as1ra, self.addHost('h1'),
                     params1={"ip": "2001:1234:1::a/64"},
                     params2={"ip": "2001:1234:1::1/64"})
        self.addLink(as2rb, self.addHost('h2'),
                     params1={"ip": "2001:1234:2::b/64"},
                     params2={"ip": "2001:1234:2::2/64"})
        self.addLink(as3rc, self.addHost('h3'),
                     params1={"ip": "2001:1234:3::c/64"},
                     params2={"ip": "2001:1234:3::1/64"})
        self.addLink(as4rd, self.addHost('h4'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})

        super(SimpleBGP, self).build(*args, **kwargs)

    def bgp(self, name, net=None):
        if net is None:
            net=[]
        return self.addRouter(name, use_v4=True, 
                              use_v6=True, 
                              config=(RouterConfig, 
                                      { 'daemons': [(BGP, 
                                                   { 'address_families': ( _bgp.AF_INET6(networks=net),)} 
#                                                   { 'address_families': ( _bgp.AF_INET6(networks=net,redistribute=('connected',)),)} 
                                                   )]
                                       }
                                      )
                              )


ipmininet.DEBUG_FLAG = True

os.environ["PATH"] += os.pathsep + "/home/vagrant/quagga/bin" + os.pathsep + "/home/vagrant/quagga/sbin"

# Start network
net = IPNet(topo=SimpleBGP(), use_v4=False, use_v6=True, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()

