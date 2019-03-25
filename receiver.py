import socket
import time
import struct
import sys
import collections

def recvFromRadar():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    radar_address = ('', 50000)
    sock.bind(radar_address)
    pack=0
    while True:
        # print(pack)
        # print('DEBUG')
        pack+=1
        msg1, addr = sock.recvfrom(8192)
        if msg1[0] != 1 or msg1[2] != 1:
            continue

        msg2, addr = sock.recvfrom(8192)
        if msg2[0] != 2 or msg2[2] != 2:
            continue
        # msg_list.append(msg)
        # print(type(msg), type(addr))
        if(msg1[0]==1 and msg1[2] ==1 and msg2[0]==2 and msg2[2] ==2):
            msg= msg1[4:]+msg2[4:]
            targetcount = struct.unpack('<f',msg[0:4])[0]
            Type = struct.unpack('<f',msg[4:8])[0]
            Version = struct.unpack('<f',msg[8:12])[0]
            curtime = struct.unpack('<f', msg[12:16])[0]
            print({'Pack':pack,'Count':targetcount, 'Type':Type, 'Version':Version, 'Curtime':curtime})
            if targetcount<1:
                # sys.stdout.write('.')
                sys.stdout.flush()
                # continue
            # print('DEBUG')
            
            target_data=[]
            for i in range(max(int(targetcount), 1)):
                sector=msg[16+i*60:16+(i+1)*60]
                # print(len(sector))
                
                dic = collections.OrderedDict({
                    'target_id':struct.unpack('<f',sector[0:4])[0],
                    'n_time':struct.unpack('<f',sector[4:8])[0],
                    'version':struct.unpack('<f',sector[8:12])[0],
                    'r':struct.unpack('<f',sector[12:16])[0],
                    'av':struct.unpack('<f',sector[16:20])[0],
                    'v':struct.unpack('<f',sector[20:24])[0],
                    'x':struct.unpack('<f',sector[24:28])[0],
                    'y':struct.unpack('<f',sector[28:32])[0],
                    'z':struct.unpack('<f',sector[32:36])[0],
                    'vx':struct.unpack('<f',sector[36:40])[0],
                    'vy':struct.unpack('<f',sector[40:44])[0],
                    'vz':struct.unpack('<f',sector[44:48])[0],
                    'ax':struct.unpack('<f',sector[48:52])[0],
                    'ay':struct.unpack('<f',sector[52:56])[0],
                    'az':struct.unpack('<f',sector[56:60])[0],
                })
                print({'data':dic})
                target_data.append(dic)
            print(target_data)
            #rp.report({'data':target_data})
        else:
            print("sequence error", msg1[0:3], msg2[0:3])
           

    # print(msg_list)


if __name__ == '__main__':
    print('start receive the radar data...')
    recvFromRadar()