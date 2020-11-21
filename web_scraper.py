import socket, requests, argparse, sys
from bs4 import BeautifulSoup

class Server:
    LHOST = '127.0.0.1'
    LPORT = 4444
    MAX_BYTES = 65535

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_working(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.LHOST, self.LPORT))
        self.sock.listen(1)

        print('---'*18)
        print("[SERVER] is started at ", self.sock.getsockname())

        while True:
            conn, sockname = self.sock.accept()
            print('---'*18)
            print("Connection established with ", sockname)
            print('\nScraping web page...')
            url = (conn.recv(self.MAX_BYTES)).decode()
            processed_data = self.process_url(url)
            data_to_send = 'Pictures: '+str(processed_data['pictures'])+'\n'+'Leaf paragraphs: '+str(processed_data['leaf_paragraphs'])+'\n'
            conn.sendall(data_to_send.encode())
            print('Results were sent to client ', conn.getpeername())


    def process_url(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        proc_data = {}
        pic_num = self.count_pic(soup)
        leaf_p_num = self.count_leaf_p(soup)
        proc_data['pictures'] = pic_num
        proc_data['leaf_paragraphs'] = leaf_p_num
        return proc_data

    def count_pic(self, soupp):
        img_tags = soupp.find_all('img')
        return len(img_tags)

    def count_leaf_p(self, soupp):
        p_tags = soupp.find_all('p')

        c=0
        for i in p_tags:
            if not i.find_all('p'):
            #if not i.findChildren():
                c+=1

        return c



class Client:
    LHOST = '127.0.0.1'
    LPORT = 4444
    MAX_BYTES = 65535

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_working(self, url):
        self.sock.connect((self.LHOST, self.LPORT))

        print('---'*18)
        print("[CLIENT] is started at ", self.sock.getsockname())
        print("Connected to server at ", self.sock.getpeername())
        print('---'*18)
        self.sock.sendall(url.encode())

        print('Waiting for result...\n')
        data_from_server = (self.sock.recv(self.MAX_BYTES)).decode()
        print('\033[1m'+data_from_server+'\033[0m')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Scraper")
    options={"client": Client, "server": Server}
    parser.add_argument("role", choices=options, help="server or client")

    if sys.argv[1] == "client":
        parser.add_argument('-p', type = str, help = "URL")

    args=parser.parse_args()
    class_name = options[args.role]

    if args.role == "server":
        server_obj = class_name()
        server_obj.start_working()

    elif args.role == "client":
        client_obj = class_name()
        client_obj.start_working(args.p)
