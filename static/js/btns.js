let warn=document.getElementById("warn");
function fbtn1(){
	let pk=document.getElementsByClassName("card_select");
	let li="";
	for(let i=0;i<pk.length;i++){
		li+=pk[i].id;
		li+=" ";
	}
	$.post("/gm/cp",{"p":li},function(res){
		warn.innerHTML=res["msg"];
	});
}
function fbtn2(){
	$.get("/gm/mp",function(res){
		hid_btn();
	});
}
function fbtn4(){
	$.get("/gm/cancel",function(res){
		hid_btn();
		warn.innerHTML="";
	});
}
function fbtn8(){
	$.get("/gm/jb",function(res){
		hid_btn();
	});
}
function fbtn16(){
	$.get("/gm/cjjb",function(res){
		hid_btn();
	});
}
function fbtn32(){
	$.get("/gm/jdz",function(res){
		hid_btn();
	});
}
function fbtn64(){
	$.get("/gm/qdz",function(res){
		hid_btn();
	});
}
function fbtn128(){
	$.get("/gm/ready",function(res){
		hid_btn();
	});
}
