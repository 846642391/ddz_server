ERR=("0",0,0);
GP=("-1",0,0);
X2L=["4"];
X6L=[("4",0,14)];
ZD="4";
def g(li):
	rl=[0 for i in range(16)];
	for i in li:
		rl[i>>4]+=1;
	return rl;
def _4(li):
	if(len(li)!=4 and len(li)!=2):return ERR;
	rl=g(li);
	if(rl[14]and rl[15]):return("4",0,14);
	for i in range(len(rl)):
		if(rl[i]==4):return("4",0,i);
	return ERR;
def _3(li):
	if(len(li)!=3):return ERR;
	rl=g(li);
	for i in range(len(rl)):
		if(rl[i]==3):return("3",0,i);
	return ERR;
def _2(li):
	if(len(li)!=2):return ERR;
	rl=g(li);
	for i in range(len(rl)):
		if(rl[i]==2):return("2",0,i);
	return ERR;
def _1(li):
	if(len(li)!=1):return ERR;
	rl=g(li);
	for i in range(len(rl)):
		if(rl[i]==1):return("1",0,i);
	return ERR;
def _4_2(li):
	if(len(li)!=6):return ERR;
	rl=g(li);
	for i in range(len(rl)):
		if(rl[i]==4):return("4_2",0,i);
	return ERR;
def _4_4(li):
	if(len(li)!=8):return ERR;
	rl=g(li);
	mainvalue=0;
	dzyz=0;
	for i in range(len(rl)-1,0,-1):
		if(rl[i]==4 and mainvalue==0):mainvalue=i;
		elif(rl[i]==2):dzyz+=1;
		elif(rl[i]==4):dzyz+=2;
	if(mainvalue==0 or dzyz<2):return ERR;
	return("4_4",0,mainvalue);
def _3_1(li):
	if(len(li)!=4):return ERR;
	rl=g(li);
	for i in range(len(rl)):
		if(rl[i]==3):return("3_1",0,i);
	return ERR;
def _3_2(li):
	if(len(li)!=5):return ERR;
	rl=g(li);
	mainvalue=0;
	dzyz=0;
	for i in range(len(rl)):
		if(rl[i]==3):mainvalue=i;
		elif(rl[i]==2):dzyz+=1;
	if(mainvalue==0 or dzyz<1):return ERR;
	return("3_2",0,mainvalue);
def _n(li):
	if(len(li)<5 or len(li)>12):return ERR;
	rl=g(li);
	mainvalue=0;
	length=0;
	dk=0;
	for i in range(len(rl)):
		if(mainvalue==0 and rl[i]==1):
			length+=1;
			mainvalue=i;
		elif(rl[i]==1):length+=1;
		elif(length):dk=1;
		if(dk and rl[i]):return ERR;
		if(i>12 and rl[i]):return ERR;
	if(length<5):return ERR;
	return("n",length,mainvalue);
def _2n(li):
	if(len(li)<6 or len(li)%2):return ERR;
	rl=g(li);
	mainvalue=0;
	length=0;
	dk=0;
	for i in range(len(rl)):
		if(mainvalue==0 and rl[i]==2):
			length+=1;
			mainvalue=i;
		elif(rl[i]==2):length+=1;
		elif(length):dk=1;
		if(dk and rl[i]):return ERR;
		if(i>12 and rl[i]):return ERR;
	if(length<3):return ERR;
	return("2n",length,mainvalue);
def _3n(li):
	if(len(li)<6 or len(li)%3):return ERR;
	rl=g(li);
	mainvalue=0;
	length=0;
	dk=0;
	for i in range(len(rl)):
		if(mainvalue==0 and rl[i]==3):
			length+=1;
			mainvalue=i;
		elif(rl[i]==3):length+=1;
		elif(length):dk=1;
		if(dk and rl[i]):return ERR;
		if(i>12 and rl[i]):return ERR;
	if(length<2):return ERR;
	return("3n",length,mainvalue);
def _3n_n(li):
	if(len(li)<8 or len(li)%4):return ERR;
	mainvalue=0;
	length=0;
	dzyz=0;
	dk=0;
	h=0;
	rl=g(li);
	for i in range(len(rl)):
		if(mainvalue==0 and rl[i]>=3 and not dk):
			length+=1;
			mainvalue=i;
			h=1;
			if(rl[i]==4):dzyz+=1;
		elif(rl[i]>=3 and not dk):
			length+=1;
			h=1;
			if(rl[i]==4):dzyz+=1;
		elif(rl[i]>=3):
			dzyz+=rl[i];
		elif(rl[i]==2):
			if(h):dk=1;
			dzyz+=2;
		elif(rl[i]==1):
			if(h):dk=1;
			dzyz+=1;
		elif(rl[i]==0):
			if(h):dk=1;
		if(i==12):dk=1;
	if(dzyz!=length or length<2):return ERR;
	return("3n_n",length,mainvalue);
def _3n_n_t(li):
	if(len(li)<8 or len(li)%4):return ERR;
	mainvalue=0;
	length=0;
	dzyz=0;
	dk=0;
	mx=max(li)>>4;
	zd=0
	rl=g(li);
	h=0;
	for i in range(len(rl)):
		if(mainvalue==0 and rl[i]==4 and not zd):
			zd=1;
			dzyz+=4;
		elif(rl[i]==4 and i==mx and not zd):
			zd=1;
			dzyz+=4;
		elif(mainvalue==0 and rl[i]>=3 and not dk):
			length+=1;
			mainvalue=i;
			h=1;
			if(rl[i]==4):dzyz+=1;
		elif(rl[i]>=3 and not dk):
			length+=1;
			h=1;
			if(rl[i]==4):dzyz+=1;
		elif(rl[i]>=3):
			dzyz+=rl[i];
		elif(rl[i]==2):
			if(h):dk=1;
			dzyz+=2;
		elif(rl[i]==1):
			if(h):dk=1;
			dzyz+=1;
		elif(rl[i]==0):
			if(h):dk=1;
		if(i==12):dk=1;
	if(dzyz!=length or length<2):return ERR;
	return("3n_n",length,mainvalue);
def _3n_2n(li):
	if(len(li)<10 or len(li)%5):return ERR;
	rl=g(li);
	mainvalue=0;
	length=0;
	dk=0;
	dzyz=0;
	for i in range(len(rl)):
		if(mainvalue==0 and rl[i]==3):
			length+=1;
			mainvalue=i;
		elif(rl[i]==3):length+=1;
		elif(rl[i]==4):dzyz+=2;
		elif(rl[i]==2):dzyz+=1;
		elif(length):dk=1;
		if(dk and(rl[i]==1 or rl[i]==3)):return ERR;
		if(i>12 and rl[i]>=3):return ERR;
	if(length<2):return ERR;
	return("3n_2n",length,mainvalue);
def verify(li):
	ret=ERR;
	fi=[_1,_2,_3,_4,_3_1,_3_2,_4_2,_4_4,_n,_2n,_3n,_3n_n,_3n_n_t,_3n_2n];
	i=0;
	while(i<len(fi)and ret==ERR):
		ret=fi[i](li);
		i+=1;
	return ret;