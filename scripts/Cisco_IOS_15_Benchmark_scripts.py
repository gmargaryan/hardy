import re
import yaml
from netmiko import Netmiko


### Debug output ###

def debug_output(command, pattern, output):
  print ("\ncommand:\n" + command)
  print ("\npattern:\n" + pattern)
  print ("\noutput:\n" + output + "\n")

### Manual ###

def manual(net_connect,host_parameters, debug):
  return (False, "MANUAL")

### Dependecies ####

def if_eigrp_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO EIGRP"

  command_1 = "sh run | sec router eigrp"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # compare output with pattern
  match_1 = re.search(pattern_1, output_str_1)
  if match_1:
    result = True
    message = ""
  return (result, message)

def if_ospf_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO OSPF"

  command_1 = "sh run | sec router ospf"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # compare output with pattern
  match_1 = re.search(pattern_1, output_str_1)
  if match_1:
    result = True
    message = ""
  return (result, message)

def if_bgp_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO BGP"

  command_1 = "sh run | sec router bgp"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # compare output with pattern
  match_1 = re.search(pattern_1, output_str_1)
  if match_1:
    result = True
    message = ""
  return (result, message)

def if_rip_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO RIP"

  command_1 = "sh run | sec router rip"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # compare output with pattern
  match_1 = re.search(pattern_1, output_str_1)
  if match_1:
    result = True
    message = ""
  return (result, message)


### Scripts ####


def Create_acl_for_use_with_line_vty(net_connect,host_parameters, debug):
    
  result = False  

  command_1 = "show conf | sec line vty"
  pattern_1 = "access-class (\w+) in"

  command_2_without_acl_name = "show ip access-list %s"
  pattern_2 = ".+"
 
  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # compare output with pattern
  match_1 = re.search(pattern_1, output_str_1)
  if match_1:
    acl_name = match_1.group(1)
    command_2 = command_2_without_acl_name % acl_name
    output_str_2 = net_connect.send_command(command_2 ) 
    if debug:
      debug_output(command_2, pattern_2, output_str_2)
    else:
      pass
    match_2 = re.search(pattern_2, output_str_2)
    if match_2:
      result = True
  return (result, "")


def Create_an_acl_for_use_with_SNMP(net_connect,host_parameters, debug):

  result = False

  command_1 = "show conf | sec snmp-server community"
  pattern_1 = "snmp-server community .* R[OW] (\w+)"

  command_2_without_acl_name = "show ip access-list %s"
  pattern_2 = ".+"

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      acl_name = match_1.group(1)
      command_2 = command_2_without_acl_name % acl_name
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        result = False
        break
  return (result, "")


def Set_no_ip_proxy_arp(net_connect,host_parameters, debug):
  result = False
  message = "NO INT"

  command_1 = "sh ip interface brief | incl Eth|eth"
  pattern_1 = "^(\w+[0-9/.]+)\s+[0-9.]+\s+YES.*"

  command_2_without_int_name = "sh run int %s | incl proxy-arp"
  pattern_2 = "no ip proxy-arp"

  interface = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = False
      message = ""
      interface = match_1.group(1)
      command_2 = command_2_without_int_name % interface
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)

def Set_ip_verify_unicast_source_reachable_via(net_connect,host_parameters, debug):
  command_without_int = "sh ip int %s | incl verify source"
  pattern = ".+"
  result = True
  for interface in host_parameters['interfaces']['untrust']:
    if (interface['name']):
      command = command_without_int % interface['name']
      output_str = net_connect.send_command(command)
      if debug:
        debug_output(command, pattern, output_str)
      else:
        pass
      match = re.search(pattern, output_str)
      if not(match):
        result = False
        break
      else:
        pass
  if result:
    for interface in host_parameters['interfaces']['internet']:
      if (interface['name']):
        command = command_without_int % interface['name']
        output_str = net_connect.send_command(command)
        if debug:
          debug_output(command, pattern, output_str)
        else:
          pass
        match = re.search(pattern, output_str)
        if not(match):
          result = False
          break
        else:
          pass
  if result:
    for interface in host_parameters['interfaces']['dmz']:
      if (interface['name']):
        command = command_without_int % interface['name']
        output_str = net_connect.send_command(command)
        if debug:
          debug_output(command, pattern, output_str)
        else:
          pass
        match = re.search(pattern, output_str)
        if not(match):
          result = False
          break
        else:
          pass
  return (result, "")

def Set_ip_acl_extended_to_Forbid_Private_Source_Addresses_from_External_Networks(net_connect,host_parameters, debug):
  return (False, "MANUAL")

def Set_inbound_ip_access_group_on_the_External_Interface(net_connect,host_parameters, debug):
  return (False, "MANUAL")

def Set_ip_authentication_key_chain_eigrp(net_connect,host_parameters, debug):
  result = False
  message = "NO INT"

  command_1 = "sh ip eigrp interfaces | excl Vi|Lo"
  pattern_1 = "^(\w+[0-9/.]+)\s+.+"

  command_2_without_int_name = "sh run int %s | incl key-chain"
  pattern_2 = "ip authentication key-chain eigrp "

  interface = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if (match_1):
      result = False
      message = ""
      interface = match_1.group(1)
      command_2 = command_2_without_int_name % interface
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)

def Set_ip_authentication_mode_eigrp(net_connect,host_parameters, debug):

  result = False
  message = "NO INT"

  command_1 = "sh ip eigrp interfaces | excl Vi|Lo"
  pattern_1 = "^(\w+[0-9/.]+)\s+.+"

  command_2_without_int_name = "sh run int %s | incl authentication mode"
  pattern_2 = "ip authentication mode eigrp .+ "

  interface = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = False
      message = ""
      interface = match_1.group(1)
      command_2 = command_2_without_int_name % interface
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)

def Set_authentication_message_digest_for_OSPF_area(net_connect,host_parameters, debug):

  result = False
  message = "NO INT"

  command_1 = "sh ip ospf interface brief | excl Vi|Lo"
  pattern_1 = "^\w+[0-9/.]+\s+\d+\s+(\d+)\s+.+"

  command_2 = "sh run | sec router ospf "
  pattern_2_without_area_name = "area %s authentication message-digest"

  area = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = False
      message = ""
      area = match_1.group(1)
      pattern_2 = pattern_2_without_area_name % area
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)


def Set_ip_ospf_message_digest_key_md5(net_connect,host_parameters, debug):


  result = False
  message = "NO INT"

  command_1 = "sh ip ospf interface brief | excl Vi|Lo"
  pattern_1 = "^(\w+[0-9/.]+)\s+\d+\s+\d+\s+.+"

  command_2_without_int_name = "sh run int %s | incl ip ospf message-digest-key"
  pattern_2 = "ip ospf message-digest-key \d+ md5 .+"

  interface = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = False
      message = ""
      interface = match_1.group(1)
      command_2 = command_2_without_int_name % interface
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)

def Set_ip_rip_authentication_key_chain(net_connect,host_parameters, debug):

  result = False
  message = "NO INT"

  command_1 = "sh ip protocols | sec rip"
  pattern_1 = "\s+(\w+[0-9/.]+)\s+[12]"

  command_2_without_int_name = "sh run int %s | incl ip rip authentication key-chain"
  pattern_2 = "ip rip authentication key-chain .+"

  interface = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if (match_1 and not(re.search('Lo', match_1.group(1))) and not(re.search('Virtual-Access', match_1.group(1)))):
      result = False
      message = ""
      interface = match_1.group(1)
      command_2 = command_2_without_int_name % interface
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)


def Set_ip_rip_authentication_mode_to_md5(net_connect,host_parameters, debug):

  result = False
  message = "NO INT"

  command_1 = "sh ip protocols | sec rip"
  pattern_1 = "\s+([FfGgEe]\w+[0-9/.]+)\s+[12]"

  command_2_without_int_name = "show run interface %s | incl ip rip authentication mode"
  pattern_2 = "ip rip authentication mode md5"

  interface = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if (match_1 and not(re.search('Lo', match_1.group(1))) and not(re.search('Virtual-Access', match_1.group(1)))):
      result = False
      message = ""
      interface = match_1.group(1)
      command_2 = command_2_without_int_name % interface
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)

def Set_neighbor_password(net_connect,host_parameters, debug):

  result = False
  message = "NO PEERS"

  command_1 = "sh run | sec router bgp"
  pattern_1 = "neighbor (.+) remote-as"

  command_2 = "sh run | sec router bgp "
  pattern_2_without_peer_name = "neighbor %s password"

  peer = ""

  output_str_1 = net_connect.send_command(command_1)
  if debug:
    debug_output(command_1, pattern_1, output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = False
      message = ""
      peer = match_1.group(1)
      pattern_2 = pattern_2_without_peer_name % peer
      output_str_2 = net_connect.send_command(command_2)
      if debug:
        debug_output(command_2, pattern_2, output_str_2)
      else:
        pass
      match_2 = re.search(pattern_2, output_str_2)
      if match_2:
        result = True
      else:
        break
  return (result, message)
