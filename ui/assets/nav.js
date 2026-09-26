/* Shared navigation + admin-token memory for every uniAIverse page. Loaded by every ui/*.html. */
(function(){
  var pages=[["/console","Console"],["/","Audit"],["/services","Services"],["/showcase","Showcase"],["/news","News"],["/discovery","Discovery"],["/delivery","Delivery"],["/tools","Tools"],["/demos","Demos"],["/course-finder","Course Finder"],["/quest","Quest"],["/register","Register"],["/pay","Pay"]];
  var admin=[["/platform","Control plane"],["/monitor","Monitor"],["/admin","Admin"],["/docs","API"]];
  var here=location.pathname.replace(/\/$/,"")||"/";
  var nav=document.createElement("nav");nav.className="uav-nav";
  nav.innerHTML='<div class="in"><a class="brand" href="/console"><b></b>uniAIverse</a><div class="links">'+pages.map(function(p){return '<a href="'+p[0]+'"'+(here===p[0]?' class="on"':'')+'>'+p[1]+'</a>'}).join("")+admin.map(function(p){return '<a href="'+p[0]+'" class="adm'+(here===p[0]?' on':'')+'">'+p[1]+'</a>'}).join("")+'</div><span class="env" id="uavEnv">…</span></div>';
  document.body.insertBefore(nav,document.body.firstChild);
  var foot=document.createElement("div");foot.className="uav-foot";foot.innerHTML="uniAIverse · one engine, many faces · figures marked placeholder are not quotes";document.body.appendChild(foot);
  fetch("/api/health").then(function(r){return r.json()}).then(function(h){var e=document.getElementById("uavEnv");if(e)e.textContent=(h.version||"")+" · "+(h.services||[]).length+" services"}).catch(function(){});
  // Admin token memory: any input with id 'tok' or 'token' remembers its value for this browser session.
  window.uavToken=function(){return sessionStorage.getItem("uav_admin_token")||""};
  document.addEventListener("DOMContentLoaded",function(){["tok","token"].forEach(function(id){var i=document.getElementById(id);if(!i)return;if(!i.value)i.value=window.uavToken();i.addEventListener("change",function(){sessionStorage.setItem("uav_admin_token",i.value.trim())});i.addEventListener("keyup",function(){sessionStorage.setItem("uav_admin_token",i.value.trim())})});});
})();
