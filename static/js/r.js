let errmsg=document.getElementById("errmsg");
let msgs=document.getElementById("msgs");
let name_up=document.getElementById("name_up");
let name_my=document.getElementById("name_my");
let name_dn=document.getElementById("name_dn");
let dzpd_up=document.getElementById("dzpd_up");
let dzpd_my=document.getElementById("dzpd_my");
let dzpd_dn=document.getElementById("dzpd_dn");
let s_up=document.getElementById("s_up");
let s_my=document.getElementById("s_my");
let s_dn=document.getElementById("s_dn");
let card_up=document.getElementById("card_up");
let card_my=document.getElementById("card_my");
let card_dn=document.getElementById("card_dn");
let myc=document.getElementById("myc");
let rtime=document.getElementById("rtime");
let dzcard=document.getElementById("dzcard");
let bs=document.getElementById("bs");
let fs_up=document.getElementById("fs_up");
let fs_my=document.getElementById("fs_my");
let fs_dn=document.getElementById("fs_dn");
let btn1=document.getElementById("btn1");
let btn2=document.getElementById("btn2");
let btn4=document.getElementById("btn4");
let btn8=document.getElementById("btn8");
let btn16=document.getElementById("btn16");
let btn32=document.getElementById("btn32");
let btn64=document.getElementById("btn64");
let btn128=document.getElementById("btn128");
let selections=[];
let previos=[];
let selectopt="";
function gettime() {
    // let msgs_=document.getElementById("msgs").getElementsByTagName("div");
    // let last_time=msgs_[msgs_.length-1].dataset.time;
    return msgid;
}

function arrayequal(a0,a1){
	if(a0.length!==a1.length)return 0;
	for(let i=0;i<a0.length;i++)if(a0[i]!==a1[i])return 0;
	return 1;
}

function appendhiddendiv(res){
	// msgs.innerHTML+="<div data-time="+res["msgid"]+"></div>";
	msgid=res["msgid"];
}
function show_new_list(res){
    for(let i=0;i<res.length;i++){
		appendhiddendiv(res[i]);
		handle_req(res[i]);
	}
}
function show_player(){
	$.get("/get_player",function(res){
		name_up.innerHTML=res[0]["name"];
		name_my.innerHTML=res[1]["name"];
		name_dn.innerHTML=res[2]["name"];
		dzpd_up.innerHTML=res[0]["is_dz"]?"地主":"";
		dzpd_my.innerHTML=res[1]["is_dz"]?"地主":"";
		dzpd_dn.innerHTML=res[2]["is_dz"]?"地主":"";
		card_up.innerHTML=res[0]["cardr"];
		card_my.innerHTML=res[1]["cardr"];
		card_dn.innerHTML=res[2]["cardr"];
		s_up.innerHTML=res[0]["content"].replace(/\[R\]/g,"<span class=\"rc\">").replace(/\[B\]/g,"<span class=\"bc\">").replace(/\[\/\]/g,"</span>");
		s_my.innerHTML=res[1]["content"].replace(/\[R\]/g,"<span class=\"rc\">").replace(/\[B\]/g,"<span class=\"bc\">").replace(/\[\/\]/g,"</span>");
		s_dn.innerHTML=res[2]["content"].replace(/\[R\]/g,"<span class=\"rc\">").replace(/\[B\]/g,"<span class=\"bc\">").replace(/\[\/\]/g,"</span>");
		fs_up.innerHTML=res[0]["point"];
		fs_my.innerHTML=res[1]["point"];
		fs_dn.innerHTML=res[2]["point"];
	});
}
function get_btn(){
	$.get("/get_btn",function(res){
		let ires=Number(res["num"]);
		if(ires&128)btn128.style.display="inline";
		else btn128.style.display="none";
		if(ires&64)btn64.style.display="inline";
		else btn64.style.display="none";
		if(ires&32)btn32.style.display="inline";
		else btn32.style.display="none";
		if(ires&16)btn16.style.display="inline";
		else btn16.style.display="none";
		if(ires&8)btn8.style.display="inline";
		else btn8.style.display="none";
		if(ires&4)btn4.style.display="inline";
		else btn4.style.display="none";
		if(ires&2)btn2.style.display="inline";
		else btn2.style.display="none";
		if(ires&1)btn1.style.display="inline";
		else btn1.style.display="none";
	});
}
function get_card(){
	$.get("/get_card",function(res){
		let now=[];
		for(let i=0;i<res.length;i++)now[i]=res[i]["data"];
		if(arrayequal(previos,now))return;
		myc.innerHTML="";
		previos=now;
		for(let i=0;i<res.length;i++){
			if(res[i]["data"]==0xf0||(res[i]["data"]!=0xf0&&((res[i]["data"]&0xf)==1||(res[i]["data"]&0xf)==3))){
				myc.innerHTML+="<div id=\""+res[i]["data"]+"\" class=\"card rc\" style=\"position:absolute;left:"+i*30+"px;z-index:"+i+";\" onmousedown=\"slt("+res[i]["data"]+")\">"+res[i]["display"]+"</div>";
			}
			else if(res[i]["data"]==0xe0||(res[i]["data"]!=0xe0&&((res[i]["data"]&0xf)==0||(res[i]["data"]&0xf)==2))){
				myc.innerHTML+="<div id=\""+res[i]["data"]+"\" class=\"card bc\" style=\"position:absolute;left:"+i*30+"px;z-index:"+i+";\" onmousedown=\"slt("+res[i]["data"]+")\">"+res[i]["display"]+"</div>";
			}
		}
	});
}
function get_dzcard(){
	$.get("/get_dzcard",function(res){
		dzcard.innerHTML=res["c"].replace(/\[R\]/g,"<span class=\"rc\">").replace(/\[B\]/g,"<span class=\"bc\">").replace(/\[\/\]/g,"</span>");
	});
}
function get_end_time(){
	$.get("/get_end_time",function(res){
		rtime.innerHTML=res["num"];
		bs.innerHTML=res["bs"];
	})
}
function get_fs(){
	$.get("/get_fs",function(res){});
}
// function saveselect(){
// 	let trs=document.getElementsByClassName("selects");
// 	for(let i=0;i<trs.length;i++){
// 		let a=document.getElementById("select_"+(i+1));
// 		if(a!=null)
// 			selections[i+1]=a.value;
// 		else selections[i+1]=0;
// 	}
// }
function hid_btn(){
	btn128.style.display="none";
	btn64.style.display="none";
	btn32.style.display="none";
	btn16.style.display="none";
	btn8.style.display="none";
	btn4.style.display="none";
	btn2.style.display="none";
	btn1.style.display="none";
}
function handle_req(req){
	if(req["msg"]=="sp")show_player();
	if(req["msg"]=="gb")get_btn();
	if(req["msg"]=="gc")get_card();
	if(req["msg"]=="gd")get_dzcard();
	if(req["msg"]=="gf")get_fs();
}
function slt(s){
	let csd=document.getElementById(String(s));
	if(!/card_select/.test(csd.className)){
		csd.className+=" card_select";
	}else{
		csd.className=csd.className.replace(" card_select","");
	}
	return csd.className;
}
window.onload=function(){
	show_player();
	get_btn();
	get_card();
	get_dzcard();
	setInterval(function(){
        let last_time=gettime();
		get_end_time();
        $.get("/get_msg?t="+last_time,function(res){
            show_new_list(res);
        })
    },1000);
}
