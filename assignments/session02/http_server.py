import socket
import sys
import os
import mimetypes


def response_ok(body="", mimetype="text/plain"):
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: {0}".format(mimetype))
    resp.append("")
    resp.append(body)
    return "\r\n".join(resp)
    
def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)

def response_not_found():
    """returns a 404 Not found response"""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    return uri

def resolve_uri(uri):
    relv_uri=uri.lstrip('/')
    base='webroot'
    path = os.path.join(base,relv_uri)

    if os.path.exists(path):
        if os.path.isdir(path):
            contents=os.listdir(path)
            body="/n".join(contents)
        elif os.path.isfile(path):
            try:
                body=open(path,'rb').read()
            except :
                raise IOError
    else:
        raise ValueError
 
    mimetype=mimetypes.guess_type(path)[0]
    mimetype="text/plain" if not mimetype else mimetype
    return body,mimetype



def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    uri=parse_request(request)
                    body,mime=resolve_uri(uri)

                except NotImplementedError:
                    response = response_method_not_allowed()
                except (IOError,ValueError):
                    response=response_not_found()
                else:
                    response = response_ok(body,mime)

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()
            
    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
