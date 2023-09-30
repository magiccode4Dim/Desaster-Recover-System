import http.server
import socketserver

# Define a porta em que o servidor irá escutar
port = 7000

# Cria um manipulador (handler) para o servidor HTTP
handler = http.server.SimpleHTTPRequestHandler

# Inicializa o servidor com o manipulador e a porta especificada
with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Servidor HTTP em execução na porta {port}")
    
    # Mantém o servidor em execução indefinidamente
    httpd.serve_forever()
