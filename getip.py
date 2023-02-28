import fcntl
import socket
import struct

try:
    from netifaces import AF_INET, ifaddresses
except ModuleNotFoundError as e:
    raise SystemExit(f"Requires {e.name} module. Run 'pip install {e.name}' "
                     f"and try again.")


def get_ip_linux(interface: str) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packed_iface = struct.pack('256s', interface.encode('utf_8'))
    packed_addr = fcntl.ioctl(sock.fileno(), 0x8915, packed_iface)[20:24]
    return socket.inet_ntoa(packed_addr)


print(get_ip_linux("wlan0"))
