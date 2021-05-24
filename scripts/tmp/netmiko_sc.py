#!/usr/bin/env python
from netmiko import Netmiko
# from getpass import getpass

def cmd_exec_cisco_ios (host, username, password, command):

  cisco1 = {
      "host": host,
      "username": username,
      "password": password,
      "device_type": "cisco_ios",
  }

  net_connect = Netmiko(**cisco1)

  command = command + '\n'

#  print(net_connect.find_prompt())
  output = net_connect.send_command(command)
  net_connect.disconnect()
  return output
