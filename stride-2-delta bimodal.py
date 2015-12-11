import os

print os.getcwd();

tsize=2048;
counter_max=3
counter_thres=1

f=open('radixsort.txt', 'r')
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
    
		



Stride={};

for i in range(0,len(ip)):
	key=(ip[i])%tsize;
	count=0;
	Stride[key]=[0,0,0,0];

stride1=0;
stride2=0;

counter=0;

pcorrect=0;
pincorrect=0;
npcorrect=0;
npincorrect=0;


for i in range(0,len(ip)):
     key=(ip[i])%tsize;
     answer=loadval[i];
     value=Stride[key];
     last_value=value[0];
     stride1=value[1]
     stride2=value[2];
     counter=value[3];
     predict=last_value+stride2;

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

     temp=answer-last_value;
     temp=temp&(0xFF)
     if(temp==stride1):
        stride2=temp;
     stride1=temp;
     Stride[key]=[loadval[i],stride1,stride2,counter];  
                        



total=pcorrect+pincorrect;
accuracy=(pcorrect*100)/total;
print accuracy;
cov=(pcorrect*100)/len(ip);

print cov;

print Stride;

