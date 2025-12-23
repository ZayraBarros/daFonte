#!/usr/bin/env python3
"""
Servidor simples para enviar emails do formulário da landing page
Usa Resend API (compatível com Railway e outras plataformas cloud)
"""
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import logging

# Configure logging
logger = logging.getLogger('dafonte_mail')
logger.setLevel(logging.INFO)
if not logger.handlers:
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(sh)

# Configurações de email
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO", "felipe.bastos3357@gmail.com")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "contato@dafonteinfra.com.br")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

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
                if RESEND_API_KEY:
                    try:
                        response = requests.post(
                            'https://api.resend.com/emails',
                            headers={
                                'Authorization': f'Bearer {RESEND_API_KEY}',
                                'Content-Type': 'application/json'
                            },
                            json={
                                'from': EMAIL_REMETENTE,
                                'to': [EMAIL_DESTINO],
                                'subject': assunto,
                                'text': corpo
                            },
                            timeout=10
                        )

                        if response.status_code == 200:
                            logger.info(f"Email enviado com sucesso para {EMAIL_DESTINO} (nome={nome}, email={email})")
                        else:
                            logger.error(f"Erro ao enviar email: {response.status_code} - {response.text}")
                            self.send_response(500)
                            self.send_header('Content-Type', 'application/json')
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.end_headers()
                            self.wfile.write(json.dumps({'error': 'Erro ao enviar email'}).encode())
                            return
                    except Exception as e:
                        logger.exception(f"Erro ao enviar email para {EMAIL_DESTINO}")
                        self.send_response(500)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': 'Erro ao enviar email'}).encode())
                        return
                else:
                    # Modo de teste - apenas imprime no console
                    logger.info("EMAIL (MODO TESTE - não enviado): Para=%s Assunto=%s", EMAIL_DESTINO, assunto)
                    logger.info("Corpo:\n%s", corpo)
                    logger.info("⚠️  Para enviar emails reais, configure RESEND_API_KEY nas variáveis de ambiente.")
                
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

        # Frontend está em ../front/ relativo ao backend/
        file_path = os.path.join(os.path.dirname(__file__), '..', 'front', self.path.lstrip('/'))

        try:
            with open(file_path, 'rb') as f:
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
            self.send_header('Access-Control-Allow-Origin', '*')
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
    port = int(os.environ.get("PORT", 8080))

    server = HTTPServer(('0.0.0.0', port), EmailHandler)

    print(f"🚀 Servidor rodando em http://0.0.0.0:{port}")
    print(f"📧 Emails serão enviados para: {EMAIL_DESTINO}")

    if not RESEND_API_KEY:
        print("⚠️  Modo TESTE: emails serão apenas exibidos no console")
        print("   Configure RESEND_API_KEY para envio real")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado.")
        server.server_close()


