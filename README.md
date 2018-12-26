# Cabure Pipeline

Pipeline de dados do Caburé, baixa e extrai os dados dos relatórios
de cota parlamentar da ALEPI e gera relatórios mensais e anuais.

## Setup

```
docker build -t cabure .
```

## Run

```
docker run --rm -it -v $(pwd):/usr/src/app -e 'PYTHONPATH=/usr/src/app' cabure luigi --local-scheduler --module cabure RunForYear --year 2017
```

## License

[MIT](./LICENSE)