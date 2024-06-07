import pyzagi as pz

import sys
sys.path.append('D:/GitHub/')

# Those are personal values. Replace it
from mysecrets.pztg.passcodes import (
    TOKEN, BOT_USERNAME,
    baseURL,
    clientid,
    clientsecret)

bizagibpm = pz.ConnectionBPM(
                baseURL,
                {'id':clientid, 'secret':clientsecret}
            )

print(bizagibpm.get_processes())