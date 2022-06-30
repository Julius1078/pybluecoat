from paramiko.client import SSHClient
from paramiko.ssh_exception import SSHException



class BluecoatServer:

    def _connect(self):
        if not self._client:
            self._client = SSHClient()
            self._client.load_system_host_keys()
            self._client.connect(
                self._servername, username=self._username, password=self._password)

    def __init__(self, username, password, servername):
        self._username = username
        self._password = password
        self._servername = servername
        self._client = None
        self._connect()

    def run_commands_on_shell(self, command_list, enable_required=True):
        try:
            shell = self._client.invoke_shell()
        except SSHException as e:
            print ('Error using current ssh connection. Trying to create connection over new one ')
            self._client = None
            self._connect()
            shell = self._client.invoke_shell()
        if (enable_required):
            shell.send('{}\r\n'.format('enable'))
            shell.recv(1024)
            shell.send('{}\r\n'.format(self._password))
            shell.recv(1024)

        for command in command_list:
            shell.send('{}\r\n'.format(command))
            print(shell.recv(1024))

    def delete_logs(self):
        command_list = [
            'configure terminal',
            'access-log',
            'exit',
            'exit'
        ]
        self.run_commands_on_shell(command_list)


    def show_access_logs(self):
        command_list = [
            'show access-log format brief',
            'exit'
        ]
        self.run_commands_on_shell(command_list,enable_required=False)
