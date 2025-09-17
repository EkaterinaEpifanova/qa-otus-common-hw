import socket
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 8080

HEADER = "iso-8859-1"
BODY = "utf-8"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(128)
    print(f"Listening on http://{HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with conn:
            try:
                data = bytearray()
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    data += chunk

                head, _, _ = data.partition(b"\r\n\r\n")
                text = head.decode(HEADER, errors="replace")
                lines = text.split("\r\n")
                request_line = lines[0] if lines else ""
                parts = request_line.split(" ")

                method = parts[0] if len(parts) > 0 else "GET"
                target = parts[1] if len(parts) > 1 else "/"
                version = parts[2] if len(parts) > 2 else "HTTP/1.1"
                headers_raw = [ln for ln in lines[1:] if ln]

                status = HTTPStatus(200)
                try:
                    query = urlparse(target).query
                    val = parse_qs(query).get("status", [None])[0]
                    if val not in (None, ""):
                        status = HTTPStatus(int(val))
                except Exception:
                    status = HTTPStatus(200)

                body_lines = [
                    f"Request Method: {method}",
                    f"Request Source: {addr}",
                    f"Response Status: {status.value} {status.phrase}",
                    *headers_raw,
                ]
                body = ("\r\n".join(body_lines) + "\r\n").encode(BODY)

                if not version.startswith("HTTP/"):
                    version = "HTTP/1.1"
                status_line = f"{version} {status.value} {status.phrase}\r\n"
                resp_headers = [
                    "Content-Type: text/plain; charset=utf-8",
                    f"Content-Length: {len(body)}",
                    "Connection: close",
                ]
                head_out = status_line + "\r\n".join(resp_headers) + "\r\n\r\n"
                conn.sendall(head_out.encode(HEADER) + body)

            except Exception as e:
                body = (
                    "Request Method: UNKNOWN\r\n"
                    f"Request Source: {addr}\r\n"
                    "Response Status: 500 Internal Server Error\r\n"
                    f"error: {e}\r\n"
                ).encode(BODY)
                head_out = (
                    "HTTP/1.1 500 Internal Server Error\r\n"
                    "Content-Type: text/plain; charset=utf-8\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Connection: close\r\n\r\n"
                ).encode(HEADER)
                try:
                    conn.sendall(head_out + body)
                except Exception:
                    pass
