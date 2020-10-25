# SDCCProject
![parking now logo]()

## Requirements
This project uses docker and docker-compose to simulate the fog nodes locally.
Please refer to this links:
* [docker download](https://www.docker.com/products/docker-desktop)
* [docker compose download](https://docs.docker.com/compose/install/)

## Fog nodes
To create the fog nodes you need to run the following command from the terminal:
    
    docker-compose up --scale fognode=3

This will create both the proxy server, which redirects the client requests to one of the nodes, and the fog cluster.
You need to specify the number of instances of fog nodes you wish to create (in the above example we
use 3). 

[docker-compose up manual](https://docs.docker.com/compose/reference/up/)

#### Sensors
To run the sensors you can use:

    python sensor.py
    
## Client
