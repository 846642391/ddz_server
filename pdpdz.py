def _3n(li):
	li=sorted(li);
	if((li[0]<<4)==((li[1]<<4)-1)and(li[0]<<4)==((li[2]<<4)-2)and((li[2]<<4)<0xe)):
		return 3;
	return 1;
def _31(li):
	li=sorted(li);
	if((li[0]<<4)==(li[1]<<4)and(li[0]<<4)==(li[2]<<4)):
		return 3;
	return 1;
def _th(li):
	li=sorted(li);
	if(0xe0 in li or 0xf0 in li):return 1;
	li=[i&0xf for i in li];
	if(li[0]==li[1]and li[0]==li[2]):return 3;
	return 1;
def _e0(li):
	if(0xe0 in li):return 2;
	return 1;
def _f0(li):
	if(0xf0 in li):return 2;
	return 1;
def verify(li):
	ret=1;
	fl=[_3n,_31,_th,_e0,_f0];
	for i in fl:
		ret*=i(li);
	return ret;