import os
import numpy as np
import collections

tsize=2048;
counter_max=3
counter_thres=1

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



LVPT={};

for i in range(0,len(ip)):
	key=((ip[i]))%tsize;
	count=0;
	LVPT[key]=[0,0];

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;

for i in range(0,len(ip)):
    key=((ip[i]))%tsize;
    answer=loadval[i];
    val=LVPT[key];
    predict=val[0];
    counter=val[1];




    if(counter>counter_thres):
        if(answer==predict):
            pcorrect=pcorrect+1;
            counter=counter+1;
            if(counter>=counter_max):
                
                counter=counter_max;

        elif(answer!=predict):
            pincorrect=pincorrect+1;
            counter=counter-1;
            if(counter<=0):
                 counter=0;

    elif(counter<=counter_thres):

        if(answer==predict):
            npcorrect=npcorrect+1;
            counter=counter+1;
            if(counter>=counter_max):
               counter=counter_max;

        elif(answer!=predict):
            npincorrect=npincorrect+1;
            counter=counter-1;
            if(counter<=0):
                counter=0;

    LVPT[key]=[loadval[i],counter];            

        	



total=pcorrect+pincorrect;

print LVPT;

accuracy=(pcorrect*100)/total;
print (accuracy);

ptotal=pcorrect+npincorrect;
cov=(pcorrect*100)/len(ip);

print (cov);


