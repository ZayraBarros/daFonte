# Configuração de Envio de Email

## Modo Teste (Atual)

Por padrão, o servidor está rodando em **modo teste**. Quando alguém preencher o formulário:
- Os dados serão exibidos no console do servidor
- Nenhum email real será enviado

## Configurar Envio Real de Email

Para enviar emails reais para `felipe.bastos3357@gmail.com`, você precisa:

### 1. Criar uma Senha de App no Gmail

1. Acesse: https://myaccount.google.com/apppasswords
2. Faça login na sua conta Gmail
3. Selecione "App" e escolha "Mail"
4. Selecione "Outro (nome personalizado)" e digite "DAFONTE Server"
5. Clique em "Gerar"
6. Copie a senha gerada (16 caracteres)

### 2. Configurar Variáveis de Ambiente

No terminal, antes de rodar o servidor:

```bash
export EMAIL_REMETENTE="seu-email@gmail.com"
export SENHA_APP="sua-senha-de-app-gerada"
python3 server.py
```

Ou crie um arquivo `.env` (não commitado) e carregue antes:

```bash
source .env
python3 server.py
```

### 3. Testar

1. Acesse http://localhost:8000
2. Preencha o formulário
3. Verifique o email em `felipe.bastos3357@gmail.com`

## Estrutura do Email

O email enviado terá:
- **Assunto**: "Novo contato da Landing Page DAFONTE"
- **Conteúdo**:
  - Nome
  - E-mail
  - WhatsApp
  - Indicação de que veio da landing page

