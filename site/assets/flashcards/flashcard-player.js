const FlashcardPlayer=(()=>{let cards=[];let order=[];let idx=0;let flipped=false;function escapeHtml(s){return(s||"").toString().replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function shuffle(arr){const a=arr.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
return a;}
function render(){const card=cards[order[idx]];const stage=document.getElementById("card-stage-inner");stage.className="flashcard"+(flipped?" flipped":"");stage.innerHTML=`
      <div class="card-face front">
        <div class="card-label">Question</div>
        <div class="card-front-text">${escapeHtml(card.front)}</div>
      </div>
      <div class="card-face back">
        <div class="card-label">Answer</div>
        <div class="back-section definition"><div class="bs-label">Definition</div><div class="bs-text">${escapeHtml(card.back_definition)}</div></div>
        ${card.back_example ? `<div class="back-section example"><div class="bs-label">Example</div><div class="bs-text">${escapeHtml(card.back_example)}</div></div>` : ""}
        ${card.back_confusion ? `<div class="back-section confusion"><div class="bs-label">Don't Confuse</div><div class="bs-text">${escapeHtml(card.back_confusion)}</div></div>` : ""}
        ${card.back_hook ? `<div class="back-section hook"><div class="bs-label">Memory Hook</div><div class="bs-text">${escapeHtml(card.back_hook)}</div></div>` : ""}
      </div>
    `;document.getElementById("deck-position").textContent=(idx+1)+" / "+cards.length;document.getElementById("prev-btn").disabled=idx===0;document.getElementById("next-btn").disabled=idx===cards.length-1;}
function flip(){flipped=!flipped;document.getElementById("card-stage-inner").classList.toggle("flipped",flipped);}
function next(){if(idx<cards.length-1){idx++;flipped=false;render();}}
function prev(){if(idx>0){idx--;flipped=false;render();}}
function reshuffle(){order=shuffle(order);idx=0;flipped=false;render();}
function restart(){order=cards.map((_,i)=>i);idx=0;flipped=false;render();}
async function exportAnki(){const cfg=window.FLASHCARD_CONFIG;if(!cfg.apkgUrl){alert("Anki export not available for this deck.");return;}
const a=document.createElement("a");a.href=cfg.apkgUrl;a.download=cfg.apkgUrl.split("/").pop();document.body.appendChild(a);a.click();document.body.removeChild(a);}
async function init(){const cfg=window.FLASHCARD_CONFIG;document.getElementById("deck-title").textContent=cfg.title;document.getElementById("deck-subtitle").textContent=cfg.subtitle||"";const resp=await fetch(cfg.dataUrl);const data=await resp.json();cards=data.flashcards||[];order=cards.map((_,i)=>i);document.getElementById("deck-total").textContent=cards.length;if(cards.length===0){document.getElementById("card-stage-inner").innerHTML='<div class="card-face front">No flashcards available.</div>';return;}
render();document.addEventListener("keydown",(e)=>{if(e.code==="Space"){e.preventDefault();flip();}
if(e.code==="ArrowRight")next();if(e.code==="ArrowLeft")prev();});}
return{init,flip,next,prev,reshuffle,restart,exportAnki};})();document.addEventListener("DOMContentLoaded",()=>FlashcardPlayer.init());
