import os

print os.getcwd();




f=open('test.txt', 'r')
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

for i in range(0,len(ip)-1):
	key=(ip[i])%2048;
	counter=0;
	Stride[key]=[0,0,0];

stride1=0;
stride2=0;


correct=0;
incorrect=0;
count=0;

for i in range(0,len(ip)):
     key=(ip[i])%2048;
     answer=loadval[i];
     value=Stride[key];
     last_value=value[0];
     stride1=value[1]
     stride2=value[2];
     predict=last_value+stride2;


     if (answer==predict):
     	correct=correct+1;
     else:
        incorrect=incorrect+1;
     temp=((answer)-(last_value));
     temp=temp&(0xFF);

     if(temp==stride1):
        stride2=temp;
     stride1=temp;
     Stride[key]=[loadval[i],stride1,stride2];        
   
     
total=correct+incorrect;
accuracy=(correct*100)/total;
print accuracy;
print Stride;

