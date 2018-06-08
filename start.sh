#!/usr/bin/expect
set timeout 100
set password "Vanlon88989982!@#"
spawn sudo bash /home/vanlon/monitor.sh
expect "vanlon"
send "$password\n"
interact
