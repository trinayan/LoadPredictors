import os

print os.getcwd();



f=open('linpack.txt', 'r')
table=[]
for line in f:
    table.append(line);

ip=[];
loadval=[];
for i in range(3,len(table)-1):
     stringvalue=table[i];
     b=stringvalue[0:13];
     b=int(b,16);
     ip.append(b);

     c=stringvalue[-22:];
     c=int(c);
     loadval.append(c);



FCM={};
Lookup={};

for i in range(0,len(ip)-1): 
    key=(ip[i])%2048;
    FCM[key]=[0,0,0,0];

hash1=0;hash2=0;hash3=0;hash4=0;

for i in range(0,2049):
    Lookup[i]=0;

correct=0;
incorrect=0;

for i in range(0,len(ip)):
    key=(ip[i])%2048;
    answer=loadval[i];

    fcmvalue=FCM[key];

    hash1=fcmvalue[0];
    hash2=fcmvalue[1];
    hash3=fcmvalue[2];
    hash4=fcmvalue[3];

    line= (hash1)^(hash2*2)^(hash3*4)^(hash4*8);

    

    prediction=Lookup[line];

    if (answer==prediction):
    	correct=correct+1;
    else:
        incorrect=incorrect+1;

    Lookup[line]=loadval[i];
    hash4=hash3;
    hash3=hash2;
    hash2=hash1;
    hash1=(answer & 0xFF)^((answer & 0xFF00)>>8)^((answer & 0xFF0000)>>16)^((answer & 0xFF000000)>>24) ;
   
    
    FCM[key]=[hash1,hash2,hash3,hash4]



accuracy=(correct*100)/(correct+incorrect);
print accuracy;
print FCM
print Lookup;
