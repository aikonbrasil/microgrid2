#!/usr/bin/expect -f
spawn ssh -t root@192.168.11.1 
expect "assword:"
send "YourOwnPassword\r"
expect "#"

send "lte serving-cell list\r"
#send "status lte list\r"
send "status gps list\r"
#send "status time  +'=|%Y|%m|%d|%H|%M|%S'\r"
send "status time list\r"
#send "lte serving-cell list\r"
#send "date\r"
#timestamp
send "exit\r"
expect eof
