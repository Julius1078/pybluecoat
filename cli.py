from bluecoat import BluecoatServer
from configparser import ConfigParser


config = ConfigParser()
config.read('./config.ini')
username = config['DEFAULT'].get('Username')
password = config['DEFAULT'].get('Password')

bc = BluecoatServer(username, password, 'axbfbcproxy3.central.inditex.grp')

bc.delete_logs()
bc.show_access_logs()


