This is an edge diagnostic application for Cisco Cat9K switch
## UI - MyApp
Both two parts of diagnostics are integrated into the MyApp UI. Both could be run from UI or by python files directly.
Install python3 and pyqt5. Then run following command to open GUI window
```
python MyApp.py
```
 - Should set username, password and vty tunnel for the switch before using this tool
 - Enter hostaddr, username, password, enable password (if any) respectively. Then click refresh. 
 - Network topo will be stored as a .png file and the log as LogInfo.txt in the same dir.
 - The green button means no err, and the red ones means issue exists. Click on the red button, then the program will fix the issue by itself.

## Part 1. network topo GUI
Telnet to target switch and generate the network topo image automatically. When dynamic showing graph, blue lines mean link-up during time interval and res lines mean link-down.

### Input parameters: (install python3 and run the following cmd)
```
python switch2graph_log.py <host_addr> <username> <password> <ena-password> <timeinterval - sec>
```
  
- Type in enable password if any.

- Will show static image if timeinterval is less than or equal to 0.

- Output files stored under the same path as the script file


**repo contains a sample topo graph and a log output

## Part 2. app-hosting diagnostics
### Input parameters: (install python3 and run the following cmd)
```
python readloginfo.py <host_addr> <username> <password> <ena-password>
```
- Type in enable password if any.

- Will show app-hosting related info automatically

- Funtions to fix app-hosting issues also inluded in the .py file

- Output file stored under the same path as the script file
