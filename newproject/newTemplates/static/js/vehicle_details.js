document.getElementById("button1").addEventListener("click",(e)=>{
  document.getElementById("block-1").style.display = "block";
  document.getElementById("block-2").style.display = "none";
  document.getElementById("block-3").style.display = "none";
  
});
document.getElementById("button2").addEventListener("click",(e)=>{
  document.getElementById("block-2").style.display = "block";
  document.getElementById("block-1").style.display = "none";
  document.getElementById("block-3").style.display = "none";
  
});
document.getElementById("button3").addEventListener("click",(e)=>{
  document.getElementById("block-3").style.display = "block";
  document.getElementById("block-1").style.display = "none";
  document.getElementById("block-2").style.display = "none";
  
});
