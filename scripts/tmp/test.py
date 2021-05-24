import benchmark_check_scripts

username = "admin"
password = "cisco123"
host = "192.168.31.136"

result = benchmark_check_scripts.create_acl_for_use_with_line_vty(host, username, password)
print (result)
