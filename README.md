# Useful Mininet Scripts

## About
A place for useful Mininet scripts. 

## Requirements
```
Kernel 5.13.0-48-generic
Ubuntu 20.04.2 LTS
Python 3.8.10
Mininet 2.6
networkx 2.8.3
```

## Run
Use `python3` to launch scripts.

## Documentation
### Static Routing
Static routing is implemeted in `static_route.py`. It is possible to specify a set of hosts, links, and paths consisting of hosts. 
The file already contains an example. To run the example, use the following commands:
```
sudo python3 static_route.py
mininet> xterm h1
h1> ping 10.0.4.2
```
In this case, host `h1` pings host `h4` via host `h6`. To verify, we can open `wireshark` in host `h6`:
```
mininet> h6 wireshark &
```
It is possible to see ICMP packets exchange between `h1` (`10.0.1.2`) and `h4` (`10.0.4.2`).

## License
Copyright 2022 Mahdi Dolati.

The project's source code are released here under the MIT license. 
