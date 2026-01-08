// Dark / Light Toggle
const toggleBtn = document.getElementById("themeToggle");
if(toggleBtn){
  toggleBtn.addEventListener("click", ()=>{
    document.body.classList.toggle("light");
    const isLight = document.body.classList.contains("light");
    localStorage.setItem("theme", isLight ? "light":"dark");
    toggleBtn.textContent = isLight ? "☀️":"🌙";
  });
  const savedTheme = localStorage.getItem("theme");
  if(savedTheme==="light"){
    document.body.classList.add("light");
    toggleBtn.textContent="☀️";
  }
}

// Scroll Reveal
function reveal(){
  const reveals=document.querySelectorAll(".reveal");
  for(let i=0;i<reveals.length;i++){
    const windowHeight=window.innerHeight;
    const elementTop=reveals[i].getBoundingClientRect().top;
    const elementVisible=100;
    if(elementTop<windowHeight-elementVisible){
      reveals[i].classList.add("active");
    }else{
      reveals[i].classList.remove("active");
    }
  }
}
window.addEventListener("scroll",reveal);
window.addEventListener("load",reveal);
