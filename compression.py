import os
class Nodes:
    def __init__(self,val,prio):        
        self.val = val
        self.prio = prio 
        self.left = None
        self.right = None
        
class minheap:
    def __init__(self):
        self.a = []
        
    def getsize(self):
        return len(self.a)
    
    def insert(self,node):
        self.a.append(node)
        ci = len(self.a) - 1
        pi = (ci-1)//2
        while(pi>=0):
            if self.a[pi].prio>self.a[ci].prio:
                self.a[pi],self.a[ci] = self.a[ci],self.a[pi]
            else:
                break
            ci = pi
            pi = (ci-1)//2
        
    def remove(self):
        if len(self.a) == 0:
            return "Empty"
        self.a[0],self.a[-1] = self.a[-1],self.a[0]
        ele = self.a.pop()
        te = len(self.a)
        pi = 0
        while(1):
            if 2*pi+2<te:
                if self.a[2*pi+1].prio <= self.a[2*pi+2].prio:
                    if self.a[pi].prio<self.a[2*pi+1].prio:
                        break
                    else:
                        self.a[pi],self.a[2*pi+1] = self.a[2*pi+1],self.a[pi]
                        pi = 2*pi+1
                else:
                    if self.a[pi].prio < self.a[2*pi+2].prio:
                        break
                    else:
                        self.a[pi],self.a[2*pi+2] = self.a[2*pi+2],self.a[pi]
                        pi = 2*pi+2
            elif 2*pi + 1<te:
                if self.a[pi].prio<self.a[2*pi+1].prio:
                    break
                else:
                    self.a[pi],self.a[2*pi+1] = self.a[2*pi+1],self.a[pi]
                    pi = 2*pi+1
            else:
                break
        return ele
        
class huffmanCoding:
    def __init__(self,path):
        self.path = path
        self.codes = {}
        self.reverse_codes = {}
        
    def frequency_dictionary(self,s):
        d = {}
        for i in range(len(s)):
            if s[i] not in d:
                d[s[i]] = 0
            d[s[i]] += 1
        return d
        
        
    def build_tree(self,pq):
        
        while(pq.getsize()>1):
            bn1 = pq.remove()
            bn2 = pq.remove()
            newNode = Nodes(None,bn1.prio + bn2.prio)
            newNode.left = bn1
            newNode.right = bn2
            pq.insert(newNode)
            
        root = pq.remove()
        return root
        
    def getting_codes(self,root,s,codes):
        if root.val is not None:
            codes[root.val] = s
            return

        self.getting_codes(root.left,s + "0",codes)
        self.getting_codes(root.right,s + "1",codes)
        
        return codes
        
    def compress_text(self,codes,text):
        compress = ""
        for i in range(len(text)):
            compress = compress + codes[text[i]]
        return compress
        
    def padded(self,s):
        
        padding_amount = 8 - len(s)%8
        for i in range(padding_amount):
            s += "0"
            
        bn = bin(padding_amount).replace("0b","")
        padded_num= "0"*(8-len(bn)) + bn

        s = padded_num + s
        return s
        
    
    def compress(self):
        file_name = self.path.split(".")[0]
        output_file_name =  file_name + "_compressed"  + ".txt"
        
        with open(self.path,"r+",errors="ignore") as file, open(output_file_name,"wb") as output:
            text = file.read()
            text = text.rstrip()

            freq_dict = self.frequency_dictionary(text)
            
            pq = minheap()
            
            for char,freq in freq_dict.items():
                node = Nodes(char,freq)
                pq.insert(node)
                
            root = self.build_tree(pq)
            
            self.codes = self.getting_codes(root,"",self.codes)
            
            compressed = self.compress_text(self.codes,text)
            
            padded_compressed = self.padded(compressed)
            
            bytes_array = []
            for i in range(0,len(padded_compressed),8):
                bytes_array.append(int(padded_compressed[i:i+8],2))

            compressed_into_bytes = bytes(bytes_array)
          
            output.write(compressed_into_bytes)

            print("compressed")

            
            return output_file_name
            
    def remove_padding(self,s):
        
        padded_amount = s[:8]
        num = int(padded_amount,2)
        s = s[8:]
        return s[:len(s)-num]
        
    def get_text(self,bits):
      
        text = ""
        prev = 0
        i = 1
        while(i<len(bits)):
            if bits[prev:i] in self.reverse_codes:
                text = text + self.reverse_codes[bits[prev:i]]
                prev = i
            i = i+1
        return text
                
    def decompress(self,input_path):
        
        file_name,file_extension = input_path.split(".")
        output_file_name = file_name + "_decompressed" + ".txt"
        
        with open(input_path,"rb") as file , open(output_file_name,"w") as output:
            
            bitstring = ""
            # print(file.read())
            byte = file.read(1)
            while(byte):
                byte = ord(byte)
                bn = bin(byte).replace("0b","")
                fbn = "0"*(8-len(bn)) + bn
                bitstring += fbn
                byte = file.read(1)
                
            bits = self.remove_padding(bitstring)

            
            for key,val in self.codes.items():
                self.reverse_codes[val] = key

            actualtext = self.get_text(bits)


            # print(self.codes)
            # print(actualtext)

            output.write(actualtext)

            print("decompressed")

        return 

    

path = "/Users/DELL/OneDrive/Desktop/compress/sample_file.txt"
h = huffmanCoding(path)
compressed_file = h.compress()
h.decompress(compressed_file)
            
            
            
            
            
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        