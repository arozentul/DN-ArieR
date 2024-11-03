from Class_SSH_Con import SSH_Conn

import re
from collections import OrderedDict

# Assuming SSH_Conn is the class you provided earlier and it handles all SSH connections and interactions

INTERFACE_REGEX = r'\bge\d+-\d+/\d+/\d+\b'


class BaseConnector:
    def __init__(self, ip, username, interface=None):
        self.ip = ip
        self.username = username
        self.interface = '' if interface is None else interface

        try:
            self.connection: SSH_Conn = SSH_Conn(host=self.ip, authentication=None, localized_exec=True,
                                                 session_log='test_con.log',
                                                 icmp_test=True)
            self.connection.connect()

        except Exception as e:
            print(f'Error: {e}')
            self.connection: SSH_Conn = None

    def get_up_interfaces(self):
        if self.connection is None:
            print('Error: Connection failed')
            return []

        self.connection.change_mode(requested_cli=self.connection.SSH_ENUMS.CLI_MODE.DNOS_SHOW)
        output = self.connection.exec_command(cmd='show interfaces', timeout=100)

        # Define a regex pattern to capture interface names with "up" operational status
        interface_pattern = re.compile(r'^\|\s+(ge\d+-\d+/\d+/\d+).*\|\s+up\s+\|', re.MULTILINE)

        # Find all interfaces that are up
        up_interfaces = interface_pattern.findall(output)

        # Convert to a set and back to a list to remove duplicates
        up_interfaces = list(OrderedDict.fromkeys(up_interfaces))

        return up_interfaces


if __name__ == "__main__":
    device_id = "wng1c7vs00017p2"
    connector = BaseConnector(ip=device_id, username='your_username')
    up_interfaces = connector.get_up_interfaces()

    if up_interfaces:
        print(f"Interfaces that are UP on {device_id}:\n")
        for interface in up_interfaces:
            print(f"- {interface}")
    else:
        print(f"No interfaces are UP on {device_id}, or failed to connect.")
