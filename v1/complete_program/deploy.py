import paramiko
import os

class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are 
            created under target.
        '''
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

HOST = 'gerty.cobotmakerspace.org'
PORT = 22
USERNAME = 'mitchellsparrow'
PASSWORD = 'coolcars'

transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USERNAME, password=PASSWORD)
sftp = MySFTPClient.from_transport(transport)
sftp.mkdir('/home/mitchellsparrow/tmp/complete_program/', ignore_existing=True)
sftp.put_dir("C:\\Users\\mitch\\Documents\\Mitch Files\\University\\Postgrad\\Dissertation\\Code\\Robot_Control\\v1\\complete_program", '/home/mitchellsparrow/tmp/complete_program/')
sftp.close()