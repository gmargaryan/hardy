import paramiko
from getpass import getpass
import time
import re

def cmd_exec_cisco_ios (host, username, password, command):

#### Authentication block ####

  username = username
  password = password
  #password = getpass()
  #enable = 'cisco123'
  ip = host

#### Commands block ####

  cmd_1 = command + '\n'

#### Prompt block ####

# To remove prompt from line:

#  p = re.compile(r'\s*[\w().-]*[\$#>]\s?(?:\(enable\))?\s*(.*)$')
#  m = p.search(output_with_prompt)
#  output_without_prompt = m.group(1)

#### Main Body ####

  remote_conn_pre=paramiko.SSHClient()
  remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  remote_conn_pre.connect(ip, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)

  remote_conn = remote_conn_pre.invoke_shell()
  output = remote_conn.recv(65535)

#### Enable ####

#  remote_conn.send('enable\n')
#  time.sleep(.5)
#  remote_conn.send('cisco123\n')

#### Commands Block ####

  remote_conn.send(cmd_1)
  time.sleep(.5)
  output = remote_conn.recv(65535)
  output = output.decode('utf-8')

  remote_conn.send("end\n")
  time.sleep(.5)

  return output
		
