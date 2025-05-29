# Tauste Checker

Este projeto é um verificador de cartões para o site Tauste.com.br. Ele automatiza o processo de verificação de cartões de crédito, incluindo suporte a proxy rotation para evitar bloqueios.

## Funcionalidades

- Verificação automática de cartões de crédito
- Suporte a rotação de proxies
- Salvamento automático de cartões válidos
- Configuração flexível de endereços de entrega e faturamento
- Tratamento de erros e timeouts

## Requisitos

- Python 3.6 ou superior
- Conexão com a internet
- Lista de proxies (opcional)

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/Pugn0/tauste.com.br.git
cd tauste-checker
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `lista.txt` com os cartões no formato:
```
numero_cartao|mes|ano|cvv
```

2. (Opcional) Crie um arquivo `proxy.txt` com seus proxies, um por linha:
```
ip:porta
```

## Uso

1. Configure os arquivos necessários (lista.txt e proxy.txt)
2. Execute o script:
```bash
python check.py
```

## Arquivos de Saída

- `live.txt`: Contém os cartões válidos encontrados
- Logs são exibidos no console durante a execução

## Suporte e Contato

Para suporte, dúvidas ou colaboração, entre em contato através do Telegram:
[@pugno_fc](https://t.me/pugno_fc)

## Aviso Legal

Este projeto é apenas para fins educacionais. O uso indevido deste software pode violar os termos de serviço do site alvo. Use por sua conta e risco.
