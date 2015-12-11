import os

print os.getcwd();

f=open('radixsort.txt', 'r')
table=[]
for line in f:
    table.append(line);

tsize=2048;
counter_max=3
counter_thres=1


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

for i in range(0,len(ip)): 
    key=(ip[i])%tsize;
    FCM[key]=[0,0,0,0,0];


hash1=0;hash2=0;hash3=0;hash4=0;

for i in range(0,2048):
    Lookup[i]=0;

pcorrect=0;
pincorrect=0;

counter=0;

npcorrect=0;
npincorrect=0;


for i in range(0,len(ip)):
    key=(ip[i])%tsize;
    answer=loadval[i];

    fcmvalue=FCM[key];

    
    hash1=fcmvalue[0];
    hash2=fcmvalue[1];
    hash3=fcmvalue[2];
    hash4=fcmvalue[3];
    counter=fcmvalue[4];

    line= ((hash1)^(hash2*2)^(hash3*4)^(hash4*8));
    #line=line&(0xFF);
    


    predict=Lookup[line];

    if(counter>counter_thres):
        if(answer==predict):
            pcorrect=pcorrect+1;
            counter=counter+1;
            if(counter>counter_max):
                counter=counter_max;
        elif(answer!=predict):
            pincorrect=pincorrect+1;
            counter=counter-1;
            if(counter<0):
                 counter=0;

    elif(counter<=counter_thres):

        if(answer==predict):
            npcorrect=npcorrect+1;
            counter=counter+1;
            if(counter>counter_max):
               counter=counter_max;

        elif(answer!=predict):
            npincorrect=npincorrect+1;
            counter=counter-1;
            if(counter<0):
                counter=0;
    
    

    

    Lookup[line]=loadval[i];

    hash4=hash3;
    hash3=hash2;
    hash2=hash1;
    hash1=(answer & 0xFF)^((answer & 0xFF00)>>8)^((answer & 0xFF0000)>>16)^((answer & 0xFF000000)>>24) ;
        
    FCM[key]=[hash1,hash2,hash3,hash4,counter];


accuracy=(pcorrect*100)/(pcorrect+pincorrect);
print accuracy;

cov=(pcorrect*100)/len(ip);

print cov;

