import socket
from website import create_app

app = create_app()

def start_the_server():#this function is res
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 5000))
        server.listen(4)
        while True:
            print('Server is working...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            content = load_page_get_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print('Shut down')
    
    
def load_page_get_request(request_data): 
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request_data.split(' ')[1]
    response = ''
    with open('website/templates' + path, 'rb') as file:
        response = file.read()
    return HDRS.encode('utf-8') + response

if __name__ == '__main__':
    app.run(debug=True)
