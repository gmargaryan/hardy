import re
import yaml
from netmiko import Netmiko

### Debug output ###

def debug_output(command, pattern, output):
  print ("\ncommand:\n" + command)
  print ("\npattern:\n" + pattern)
  print ("\noutput:\n" + output + "\n")

### Dependecies ####

### Manual ###

def manual(net_connect,host_parameters, debug):
  return (False, "MANUAL")

### Scripts ####


