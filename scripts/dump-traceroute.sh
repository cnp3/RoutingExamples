#!/bin/bash

tcpdump -v -i $1 -n '(ip6 && udp) || (icmp6  && (ip6[40] == 1 || ip6[40]==3))'