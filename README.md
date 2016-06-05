# Socket-Handling
Test project for handling communcation between server/client using a passkey

*start daemon with:* <br />
./server.sh start <br />
*or the server with:* <br />
./server/server.py

*connect to server with:*<br />
./client/client.py
and enter password (default 'admin') for communication

| Command       | Description   | Implemented  |
| ------------- |:-------------:| ------------:|
| portprobe     | Checks if a port is open on the server. e.g portprobe \<portnumber\> |    YES       |
| portmod       | Modifies a port to accept or deny incoming traffic via iptables |    NO       |
| services      | Displays currently enabled services |    YES       |
| mdf           | Custom Diskfree display. |    YES       |
| help          | Shows this menu.      |    YES       |
| whoami        | Displays the daemon's owner      |    YES       |
| q             | Terminates this client      |    YES       |
