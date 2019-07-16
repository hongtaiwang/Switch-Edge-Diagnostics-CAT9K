## part 1. network-topo-GUI-based-on-cdp-info
Telnet to target switch and generate the network topo image automatically. When dynamic showing graph, blue lines mean link-up during time interval and res lines mean link-down.

### Input parameters: (install python3 and run the following cmd)
```
python3 switch2graph_log.py <host_addr> <username> <password> <timeinterval - sec>
```
  
type in username if any.

will show static image if timeinterval is less than or equal to 0.


**repo contains a sample topo graph and a log output

## part 2. app-hosting logs
### Input parameters: (install python3 and run the following cmd)
```
python3 readloginfo.py <host_addr> <username> <password>
```
type in username if any.

Will show app-hosting related info automatically
