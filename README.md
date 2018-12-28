![Cabure](./cabure.svg)

# Cabure Pipeline

Pipeline de dados do Caburé, baixa e extrai os dados dos relatórios
de cota parlamentar da ALEPI e gera relatórios mensais e anuais.
É feito usando [luigi](https://github.com/spotify/luigi), um gerenciador
de pipelines em batch feito em Python. O resultado é salvo em `data` no
diretório atual, nos arquivos `year-report-<year>.csv` e `<mes>/spends.csv`.

## Setup

O Caburé foi testado apenas no Python 3.7, em um ambiente Docker. Você vai
precisar de algumas ferramentas para poder rodar.

### poppler-utils

O `poppler-utils` é uma toolkit que permite obter informacões, converter e
manipular PDFs, essa dependência é necessária nesse projeto porque os dados
são disponibilizados no site da ALEPI em formato PDF, [aqui](http://ccheque.hospedagemdesites.ws/transparencia/verbaindenizatoria.php?pasta=2018).

Para instalar no Debian/Ubuntu:

```
sudo apt-get install poppler-utils
```

### pip

Se você não roda uma instalação "padrão" do Python, que não possui o `pip`, você vai
precisar instala-lo:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Instalando dependências

```
pip install -r requirements.txt
```


### Docker

Se você usar Docker, e não tiver disposto a lidar com essas dependências, basta
rodar usando o Docker ou o Docker Compose.

Docker:

```
docker build -t cabure .
docker run --rm -it -v $(pwd):/usr/src/app -e PYTHONPATH=/usr/src/app cabure luigi --local-scheduler --module cabure RunForYear --year 2017
```

Docker Compose:

Mude o parametro do ano no comando no `docker-compose.yaml` para o ano que desejado
e execute:

```
docker-compose up --build
```

## License

[MIT](./LICENSE)