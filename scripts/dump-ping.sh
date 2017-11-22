#!/bin/bash

tcpdump -v -i $1 -n 'icmp6  && (ip6[40] == 128 || ip6[40]==129)'