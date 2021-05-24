import yaml
import re
from netmiko import Netmiko
import Cisco_Firewall_Benchmark_scripts
import Cisco_IOS_15_Benchmark_scripts
import Ubuntu_Linux_Benchmark_scripts

def print_output(description, result, level, score):

  description_format = "{:<80}".format(description)
  print ("    " + description_format, level + "      " + score + "      " + result)
  print ("------------------------------------------------------------------------------------------------------------")

def check_list_exec(credentials,host_parameters, debug):


#### import correct file with scripts ####
  
  m = re.match('(.+)\.py$', host_parameters['benchmarks']['scripts'])
  if m:
    module = m.group(1)
#    eval("import %s" % module)
  else:
    
    print (host_parameters['benchmarks']['scripts'] + ' - incorrect benchmark script name!')
    exit()
  
#### credentials ####

  host = host_parameters['ip_address']
  device_type =  host_parameters['device_type']
  port = host_parameters['port']

  [username, password, secret, key_file] = credentials
  device = {
    "host": host,
    "username": username,
    "password": password,
    "secret": secret,
    "device_type": device_type,
    "port": port,
#    "global_delay_factor": 10,
#    "blocking_timeout": 100,
    }

  if bool(key_file):
    device["use_keys"] = True
    device['key_file'] = key_file
  else:
    pass


#### table title ####

  description_format = "{:<80}".format("Verification Description")
  print ("    " + description_format, "LEVEL" + " " + "SCORE" + "   " + "RESULT")
  print ("-----------------------------------------------------------------------------------------------------------")


#### read benchmark ####

  benchmark_check_list_file = "../benchmarks/%s" % host_parameters['benchmarks']['check_list']
  benchmark_check_output_file = "../benchmarks/%s" % host_parameters['benchmarks']['check_output']

  f1 = open( "./%s" % benchmark_check_list_file )   
  f2 = open( "./%s" % benchmark_check_output_file )       
  data_check_list = f1.read()
  data_check_output = f2.read()
  f1.close()
  f2.close()

#### yaml parsing of benchmarks ####

  yaml_version = yaml.__version__

  if (float(yaml_version) < 5.1):
    yaml_data_check_list = yaml.load(data_check_list)
    yaml_data_check_output = yaml.load(data_check_output)
  else:
    yaml_data_check_list = yaml.load(data_check_list,Loader=yaml.FullLoader)
    yaml_data_check_output = yaml.load(data_check_output,Loader=yaml.FullLoader)


#### connect to device ####

  net_connect = Netmiko(**device)
  net_connect.enable()

#### if it is Linux, increase the columns number ###
 
  if re.match('linux', device['device_type']):
    net_connect.send_command('stty cols 512')
  else:
    pass

#### score dictionary initiation ####

  score = {
    "level1_success": 0,
    "level1_failed": 0,
    "level2_success": 0,
    "level2_failed": 0  
    }

#### device scanning and output ###

  for sec_dict in yaml_data_check_list["check_list"]:
  
    # print section name
    print ("\n" + sec_dict["section"] + "\n") 
    # for each item in the check list
    for check_dict in sec_dict["check"]:
      check_name = (check_dict["name"])
      if re.match('no', check_dict["status"]):
        print (check_dict["description"] + " is not checked. Change status if needed!")
        breake
      elif re.match('yes', check_dict["status"]):
        pass
      else:
        print (check_dict["description"] + " is not checked. Status is not correct. Should be 'yes' or 'no'!!")
        breake
      # Check dependecy
      if (yaml_data_check_output[check_name]["dependency"]):
          (dependency_result, dependency_message) = eval(module + "." + yaml_data_check_output[check_name]["dependency"] + "(net_connect, host_parameters, debug)")
          if not(dependency_result):
            print_output(check_dict["description"], dependency_message, "", "")
            continue
          else:
            pass
      else:
        pass
      # If there is a script execute it
      if (yaml_data_check_output[check_name]["script"]):
        script_name = yaml_data_check_output[check_name]["script"]
        (result_b, message) = eval(module + "." + script_name + "(net_connect, host_parameters, debug)")
        if message:
          result = message
        elif result_b:
          result = "SUCCESS"
          if (check_dict["level"] == 1):
            score["level1_success"] = score["level1_success"] + check_dict["score"]
          elif (check_dict["level"] == 2):
            score["level2_success"] = score["level2_success"] + check_dict["score"]
          else:
            print ("Error: incorrect level number!")
        else:
          result = "FAILED"
          if (check_dict["level"] == 1):
            score["level1_failed"] = score["level1_failed"] + check_dict["score"]
          elif (check_dict["level"] == 2):
            score["level2_failed"] = score["level2_failed"] + check_dict["score"]
          else:
            print ("Error: incorrect level number!")
        print_output(check_dict["description"], result, str(check_dict["level"]), str(check_dict["score"]))
      # if there is no script, then execute a sequence of the checks in the list
      else:
        # this list is use for the boolean (True/False) results for each checks in the list of commands
        result_list_cmd = []
        # this list is used for logical expression for commands and for patterns and should be nullified
        res = []
        for command_element in yaml_data_check_output[check_name]["commands"]:
          # if command is present
          if command_element["command"]:
            # output of the command  
#            output_str = net_connect.send_command(command_element["command"] + "\n", delay_factor=100, max_loops=100)
            output_str = net_connect.send_command(command_element["command"])
            # if debug is on print the result
            if debug:
              print ("\ncommand:\n" + command_element["command"])
              print ("\noutput:\n" + output_str)
            else:
              pass
            # this list is use for the boolean (True/False) results for each checks in the list of patterns
            result_list_ptrn = []
            # this list is used for logical expression as for commands and for patterns and should be nullified
            res = []
            for ptrn_element in command_element["patterns"]:
              # if pattern is present
              if ptrn_element["pattern"]:
                if debug:
                  print ("\npattern:\n" + ptrn_element["pattern"] + "\n")
                else:
                  pass
                match = re.search(ptrn_element["pattern"], output_str)
                if match:
                  result_list_ptrn.append(True)
                else:
                  result_list_ptrn.append(False)
              else:
                pass
            # if we have at list one pattern for the commnd
            if result_list_ptrn:
              if (re.match('and', command_element["logical_exp_ptrn"]) or re.match('or', command_element["logical_exp_ptrn"])):
                delim_str_ptrn = " %s " % command_element["logical_exp_ptrn"]
                result_ptrn = eval(delim_str_ptrn.join(str(e) for e in result_list_ptrn))
                if debug:
                  print ("pattern_exp = " + delim_str_ptrn.join(str(e) for e in result_list_ptrn))
                else:
                  pass
              else:
                res = result_list_ptrn
                result_ptrn = eval(command_element["logical_exp_ptrn"])
                if debug:
                  print ("pattern_exp = " + command_element["logical_exp_ptrn"])
                else:
                  pass
            else:
              print ("NO PATTERN!")
              break
            if result_ptrn:
              result_list_cmd.append(True)
            else:
              result_list_cmd.append(False)
          # Implemet and or or logic (logical_exp)
          else:
            pass
        # if we have at list one command for this item in the check list
        if result_list_cmd:
          if (re.match('and', yaml_data_check_output[check_name]["logical_exp_cmd"]) or re.match('or', yaml_data_check_output[check_name]["logical_exp_cmd"])):
            delim_str_cmd= " %s " % yaml_data_check_output[check_name]["logical_exp_cmd"]
            result_cmd = eval(delim_str_cmd.join(str(e) for e in result_list_cmd))
            if debug:
              print ("command_exp = " + delim_str_cmd.join(str(e) for e in result_list_cmd))
            else:
              pass
          elif re.search('res', yaml_data_check_output[check_name]["logical_exp_cmd"]):
            res = result_list_cmd
            result_cmd = eval(yaml_data_check_output[check_name]["logical_exp_cmd"])
            if debug:
              print("command_exp = " + yaml_data_check_output[check_name]["logical_exp_cmd"])
            else:
              pass
          else:
            print("Incorrect logical_exp_cmd!")
          if result_cmd:
            result = "SUCCESS"
            if (check_dict["level"] == 1):
              score["level1_success"] = score["level1_success"] + check_dict["score"]
            elif (check_dict["level"] == 2):
              score["level2_success"] = score["level2_success"] + check_dict["score"]
            else: 
              print ("Error: incorrect level number!")
          else:
            result = "FAILED"
            if (check_dict["level"] == 1):
              score["level1_failed"] = score["level1_failed"] + check_dict["score"]
            elif (check_dict["level"] == 2):
              score["level2_failed"] = score["level2_failed"] + check_dict["score"]
            else:
              print ("Error: incorrect level number!")
        # if there are no any commands for this item
        else:
          print ("NO COMMAND")
          result = "NOT CHECKED!"
        print_output(check_dict["description"], result, str(check_dict["level"]), str(check_dict["score"]))

  level1_sum = score["level1_success"] + score["level1_failed"]
  level2_sum = score["level2_success"] + score["level2_failed"]
  level12_success = score["level1_success"] + score["level2_success"]
  level12_sum = level1_sum + level2_sum

  print ("\n SCORES:\n")
  print (" LEVEL1: %s from %s" % (score["level1_success"], level1_sum)) 
  print (" LEVEL2: %s from %s" % (level12_success, level12_sum))
  print ("\n\n")

  net_connect.disconnect()


