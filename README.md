# Blood Type Compatibility

Visualization for the prevalence and compatibility of blood types.

Currently hosted at https://btc.busuttil.ca

## quick start

```bash
poetry shell
python3 src/graph_show.py
```

## source

https://www.blood.ca/en/blood/donating-blood/what-my-blood-type

## deploying a copy

- clone the repo `git clone https://github.com/MikeBusuttil/bloodtypes.git`
- launch the container `cd bloodtypes && docker compose up -d`

Note: deploying assumes the pre-installation of git, docker, and [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy)
