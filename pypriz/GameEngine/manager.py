import socket
from select import select
from queue import Queue

request_queue = Queue()

def task_manager():
    match_queue = Queue()
    request = request_queue.get(block=True)

def run_server(port='5007', host=''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        conn_list = [ server ]
        server.bind((HOST, PORT))
        server.listen(10)
        while True:
            readables, _, _ = select.select(conn_list, _, _)
            for readable in readables:
                if readable is server:
                    conn, addr = server.accept()
                    conn_list.append(conn)
                else:
                    data = readable.recv(4096)
                    request_queue.put(data)

