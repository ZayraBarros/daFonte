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

## Armazenando a senha com segurança (Keyring)

Recomendado: não deixe a `SENHA_APP` em variáveis de ambiente permanentes. No macOS (ou Windows/Linux) você pode usar o Keychain/keyring do sistema.

1) Instale a dependência auxiliar (quando necessário):

```bash
pip3 install keyring
```

2) Use o script `set_keyring.py` para gravar a senha de app no Keychain:

```bash
python3 set_keyring.py --email "helio.oficio@gmail.com" --password "SUA_SENHA_DE_APP"
```

3) No `server.py` o código tentará automaticamente ler a senha do keyring (serviço `dafonte_email`) se `EMAIL_REMETENTE` estiver definido e `SENHA_APP` não.

4) Para rodar o servidor usando o keyring, apenas exporte o remetente e destino (não a senha):

```bash
export EMAIL_REMETENTE="helio.oficio@gmail.com"
export EMAIL_DESTINO="zayrita.barros@gmail.com"
python3 server.py
```

Observação: se preferir, também é possível usar `.env` em desenvolvimento, mas NUNCA comitar `.env` com credenciais.

