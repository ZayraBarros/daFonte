#!/usr/bin/env python3
"""
Servidor simples para enviar emails do formulário da landing page
"""
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import os

# Configurações de email
EMAIL_DESTINO = "felipe.bastos3357@gmail.com"
# Para usar Gmail, você precisa criar uma "Senha de app" em:
# https://myaccount.google.com/apppasswords
# Deixe vazio para testar sem envio real (vai apenas imprimir no console)
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "")
SENHA_APP = os.getenv("SENHA_APP", "")

class EmailHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST request"""
        if self.path == '/send-email':
            try:
                # Ler dados do POST
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                nome = data.get('nome', '')
                email = data.get('email', '')
                whatsapp = data.get('whatsapp', '')
                
                # Criar mensagem de email
                assunto = "Novo contato da Landing Page DAFONTE"
                corpo = f"""
Novo contato recebido da Landing Page DAFONTE:

Nome: {nome}
E-mail: {email}
WhatsApp: {whatsapp}

---
Este email foi enviado automaticamente pelo formulário da landing page.
"""
                
                # Enviar email
                if EMAIL_REMETENTE and SENHA_APP:
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = EMAIL_REMETENTE
                        msg['To'] = EMAIL_DESTINO
                        msg['Subject'] = assunto
                        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
                        
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(EMAIL_REMETENTE, SENHA_APP)
                        server.send_message(msg)
                        server.quit()
                        
                        print(f"✓ Email enviado com sucesso para {EMAIL_DESTINO}")
                    except Exception as e:
                        print(f"✗ Erro ao enviar email: {e}")
                        # Retorna erro mas não falha completamente
                        self.send_response(500)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': 'Erro ao enviar email'}).encode())
                        return
                else:
                    # Modo de teste - apenas imprime no console
                    print("\n" + "="*50)
                    print("📧 EMAIL (MODO TESTE - não enviado)")
                    print("="*50)
                    print(f"Para: {EMAIL_DESTINO}")
                    print(f"Assunto: {assunto}")
                    print(f"\n{corpo}")
                    print("="*50)
                    print("\n⚠️  Para enviar emails reais, configure EMAIL_REMETENTE e SENHA_APP")
                    print("   ou defina as variáveis de ambiente:")
                    print("   export EMAIL_REMETENTE='seu-email@gmail.com'")
                    print("   export SENHA_APP='sua-senha-de-app'")
                    print("="*50 + "\n")
                
                # Resposta de sucesso
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                
            except Exception as e:
                print(f"Erro ao processar requisição: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Serve arquivos estáticos"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        else:
            # Remove leading slash for file system
            self.path = self.path.lstrip('/')
        
        try:
            with open(self.path, 'rb') as f:
                content = f.read()
                
            # Determinar content type
            content_type = 'text/html'
            if self.path.endswith('.css'):
                content_type = 'text/css'
            elif self.path.endswith('.js'):
                content_type = 'application/javascript'
            elif self.path.endswith('.png'):
                content_type = 'image/png'
            elif self.path.endswith('.jpg') or self.path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif self.path.endswith('.webp'):
                content_type = 'image/webp'
            elif self.path.endswith('.svg'):
                content_type = 'image/svg+xml'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
        except Exception as e:
            print(f"Erro ao servir arquivo: {e}")
            self.send_response(500)
            self.end_headers()

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('localhost', port), EmailHandler)
    print(f"🚀 Servidor rodando em http://localhost:{port}")
    print(f"📧 Emails serão enviados para: {EMAIL_DESTINO}")
    if not EMAIL_REMETENTE or not SENHA_APP:
        print("⚠️  Modo TESTE: emails serão apenas exibidos no console")
        print("   Configure EMAIL_REMETENTE e SENHA_APP para envio real")
    print("\nPressione Ctrl+C para parar o servidor\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor parado.")
        server.shutdown()

