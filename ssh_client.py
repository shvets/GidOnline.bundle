#!/usr/bin/python

from StringIO import StringIO
import paramiko
import getpass

# setup logging
#paramiko.util.log_to_file('demo_simple.log')

class SshClient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, port, username, password, key=None, passphrase=None):
        self.username = username
        self.password = password

        self.ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        self.ssh.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)

    def close(self):
        if self.ssh is not None:
            self.ssh.close()
            self.ssh = None

    def execute(self, command, sudo=False):
        feed_password = False

        if sudo and self.username != "root":
            command = "%s" % command
            feed_password = self.password is not None and len(self.password) > 0

        stdin, stdout, stderr = self.ssh.exec_command(command)

        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()

        return {
            'out': stdout.readlines(),
            'err': stderr.readlines(),
            'retval': stdout.channel.recv_exit_status()
        }

if __name__ == "__main__":
    username = 'alex'
    host = '10.0.1.37'

    password = getpass.getpass('Password for %s@%s: ' % (username, host))

    client = SshClient(host=host, port=22, username=username, password=password)

    try:
       ret = client.execute('dmesg', sudo=True)
       print "  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"]
    finally:
      client.close()
