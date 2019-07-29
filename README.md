## UI - MyApp
Both two parts of diagnostics are integerated into the MyApp UI. Both could be run from UI or by python files directly.
Install python3 and pyqt5. Then run following command to open GUI window
```
python MyApp
```
Enter hostaddr, username, password respectively. Then click refresh.

## Part 1. network topo GUI
Telnet to target switch and generate the network topo image automatically. When dynamic showing graph, blue lines mean link-up during time interval and res lines mean link-down.

### Input parameters: (install python3 and run the following cmd)
```
python switch2graph_log.py <host_addr> <username> <password> <timeinterval - sec>
```
  
- type in username if any.

- will show static image if timeinterval is less than or equal to 0.


**repo contains a sample topo graph and a log output

## Part 2. app-hosting diagnostics
### Input parameters: (install python3 and run the following cmd)
```
python readloginfo.py <host_addr> <username> <password>
```
- type in username if any.

- will show app-hosting related info automatically

- funtions to fix app-hosting issues also inluded in the .py file
