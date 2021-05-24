from check_list_exec import check_list_exec as cle
import getopt
import sys
import yaml
import re


def usage_incorrect ():
  print('\nIncorrect syntax\nType python3 scaner.py -h')

def help_info():
  print ("\n")
  print("###########################################################################################################")
  print("#                                                                                                         #")
  print("#  python3 scaner.py [ -h ] -f file_name -u username [ -s secret ] [ -p -password ] [ -k key_file ] [-d]  #")
  print("#                                                                                                         #")
  print("#  -f file_name - is a file with a list of hosts parameters needed for sacnning                           #")
  print("#  -k key_file  - pem certificate file                                                                    #")
  print("#  -s secret    - enable(Cisco)/sudo(Linux)                                                               #")
  print("#  -d           - debugging                                                                               #")
  print("#  -h           - help                                                                                    #")
  print("#                                                                                                         #")
  print("#  Example: python3 scaner.py -u admin -p cisco123 -s cisco123 -f test_list.yml                           #")
  print("#           python3 scaner.py -u ubuntu -k '/Users/Roman/.ssh/nihole.pem' -f ubuntu.yml                   #")
  print("#                                                                                                         #")    
  print("###########################################################################################################")
  print ("\n")

def main():

  [username, password, secret, key_file, file_name, debug] = ['','','','','', False]
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:s:k:f:hd', ['user=', 'passowrd=', 'secret=', 'key=', 'file=', 'help', 'debug'])
  except getopt.GetoptError as err:
    print()
    usage_incorrect()
    sys.exit()
  
  for opt,arg in opts:
    if opt in('-h', '--help'):
      help_info()
      sys.exit()
    elif opt in ('-d', '--debug'):
      debug = True
    elif opt in ('-f', '--file'):
      file_name = arg
    elif opt in ('-u', '--user'):
      username=arg
    elif opt in ('-p', '--password'):
      password=arg
    elif opt in ('-s', '--secret'):
      secret=arg
    elif opt in ('-k', '--key'):
      key_file=arg
    else:
      usage_incorrect()
      sys.exit()

  if not(file_name and username and (password or key_file)):
    usage_incorrect()
    sys.exit()

#### read information related to scanned devices  ###

  device_list = "../devices/%s" % file_name
  f = open( "./%s" % device_list )
  data_device_list = f.read()
  f.close()

#### yaml parsing of device_list ####

  yaml_version = yaml.__version__
  m = re.match ('(\d(\.\d)?)', yaml_version)
  yaml_ver = m.group(1)

  if (float(yaml_ver) < 5.1):
    yaml_data_device_list = yaml.load(data_device_list)
  else:
    yaml_data_device_list = yaml.load(data_device_list,Loader=yaml.FullLoader)

  for host_el in yaml_data_device_list['hosts']: 

    if re.match('yes', host_el['status']):
      print("\n#######################################################################################################")
      print("\n")
      print("  Host is " + host_el['ip_address'])
      print("  Benchmarks, check list: " + host_el['benchmarks']['check_list'])
      print("  Benchmarks, commands and patterns: " + host_el['benchmarks']['check_output'])
      print("  Benchmarks, scripts: " + host_el['benchmarks']['scripts'])     
      print("\n")
      print("#######################################################################################################\n")
      credentials = [username, password, secret, key_file]
      cle(credentials, host_el, debug)
    else:
      print ("Device %s is not scanned" % host_el['ip_address'])


if __name__ == "__main__":
  main()
