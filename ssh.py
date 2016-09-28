import paramiko
from util import cmd_block
from util import sftp_get
import simplejson
import re

# ------ssh parameters------
ip       = "192.168.3.248"
port     = 22
username = "root"
password = "alpine"
session_timeout = 60

#------set up ssh client------
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(ip,port,username=username,password=password)


#------get install app plist and analyse------
cmd_block(client,'cp /var/mobile/Library/MobileInstallation/LastLaunchServicesMap.plist /var/mobile/Library/MobileInstallation/temp.plist')
cmd_block(client,'plutil -convert json /var/mobile/Library/MobileInstallation/temp.plist')
json = cmd_block(client, 'cat /var/mobile/Library/MobileInstallation/temp.json')
cmd_block(client,'rm /var/mobile/Library/MobileInstallation/temp.plist')
cmd_block(client,'rm /var/mobile/Library/MobileInstallation/temp.json')
json_dict = simplejson.loads(json)
app_dict = json_dict['User']
app_options = dict()

i=0
for app in app_dict.keys():
    print i,' : ',app
    app_options[i]=app
    i=i+1

app_id = int(raw_input("plz choose which app to analyse: "))
print 'you have choose [',app_id,']',app_options[app_id]


#------get clutch -i result-----
clutch_i = cmd_block(client,'clutch -i')
pat = re.compile(r'.+<(.+)>')

clutch_app_id=-1
for line in clutch_i.split('\n'):
    print line
    m = pat.match(line)
    if m:
        if m.group(1)==app_options[app_id]:
            clutch_app_id = int(line[0])

if clutch_app_id != -1 :
    clutch_success = False
    print 'the application is encrypted, and use clutch to decrypt'
    cmd = 'clutch -d '+str(clutch_app_id)
    out = cmd_block(client,cmd)
    pat = re.compile(r'DONE:\s(.+ipa)')
    for line in out.split('\n'):
        print line
        m = pat.match(line)
        if m:
            clutch_success = True
            print m.group(1)
            sftp_get(ip,port,username,password,m.group(1),'./temp/decrypted.ipa')
    if not clutch_success:
        print 'clutch failed'
        exit(-1)

else:
    print 'the application is not encrypted'





client.close()