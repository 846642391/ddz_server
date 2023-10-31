from flask import *;
from datetime import *;
from time import sleep;
import re;
import sys;
import random;
from threading import Thread;
import pdp;
import logging;
from configparser import ConfigParser;
import os;
import pdpdz;
import copy;




cardt={
	0x10:"3♠",0x11:"3♥",0x12:"3♣",0x13:"3♦",
	0x20:"4♠",0x21:"4♥",0x22:"4♣",0x23:"4♦",
	0x30:"5♠",0x31:"5♥",0x32:"5♣",0x33:"5♦",
	0x40:"6♠",0x41:"6♥",0x42:"6♣",0x43:"6♦",
	0x50:"7♠",0x51:"7♥",0x52:"7♣",0x53:"7♦",
	0x60:"8♠",0x61:"8♥",0x62:"8♣",0x63:"8♦",
	0x70:"9♠",0x71:"9♥",0x72:"9♣",0x73:"9♦",
	0x80:"10♠",0x81:"10♥",0x82:"10♣",0x83:"10♦",
	0x90:"J♠",0x91:"J♥",0x92:"J♣",0x93:"J♦",
	0xa0:"Q♠",0xa1:"Q♥",0xa2:"Q♣",0xa3:"Q♦",
	0xb0:"K♠",0xb1:"K♥",0xb2:"K♣",0xb3:"K♦",
	0xc0:"A♠",0xc1:"A♥",0xc2:"A♣",0xc3:"A♦",
	0xd0:"2♠",0xd1:"2♥",0xd2:"2♣",0xd3:"2♦",
	0xe0:"joker",0xf0:"JOKER"
};

cardl=[
	0x10,0x11,0x12,0x13,0x20,0x21,0x22,0x23,0x30,0x31,0x32,0x33,0x40,0x41,0x42,0x43,
	0x50,0x51,0x52,0x53,0x60,0x61,0x62,0x63,0x70,0x71,0x72,0x73,0x80,0x81,0x82,0x83,
	0x90,0x91,0x92,0x93,0xa0,0xa1,0xa2,0xa3,0xb0,0xb1,0xb2,0xb3,0xc0,0xc1,0xc2,0xc3,
	0xd0,0xd1,0xd2,0xd3,0xe0,0xf0
];



app=Flask(__name__);
app.secret_key="secret_key";
log=logging.getLogger('werkzeug');
log.setLevel(logging.WARNING);
password="";



player_list=[None,None,None];
start_time=int(datetime.now().timestamp()*1000);
msg=[];
msgid=0;
is_start=0;
is_d_start=0;
sub_process=(-1,-1);
end_time=0;
time_1=20;
time_2=20;
time_3=30;
time_0=3;
dzp=[0x00,0x00,0x00];
dzt=-1;
tempdz=[-1,-1,-1];
gp=2;
cp=[];
playercard=pdp.ERR;
nplayercard=[];
lc=0;
bsc=15;
bs=bsc;
dzj=0;
jbs=[-1,-1,-1];
is_fst=1;
qdzid=1;
df=1;
dzcp=0;
nmcp=0;
ip="0.0.0.0";
port=80;
gsave=1;
modifynotice="";
saves=[];
playerban=[];
ipban=[];
enablewhitelist=0;
playerwhite=[];
ipwhite=[];
fnm="0000_00_00_00_00_00.html";
bjini="[option]\nip=0.0.0.0\nport=80\ndf=1\nbs=15\npassword=\ntime_1=20\ntime_2=20\ntime_3=30\ntime_0=3\ngsave=1\nplayerban=\nipban=\nenablewhitelist=0\nplayerwhite=\nipwhite=\n";



def readini(cz=0):
	global ip,port,df,bsc,password,gsave,playerban,ipban,enablewhitelist,playerwhite,ipwhite;
	conf=ConfigParser();
	inifile=sys.argv[1]if len(sys.argv)>=2 else "ddz.ini";
	if(not os.path.exists(inifile)):
		logging.warning("Given initialization file do not exist. Created.");
		t=open(inifile,"w",encoding="utf-8");
		t.write(bjini);
		t.close();
	conf.read(inifile,encoding="utf-8");
	if(conf.has_section("option")):
		if(not cz):
			ip=conf["option"]["ip"]if conf.has_option("option","ip")else"0.0.0.0";
			port=conf["option"].getint("port")if conf.has_option("option","port")else 80;
			print("Process is running on %s:%d"%(ip,port));
		df=conf["option"].getint("df")if conf.has_option("option","df")else 1;
		bsc=conf["option"].getint("bs")if conf.has_option("option","bs")else 15;
		time_0=conf["option"]["time_0"]if conf.has_option("option","time_0")else 3;
		time_1=conf["option"]["time_1"]if conf.has_option("option","time_1")else 20;
		time_2=conf["option"]["time_2"]if conf.has_option("option","time_2")else 20;
		time_3=conf["option"]["time_3"]if conf.has_option("option","time_3")else 30;
		password=conf["option"]["password"]if conf.has_option("option","password")else"";
		gsave=conf["option"].getint("gsave")if conf.has_option("option","gsave")else 1;
		playerban=conf["option"]["playerban"].split()if conf.has_option("option","playerban")else[];
		ipban=conf["option"]["ipban"].split()if conf.has_option("option","ipban")else[];
		enablewhitelist=conf["option"].getint("enablewhitelist")if conf.has_option("option","enablewhitelist")else 0;
		playerwhite=conf["option"]["playerwhite"].split()if conf.has_option("option","playerwhite")else[];
		ipwhite=conf["option"]["ipwhite"].split()if conf.has_option("option","ipwhite")else[];
	return;

def ASync(f):
	def wrapper(*args,**kwargs):
		thr=Thread(target=f,args=args,kwargs=kwargs);
		thr.start();
	return wrapper;

def get_time(ms=0):
	return int(datetime.now().timestamp()*1000)+ms-start_time;

def get_ct(li):
	ret="";
	for i in li:
		if(i==0xf0 or(i!=0xf0 and((i&0xf)==1 or(i&0xf)==3))):
			ret+="[R]%s&#160;[/]"%cardt[i];
		elif(i==0xe0 or(i!=0xe0 and((i&0xf)==0 or(i&0xf)==2))):
			ret+="[B]%s&#160;[/]"%cardt[i];
	return ret;

@ASync
def disconnect_player():
	while(1):
		for i in player_list:
			if(i is None):continue;
			if(get_time()-i["last_active"]>5000 and is_start==0):
				sendsysmsg("sp");
				print("%s left the game."%i["name"]);
				player_list[player_list.index(i)]=None;
		sleep(5);

def getfmsg(msg):
	global msgid;
	time=get_time();
	msgid+=1;
	return {"msg":msg,"time":time,"msgid":msgid};
def sendsysmsg(msg_):
	msg.append(getfmsg(msg_));
	return;
def mpcomment(idx):
	ret="";
	for i in player_list[idx]["card"]:
		ret+="%s "%cardt[i];
	return ret;
def qf(typ=0):
	global player_list,is_start,sub_process,tempdz,end_time,dzp,playercard,nplayercard,gp,lc,bs,is_fst,qdzid,dzj,dzt,jbs,dzcp,nmcp,saves;
	sub_process=(-1,-1);
	is_start=0;
	if(typ==0):
		player_list[0]["is_ready"]=0;
		player_list[0]["card"]=[];
		player_list[0]["is_dz"]=0;
		player_list[0]["is_mp"]=0;
		player_list[1]["is_ready"]=0;
		player_list[1]["card"]=[];
		player_list[1]["is_dz"]=0;
		player_list[1]["is_mp"]=0;
		player_list[2]["is_ready"]=0;
		player_list[2]["card"]=[];
		player_list[2]["is_dz"]=0;
		player_list[2]["is_mp"]=0;
	if(typ==1):
		player_list=[None,None,None];
	tempdz=[-1,-1,-1];
	jbs=[-1,-1,-1];
	gp=2;
	lc=0;
	is_d_start=0;
	player_card=0;
	is_fst=1;
	qdzid=1;
	dzj=0;
	bs=bsc;
	dzcp=0;
	nmcp=0;
	end_time=0;
	dzp=[];
	saves=[];


def saveg(typ=0,nam="",lcd=[],dcd=[],msg=""):
	if(not gsave):
		return;
	saves.append({"typ":typ,"nam":nam,"lcd":lcd,"dcd":dcd,"msg":msg});

def getsavehtml(fnm):
	if(not gsave):return;
	if(not os.path.exists("./replay")):
		os.mkdir("./replay");
	fnm="./replay/"+fnm;
	html=open(fnm,"w",encoding="utf-8");
	html.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>回放</title><style>.bc{color:#000;}.rc{color:#f00;}</style></head><body>");
	for d in saves:
		flcd=get_ct(d["lcd"]).replace("[B]","<span class=\"bc\">").replace("[R]","<span class=\"rc\">").replace("[/]","</span>");
		fdcd=get_ct(d["dcd"]).replace("[B]","<span class=\"bc\">").replace("[R]","<span class=\"rc\">").replace("[/]","</span>");
		if(d["typ"]==0):
			html.write("<div><div><span>玩家:%s</span><span>&#160;剩余:</span><span>%s</span></div><div><span>%s</span></div><div><span>%s</span></div></div>"%(d["nam"],flcd,fdcd,d["msg"]));
		elif(d["typ"]==1):
			html.write("<div><span>%s</span><span>%s</span></div>"%(d["msg"],fdcd));
	html.write("<div><a href=\"https://github.com/846642391/ddz_server\">GitHub</a></div><div><span>要保存此界面，请按下Ctrl+S。</span></div></body></html>");
	html.close();
	return;
@ASync
def game():
	global player_list,is_start,sub_process,tempdz,end_time,dzp,playercard,nplayercard,gp,lc,bs,is_fst,qdzid,dzj,dzt,jbs,dzcp,nmcp,fnm;
	randomcard=random.sample(cardl,54);
	print("Game started.");
	player_list[0]["card"]=sorted(randomcard[0:17],reverse=1);
	player_list[1]["card"]=sorted(randomcard[17:34],reverse=1);
	player_list[2]["card"]=sorted(randomcard[34:51],reverse=1);
	ft=datetime.now().strftime("%Y-%m-%d %H:%M:%S");
	fnm=datetime.now().strftime("%Y_%m_%d_%H_%M_%S.html");
	saveg(1,msg="开始时间:%s"%ft);
	saveg(1,
		msg="玩家: %s(%s)，%s(%s)，%s(%s)"%(
			player_list[0]["name"],player_list[0]["ip"],
			player_list[1]["name"],player_list[1]["ip"],
			player_list[2]["name"],player_list[2]["ip"]
		)
	);
	lcd0=copy.deepcopy(player_list[0]["card"]);
	lcd1=copy.deepcopy(player_list[1]["card"]);
	lcd2=copy.deepcopy(player_list[2]["card"]);
	saveg(0,player_list[0]["name"],lcd0);
	saveg(0,player_list[1]["name"],lcd1);
	saveg(0,player_list[2]["name"],lcd2);
	dzp=randomcard[51:54];
	rl=random.randint(0,2);
	is_start=1;
	sub_process=(1,-1);
	djt=0;
	sendsysmsg("gc");
	player_list[0]["content"]="";
	player_list[1]["content"]="";
	player_list[2]["content"]="";
	for i in range(4):
		if(i==3 and 1 not in tempdz):break;
		while(not tempdz[rl]):rl=(rl+1)%3;
		player_list[rl]["content"]="...";
		sendsysmsg("gb");
		sendsysmsg("sp");
		sub_process=(1,rl);
		end_time=get_time(time_1*1000);
		ftrl=tempdz[rl];
		while(tempdz[rl]==ftrl and end_time-get_time()>=0):
			sleep(.75);
		if(end_time-get_time()<0):
			tempdz[rl]=0;
			player_list[rl]["content"]="不叫"if not djt else"不抢";
			lcd=copy.deepcopy(player_list[rl]["card"]);
			saveg(0,player_list[i]["name"],lcd,[],"不叫"if not djt else"不抢");
		if(tempdz[rl]==4):
			djt=1;
		rl=(rl+1)%3;
	rl=tempdz.index(max(tempdz))if dzj else rl;
	player_list[rl]["is_dz"]=1;
	player_list[rl]["card"]=sorted(player_list[rl]["card"]+dzp,reverse=1);
	ffe=pdpdz.verify(dzp);
	bs*=ffe;
	saveg(1,dcd=dzp,msg="地主牌");
	saveg(1,msg="(倍数*%d)"%ffe if ffe!=1 else"");
	sendsysmsg("sp");
	sendsysmsg("gd");
	sendsysmsg("gc");
	sendsysmsg("gb");
	sub_process=(2,-1);
	end_time=get_time(time_0*1000);
	sleep(time_0);
	end_time=get_time(time_2*1000);
	sub_process=(2,0);
	sendsysmsg("gb");
	for i in range(3):
		player_list[i]["content"]="...";
	while(end_time>=get_time()and any([i==-1 for i in jbs])):
		sleep(1);
		sendsysmsg("sp");
	for i in range(3):
		if(jbs[i]==-1):
			player_list[i]["content"]="不加倍";
			lcd=copy.deepcopy(player_list[rl]["card"]);
			saveg(0,player_list[i]["name"],lcd,[],"不加倍");
	sendsysmsg("gb");
	sub_process=(3,-1);
	end_time=get_time(time_0*1000);
	sleep(time_0);
	sub_process=(3,rl);
	while(1):
		sub_process=(3,rl);
		sendsysmsg("gc");
		sendsysmsg("gb");
		sendsysmsg("sp");
		end_time=get_time(time_3*1000);
		nplayercard=[];
		nlc=lc;
		player_list[rl]["content"]="...";
		if(player_list[rl]["is_mp"]):
			player_list[rl]["content"]+="|明牌:"+get_ct(player_list[rl]["card"]);
		while(end_time-get_time()>=0):
			sleep(.75);
			if(lc>nlc):break;
		else:
			if(gp>=2):
				gvrg=[player_list[rl]["card"][-1]];
				playercard=pdp.verify(gvrg);
				gp=0;
				player_list[rl]["content"]=get_ct(gvrg);
				lcd=copy.deepcopy(player_list[rl]["card"]);
				saveg(0,player_list[i]["name"],lcd,gvrg,"");
				del player_list[rl]["card"][-1];
			else:
				player_list[rl]["content"]="不出";
				lcd=copy.deepcopy(player_list[rl]["card"]);
				saveg(0,player_list[rl]["name"],lcd,[],"不出");
				gp+=1;
		if(len(player_list[rl]["card"])==0):
			break;
		if(player_list[rl]["is_mp"]):
			player_list[rl]["content"]+="|明牌:"+get_ct(player_list[rl]["card"]);
		is_fst=0;
		rl=(rl+1)%3;
	dzsl=0;
	if(player_list[rl]["is_dz"]):
		dzsl=2;	
	player_list[rl]["content"]+=("|地主"if dzsl else"|农民")+"胜利";
	player_list[(rl-1)%3]["content"]=get_ct(player_list[(rl-1)%3]["card"]);
	player_list[(rl+1)%3]["content"]=get_ct(player_list[(rl+1)%3]["card"]);
	dfl=[0,0,0];
	print("Game ended.");
	if(dzsl):
		if(nmcp==0):
			bs<<=1;
			player_list[rl]["content"]+="|春天"
			saveg(1,msg="地主春天(倍数*2)");
		for i in range(3):
			if(player_list[i]["is_dz"]):
				dfl[i]=bs*df*2;
			else:
				dfl[i]=-bs*df;
			player_list[i]["point"]+=dfl[i];
		
	if(not dzsl):
		if(dzcp==1):
			bs<<=1;
			player_list[rl]["content"]+="|春天"
			saveg(1,msg="农民春天(倍数*2)");
		for i in range(3):
			if(player_list[i]["is_dz"]):
				dfl[i]=-bs*df*2;
			else:
				dfl[i]=bs*df;
			player_list[i]["point"]+=dfl[i];
		
	player_list[0]["content"]+="|得分:%d"%dfl[0];
	player_list[1]["content"]+="|得分:%d"%dfl[1];
	player_list[2]["content"]+="|得分:%d"%dfl[2];
	ft=datetime.now().strftime("%Y-%m-%d %H:%M:%S");
	saveg(1,msg="结束时间:%s"%ft);
	saveg(1,msg="本场底分:%d，结束倍数:%d"%(df,bs));
	saveg(1,
		msg="玩家得分: %s:%d分(总计%d分)，%s:%d分(总计%d分)，%s:%d分(总计%d分)"%(
			player_list[0]["name"],dfl[0],player_list[0]["point"],
			player_list[1]["name"],dfl[1],player_list[1]["point"],
			player_list[2]["name"],dfl[2],player_list[2]["point"]
		)
	);
	getsavehtml(fnm);
	sendsysmsg("gf");
	end_time=0;
	sendsysmsg("sp");
	qf(0);
	sendsysmsg("gb");
	sendsysmsg("gc");
	sendsysmsg("gd");
	return;



@app.route("/get_msg",methods=["GET"])
def get_msg():
	t=int(request.args.get("t"));
	lidx=0;
	psmsg=[];
	for i in msg:
		if(i["msgid"]==t):
			lidx=i;
			psmsg=msg[msg.index(i)+1:len(msg)];
			break;
	for i in player_list:
		if(i and i["name"]==session["name"]):
			player_list[player_list.index(i)]["last_active"]=get_time();
	return jsonify(psmsg);

@app.route("/get_player",methods=["GET"])
def get_player():
	res=[{},{},{}];
	si=session["index"];
	res[1]["name"]=player_list[si]["name"];
	res[0]["name"]=player_list[(si-1)%3]["name"]if player_list[(si-1)%3]else"";
	res[2]["name"]=player_list[(si+1)%3]["name"]if player_list[(si+1)%3]else"";
	res[1]["is_dz"]=player_list[si]["is_dz"];
	res[0]["is_dz"]=player_list[(si-1)%3]["is_dz"]if player_list[(si-1)%3]else 0;
	res[2]["is_dz"]=player_list[(si+1)%3]["is_dz"]if player_list[(si+1)%3]else 0;
	res[1]["content"]=player_list[si]["content"];
	res[0]["content"]=player_list[(si-1)%3]["content"]if player_list[(si-1)%3]else"";
	res[2]["content"]=player_list[(si+1)%3]["content"]if player_list[(si+1)%3]else"";
	res[1]["cardr"]=len(player_list[si]["card"]);
	res[0]["cardr"]=len(player_list[(si-1)%3]["card"])if player_list[(si-1)%3]else 0;
	res[2]["cardr"]=len(player_list[(si+1)%3]["card"])if player_list[(si+1)%3]else 0;
	res[1]["point"]=player_list[si]["point"];
	res[0]["point"]=player_list[(si-1)%3]["point"]if player_list[(si-1)%3]else 0;
	res[2]["point"]=player_list[(si+1)%3]["point"]if player_list[(si+1)%3]else 0;
	return res;

@app.route("/get_btn",methods=["GET"])
def get_btn():
	ret=0;
	ps=player_list[session["index"]];
	if((not is_start)and (not ps["is_ready"])):ret|=128;
	if((not is_start)and ps["is_ready"]):ret|=4;
	if(not any([i>0 for i in tempdz])and sub_process==(1,session["index"])):
		ret|=36;
	if(any([i>0 for i in tempdz])and sub_process==(1,session["index"])):
		ret|=68;
	if(sub_process==(2,0)and jbs[session["index"]]==-1):
		ret|=28;
	if(sub_process==(3,session["index"])and gp<2):
		ret|=5;
	if(sub_process==(3,session["index"])and is_fst and not player_list[session["index"]]["is_mp"]):
		ret|=3;
	if(sub_process==(3,session["index"])and gp>=2):
		ret|=1;
	return jsonify({"num":ret});

@app.route("/get_card",methods=["GET"])
def get_card():
	li=[];
	for i in player_list[session["index"]]["card"]:
		li.append({"data":i,"display":cardt[i]});
	return li;

@app.route("/get_dzcard",methods=["GET"])
def get_dzcard():
	if(sub_process[0]>=2):
		return jsonify({"c":get_ct(dzp)});
	return jsonify({"c":""});

@app.route("/get_end_time",methods=["GET"])
def get_end_time():
	return jsonify({"num":(end_time-get_time())//1000 if(end_time-get_time())//1000>0 else 0,"bs":bs});

@app.route("/get_fs",methods=["GET"])
def get_fs():
	session["point"]=player_list[session["index"]]["point"];
	return jsonify({});

@app.route("/gm/ready",methods=["GET"])
def gm_ready():
	if(not is_start):
		if(not player_list[session["index"]]["is_ready"]):
			player_list[session["index"]]["is_ready"]=1;
			player_list[session["index"]]["content"]="已准备";
			sendsysmsg("sp");
			sendsysmsg("gb");
	if(all([i["is_ready"]if i else 0 for i in player_list])):
		game();
	return jsonify({});

@app.route("/gm/cancel",methods=["GET"])
def gm_cancel():
	global gp,lc;
	if(not is_start and player_list[session["index"]]["is_ready"]):
		player_list[session["index"]]["is_ready"]=0;
		player_list[session["index"]]["content"]="";
		sendsysmsg("sp");
		sendsysmsg("gb");
	lcd=copy.deepcopy(player_list[session["index"]]["card"]);
	if(is_start and sub_process==(1,session["index"])and not dzj):
		tempdz[session["index"]]=0;
		player_list[session["index"]]["content"]="不叫";
		saveg(0,player_list[session["index"]]["name"],lcd,[],"不叫");
	if(is_start and sub_process==(1,session["index"])and dzj):
		tempdz[session["index"]]=0;
		player_list[session["index"]]["content"]="不抢";
		saveg(0,player_list[session["index"]]["name"],lcd,[],"不抢");
	if(is_start and sub_process==(2,0)):
		jbs[session["index"]]=1;
		player_list[session["index"]]["content"]="不加倍";
		saveg(0,player_list[session["index"]]["name"],lcd,[],"不加倍");
	if(is_start and sub_process==(3,session["index"])and gp<2):
		player_list[session["index"]]["content"]="不出";
		saveg(0,player_list[session["index"]]["name"],lcd,[],"不出");
		gp+=1;
		lc+=1;
	return jsonify({});

@app.route("/gm/jdz",methods=["GET"])
def gm_jdz():
	global tempdz,dzj,dzt,bs;
	if(is_start and sub_process==(1,session["index"])and not dzj):
		tempdz[session["index"]]=4;
		player_list[session["index"]]["content"]="叫地主";
		lcd=copy.deepcopy(player_list[session["index"]]["card"]);
		saveg(0,player_list[session["index"]]["name"],lcd,[],"叫地主(倍数*2)");
		dzj=1;
		bs<<=1;
		dzt=session["index"];
	return jsonify({});

@app.route("/gm/qdz",methods=["GET"])
def gm_qdz():
	global tempdz,qdzid,bs;
	if(is_start and sub_process==(1,session["index"])and dzj):
		tempdz[session["index"]]=qdzid;
		qdzid+=1;
		bs<<=1;
		player_list[session["index"]]["content"]="抢地主";
		lcd=copy.deepcopy(player_list[session["index"]]["card"]);
		saveg(0,player_list[session["index"]]["name"],lcd,[],"抢地主(倍数*2)");
	return jsonify({});

@app.route("/gm/jb",methods=["GET"])
def jb():
	global bs;
	if(is_start and sub_process==(2,0)and jbs[session["index"]]==-1):
		jbs[session["index"]]=2;
		bs<<=1;
		player_list[session["index"]]["content"]="加倍";
		lcd=copy.deepcopy(player_list[session["index"]]["card"]);
		saveg(0,player_list[session["index"]]["name"],lcd,[],"加倍(倍数*2)");
	return jsonify({});

@app.route("/gm/cjjb",methods=["GET"])
def cjjb():
	global bs;
	if(is_start and sub_process==(2,0)and jbs[session["index"]]==-1):
		jbs[session["index"]]=4;
		bs<<=2;
		player_list[session["index"]]["content"]="超级加倍";
		lcd=copy.deepcopy(player_list[session["index"]]["card"]);
		saveg(0,player_list[session["index"]]["name"],lcd,[],"超级加倍(倍数*4)");
	return jsonify({});

@app.route("/gm/mp",methods=["GET"])
def mp():
	global bs;
	if(is_start and sub_process==(3,session["index"])and is_fst):
		player_list[session["index"]]["is_mp"]=1;
		bs<<=1;
		player_list[session["index"]]["content"]+="|明牌:"+get_ct(player_list[session["index"]]["card"]);
		lcd=copy.deepcopy(player_list[session["index"]]["card"]);
		saveg(0,player_list[session["index"]]["name"],lcd,[],"明牌(倍数*2)");
		sendsysmsg("sp");
		sendsysmsg("gb");
	return jsonify({});


@app.route("/gm/cp",methods=["POST"])
def gm_cp():
	global playercard,lc,gp,bs,dzcp,nmcp,player_list;
	p=request.form.get("p");
	p=p.split();
	p=[int(i)for i in p];
	if(sub_process!=(3,session["index"])):
		return jsonify({"msg":"现在不是您出牌"});
	for i in p:
		if(i not in player_list[session["index"]]["card"]):
			return jsonify({"msg":"不能出没有的牌"});
	if(pdp.verify(p)==pdp.ERR):
		return jsonify({"msg":"不能这样出牌"});
	nv=pdp.verify(p);
	if(gp>=2):
		if(nv!=pdp.ERR):
			playercard=nv;
	else:
		if(nv!=pdp.ERR and((playercard[0]!=pdp.ZD and nv[0]==pdp.ZD)or(playercard[0]==nv[0]and playercard[1]==nv[1]and playercard[2]<nv[2]))):
			playercard=nv;
		else:	
			return jsonify({"msg":"不能出更小的牌或牌型不同的牌"});
	for i in p:
		player_list[session["index"]]["card"].remove(i);
	lc+=1;
	gp=0;
	flg=0;
	if(nv[0]in pdp.X2L or nv in pdp.X2L):
		bs<<=1;
		flg=1;
	if(player_list[session["index"]]["is_dz"]):dzcp+=1;
	else:nmcp+=1;
	player_list[session["index"]]["content"]=get_ct(p);
	lcd=copy.deepcopy(player_list[session["index"]]["card"]);
	saveg(0,player_list[session["index"]]["name"],lcd=lcd,dcd=p,msg="(倍数*2)"if flg else"");
	return jsonify({"msg":""});

@app.route("/login",methods=["GET","POST"])
def login():
	if(request.method=="GET"):
		return render_template("login.html");
	name=request.form.get("name");
	uip=request.remote_addr;
	if(name.lower()in playerban):
		return jsonify({"code":16,"msg":"您的用户名已被服务器封禁!"});
	if(uip in ipban):
		return jsonify({"code":16,"msg":"您的IP地址已被服务器封禁!"});
	if(enablewhitelist):
		flag=0;
		if(not playerwhite and not ipwhite):
			flag=1;
		if(enablewhitelist==1 and(playerwhite or ipwhite)):
			if(name.lower()in playerwhite or uip in ipwhite):
				flag=1;
		if(enablewhitelist==2):
			if(not ipwhite and name.lower()in playerwhite):
				flag=1;
			elif(not playerwhite and uip in ipwhite):
				flag=1;
			elif(name.lower()in playerwhite and uip in ipwhite):
				flag=1;
		if(not flag):
			return jsonify({"code":16,"msg":"您不在服务器白名单内!"});


	if(not re.match("^[0-9a-zA-Z_]{3,16}$",name)):
		return jsonify({"code":1,"msg":"用户名应为3-16位的字母数字或下划线!"});
	for i in player_list:
		if(i and i["name"].lower()==name.lower()):
			return jsonify({"code":4,"msg":"用户名与场内玩家重复,请更换!"});
	if(all(player_list)):
		return jsonify({"code":8,"msg":"场内玩家已满!"});
	session["name"]=name;
	for i in range(len(player_list)):
		if(player_list[i]is None):
			player_list[i]={"name":name,"ip":uip,"is_dz":0,"card":[],"last_active":get_time(),"content":"","is_ready":0,"is_mp":0,"point":session["point"]if"point"in session else 0};
			if("point"not in session):
				session["point"]=0;
			session["index"]=i;
			break;
	sendsysmsg("sp");
	session["ip"]=uip;
	print("User %s(%s) joined the game."%(name,uip));
	return jsonify({"code":0,"msg":"登陆成功!"});

@app.route("/admin",methods=["GET","POST"])
def admin():
	if(request.method=="GET"):
		return render_template("admin.html");
	name=request.form.get("name");
	password1=request.form.get("password");
	uip=request.remote_addr;
	if(password1!=password):
		print("%s tried to use admin command but failed!"%uip);
		return jsonify({"code":1,"msg":"密码错误"});
	cm=name.split();
	if(not cm):
		return jsonify({"code":1,"msg":"命令为空!"});
	if(cm[0]=="clear"):
		qf(1);
		print("Game is cleared by %s."%uip);
		return jsonify({"code":0,"msg":"清房成功!"});
	if(cm[0]=="kick"):
		if(len(cm)<2):
			return jsonify({"code":1,"msg":"命令无效!"});
		for i in player_list:
			if(i is None):continue;
			if(i["name"]==cm[1]):
				qf(0);
				print("%s was kicked by %s."%(i["name"],uip));
				player_list[player_list.index(i)]=None;
				return jsonify({"code":0,"msg":"玩家已踢出!"});
		return jsonify({"code":1,"msg":"未找到该玩家!"});
	if(cm[0]=="reload"):
		readini(1);
		print("Initialization file was reloaded by %s"%uip);
		return jsonify({"code":0,"msg":"配置文件已重载!"});
	if(cm[0]=="query"):
		if(len(cm)<2):
			return jsonify({"code":1,"msg":"命令无效!"});
		avq=["ip","port","df","bs","time_1","time_2","time_3","time_0","gsave","playerban","ipban","enablewhitelist","playerwhite","ipwhite"];
		if(cm[1]not in avq):
			print("%s made a invalid query!"%uip);
			return jsonify({"code":1,"msg":"命令无效!"});
		s=str(eval(cm[1]));
		return jsonify({"code":0,"msg":"%s is %s"%(cm[1],s)});
	if(cm[0]=="cre"):
		gr=os.listdir("./replay");
		for i in gr:
			os.remove("./replay/%s"%i);
		return jsonify({"code":0,"msg":"清理成功!"});
	return jsonify({"code":1,"msg":"命令无效!"});
		

@app.route("/help")
def help():
	return render_template("help.html",time_1=time_1,time_2=time_2,time_3=time_3,bsc=bsc,df=df);

@app.route("/replay")
def replay():
	if(not gsave):
		return"本服务器未启用游戏回放!";
	if(not os.path.exists("./replay")):
		return"本服务器无游戏回放!";
	li=os.listdir("./replay")[::-1];
	return render_template("replay.html",li=li);

@app.route("/replay/<fname>")
def replay2(fname):
	if(not gsave):
		return"本服务器未启用游戏回放!";
	try:
		a=open("./replay/%s"%fname,"r",encoding="utf-8");
	except FileNotFoundError:
		return"不存在此回放文件!";
	t=a.read();
	a.close();
	return t;
	

@app.route("/")
def r():
	global is_d_start;
	if("name"not in session or session["name"]is None):
		return redirect("/login");
	for i in player_list:
		if(i and i["name"]==session["name"]):break;
	else:
		return redirect("/login");
	if(not is_d_start):
		disconnect_player();
		is_d_start=1;
	return render_template("r.html",time=get_time(),mid=session["index"],msgid=msgid,df=df,modifynotice=modifynotice);



readini();
app.run(ip,port);