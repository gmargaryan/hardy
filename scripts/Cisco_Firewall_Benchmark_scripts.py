import re
import yaml
from netmiko import Netmiko

### Dependecies ####

def if_eigrp_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO EIGRP"

  command_1 = "sh run router eigrp"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1 + "\n")
  if debug:
    print ("\ncommand:\n" + command_1)
    print ("\npattern:\n" + pattern_1)
    print ("\noutput:\n" + output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = True
      message = ""
      break
  return (result, message)

def if_ospf_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO OSPF"

  command_1 = "sh run router ospf"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1 + "\n")
  if debug:
    print ("\ncommand:\n" + command_1)
    print ("\npattern:\n" + pattern_1)
    print ("\noutput:\n" + output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = True
      message = ""
      break
  return (result, message)

def if_bgp_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO BGP"

  command_1 = "sh run router bgp"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1 + "\n")
  if debug:
    print ("\ncommand:\n" + command_1)
    print ("\npattern:\n" + pattern_1)
    print ("\noutput:\n" + output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = True
      message = ""
      break
  return (result, message)

def if_rip_configured (net_connect,host_parameters, debug):

  result = False
  message = "NO RIP"

  command_1 = "sh run router rip"
  pattern_1 = ".+"

  output_str_1 = net_connect.send_command(command_1 + "\n")
  if debug:
    print ("\ncommand:\n" + command_1)
    print ("\npattern:\n" + pattern_1)
    print ("\noutput:\n" + output_str_1)
  else:
    pass
  # str -> list
  output_list_1 = output_str_1.split("\n")
  # check each line with pattern
  for output_line in output_list_1:
    match_1 = re.search(pattern_1, output_line)
    if match_1:
      result = True
      message = ""
      break
  return (result, message)


### Scripts ####

def Ensure_Password_Policy_is_enabled(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_Image_Integrity_is_correct(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_TACACS_RADIUS_is_configured_correctly(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_RSA_key_pair_is_greater_than_or_equal_to_2048_bits(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_noproxyarp_is_enabled_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_DHCP_services_are_disabled_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_ICMP_is_restricted_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_intrusion_prevention_is_enabled_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_packet_fragments_are_restricted_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_non_default_application_inspection_is_configured_correctly(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_DOS_protection_is_enabled_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_ip_verify_is_set_to_reverse_path_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_security_level_is_set_to_0_for_Internet_facing_interface(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_Botnet_protection_is_enabled_for_untrusted_interfaces(net_connect,host_parameters, debug):
  return (False, "MANUAL")
def Ensure_explicit_deny_in_access_lists_is_configured_correctly(net_connect,host_parameters, debug):
  return (False, "MANUAL")
