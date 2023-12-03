# Controle de Patrimônio de Equipamentos - Projeto Duplex Soft

<h2> 💻 Sobre o projeto </h2>

Na aplicação conseguimos fazer todo o controle do patrimonio de equipamento ajudando assim as equipes de TI terem um controle melhor de onde os 
equipamentos estão, quem é o colaborador responsável, e ter um rastreio de por qual empresa e/ou colaborador aquele equipamento já foi utilizado.

Com isso temos as seguintes funcionalidades:
  <li> Cadastro e listagem de Colaborador (que é a pessoa que será responsável por um equipamento);
  <li> Cadastro e listagem de Empresa (é a empresa que se encontra o equipamento, muito utilizado caso tenha equipamentos em mais de uma filial);
  <li> Cadastro e listagem do Tipo de Equipamento (aqui é aonde será cadastrado os tipos de equipamento);
  <li> Cadastro e listagem de Equipamentos (aqui é o cadastro do equipamento em sí, aonde cada um deverá ter uma TAG de marcação unica);
  <li> Detalhamento de todos os equipamentos vinculados a um Colaborador;
  <li> Detalhamento de todos os equipamentos vinculados a uma empresa;
  <li> Detalhamento de todos os equipamentos vinculados a um tipo de equipamento;
  <li> Histórico de transferencias de equipamento entre empresas, colaboradores e mudança de situação (disponivel, em uso, em manutenção e etc) de um equipamento;

<h2>🛠 Requisitos e instalação do projeto</h2>

### Documentação da API

A documentação completa da API pode ser encontrada [aqui](https://documenter.getpostman.com/view/21881076/2s9YeAAEeb). Este link direciona para a documentação gerada no Postman, que contém detalhes sobre endpoints, parâmetros, métodos e exemplos de uso.

### Pré-requisitos

- Python instalado (versão  3.12.0)
- Git instalado
- Ambiente virtual (recomendado)

### Instalação

1. Clone o repositório do projeto:

```bash
git clone https://github.com/lgustavoss/api_inventario.git
```

2. Navegue até o diretório do projeto:

```bash
cd api_inventario
```

3. (Opcional) Crie e ative um ambiente virtual:

```bash
# Criação do ambiente virtual (pode variar dependendo do sistema operacional)
python -m venv nome_do_ambiente

# Ativação do ambiente virtual no Windows
nome_do_ambiente\Scripts\activate

# Ativação do ambiente virtual no macOS/Linux
source nome_do_ambiente/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requerimentos.txt
```

5. Inicie as migrações para o banco:

```bash
python manage.py makemigrations
```

6. Configure o banco de dados e migre as alterações:

```bash
python manage.py migrate
```

7. Execute o servidor:

```bash
python manage.py runserver
```