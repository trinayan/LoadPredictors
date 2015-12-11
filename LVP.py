import os

print os.getcwd();

'''f=open('instructionpoint.txt', 'r')
ip=[];
for line in f:
	ip.append(line);

for i in range(0,len(ip)) :
    (ip[i]>>2)=int((ip[i]>>2),16);	

print ip[0];

f=open('loadval.txt', 'r')
loadval=[];
for line in f:
	loadval.append(line)

for i in range(0,len(loadval)):
	if(loadval[i]=='(nil)  \n'):
		loadval[i]="0";
	loadval[i]=int(loadval[i],16);	
		

print loadval[0];'''




f=open('radixsort.txt', 'r')
table=[]
for line in f:
    
	   table.append(line);


print len(table);

ip=[];
loadval=[];
loads=[]
for i in range(3,len(table)-1):
     stringvalue=table[i];
     b=stringvalue[0:13];
     loads.append(b);
     
     b=int(b,16);
     ip.append(b);

     c=stringvalue[-22:];
     c=int(c);
     loadval.append(c);
     




LVPT={};

for i in range(0,len(ip)):
	key=(ip[i])%2048;
	counter=0;
	LVPT[key]=0;

correct=0;
incorrect=0;
count=0;
for i in range(0,len(ip)):
     key=(ip[i]%2048);
     answer=loadval[i];
     predict=LVPT[key];


     if (answer==predict):
       
     	correct=correct+1;
     else:
        incorrect=incorrect+1;
     LVPT[key]=loadval[i];  

total=correct+incorrect;
accuracy=(correct*100)/total;
print accuracy;

print LVPT;
