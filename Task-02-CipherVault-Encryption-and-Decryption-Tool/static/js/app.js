let algorithms={},currentAlgorithm=null;
const historyKey="ciphervault_history_v3";
const $=id=>document.getElementById(id);
const el={nav:$("algo-nav"),search:$("search"),sidebar:$("sidebar"),menu:$("menu-toggle"),input:$("input-text"),output:$("output-text"),key:$("input-key"),keySection:$("key-section"),keyLabel:$("key-label"),keyHint:$("key-hint"),count:$("input-char-count"),enc:$("btn-encrypt"),dec:$("btn-decrypt"),clear:$("btn-clear"),copy:$("btn-copy"),swap:$("btn-swap"),download:$("btn-download"),status:$("result-status"),history:$("history-list"),clearHistory:$("btn-clear-history"),meter:$("password-meter")};

const visuals={
 caesar:"H E L L O\n+3 +3 +3 +3 +3\n↓ ↓ ↓ ↓ ↓\nK H O O R",
 vigenere:"Plaintext: H E L L O\nKeyword:   K E Y K E\nShift:     10 4 24 10 4\n↓\nCiphertext: R I J V S",
 atbash:"A ↔ Z    B ↔ Y    C ↔ X\n\nH E L L O\n↓ ↓ ↓ ↓ ↓\nS V O O L",
 rail_fence:"W . . E . . C . . R . . L . . T\n. E . R . D . S . O . E . E . A\n. . A . . I . . V . . D . . E .\n\nRead each rail → ciphertext",
 xor:"UTF-8 Message Bytes\n        XOR\nRepeating Secret Key Bytes\n        ↓\nBinary Result → Base64 for display",
 fernet:"Password\n   ↓\nRandom Salt + scrypt\n   ↓\nDerived Key\n   ↓\nFernet Encrypt + Authenticate\n   ↓\nVersioned Cipher Package",
 aes_gcm:"Password\n   ↓\nRandom Salt + scrypt → AES-256 Key\nRandom 12-byte Nonce\n   ↓\nAES-GCM Encrypt + Authenticate\n   ↓\nVersion + Salt + Nonce + Ciphertext"
};

async function init(){try{const r=await fetch("/api/algorithms"),d=await r.json();if(!d.success)throw 0;algorithms=d.algorithms;renderNav();renderCompareSelector();renderSecurityTable();selectAlgorithm(Object.keys(algorithms)[0]);bind();}catch{toast("Failed to load algorithms.","error");}}
function renderNav(filter=""){el.nav.innerHTML="";const groups={},order=["Classical","Key-Based","Modern"];Object.entries(algorithms).forEach(([id,a])=>{if(filter&&!`${a.name} ${a.category}`.toLowerCase().includes(filter.toLowerCase()))return;(groups[a.category]??=[]).push([id,a]);});order.forEach(cat=>{if(!groups[cat])return;const h=document.createElement("div");h.className="category-header";h.textContent=cat;el.nav.append(h);groups[cat].forEach(([id,a])=>{const b=document.createElement("div");b.className=`nav-item ${id===currentAlgorithm?"active":""}`;b.textContent=a.name;b.onclick=()=>selectAlgorithm(id);el.nav.append(b);});});}
function selectAlgorithm(id){currentAlgorithm=id;const a=algorithms[id];renderNav(el.search.value);$("info-name").textContent=a.name;$("info-category").textContent=a.category;$("info-desc").textContent=a.description;$("info-security").textContent=a.security_level;$("work-name").textContent=a.name;$("work-desc").textContent=a.description;$("work-key").textContent=a.key_type;$("work-category").textContent=a.category;$("visual-demo").textContent=visuals[id]||"Visual demonstration unavailable.";$("work-steps").innerHTML="";a.working.forEach(x=>{const li=document.createElement("li");li.textContent=x;$("work-steps").append(li);});$("ex-input").textContent=a.example?.input||"—";$("ex-key").textContent=a.example?.key||"—";$("ex-output").textContent=a.example?.output||"—";el.keySection.style.display=a.requires_key?"block":"none";el.key.value="";el.key.type=a.key_type==="Password"?"password":"text";el.keyLabel.textContent=a.key_type.toUpperCase();el.keyHint.textContent=a.key_type==="Password"?"Use a strong password. The same password is required to decrypt.":a.key_type==="Numeric Shift"?"Any integer is accepted; values wrap around the alphabet.":a.key_type==="Numeric Rails"?"Use an integer of 2 or greater.":a.requires_key?"The same key is required to reverse the operation.":"";el.meter.classList.toggle("hidden",a.key_type!=="Password");updatePasswordMeter();const encoding=a.category==="Encoding";el.enc.textContent=encoding?"Encode":"🔒 Encrypt";el.dec.textContent=encoding?"Decode":"🔓 Decrypt";if(innerWidth<950)el.sidebar.classList.remove("open");}
function passwordStrength(p){const tests=[p.length>=12,/[a-z]/.test(p),/[A-Z]/.test(p),/\d/.test(p),/[^A-Za-z0-9]/.test(p)];return {score:tests.filter(Boolean).length,tests};}
function updatePasswordMeter(){if(el.meter.classList.contains("hidden"))return;const p=passwordStrength(el.key.value),labels=["Very weak","Weak","Fair","Good","Strong","Very strong"];$("meter-bar").style.width=`${p.score*20}%`;$("meter-label").textContent=labels[p.score];$("meter-score").textContent=`${p.score}/5`;$("meter-checks").innerHTML=["12+ characters","Lowercase","Uppercase","Number","Special character"].map((x,i)=>`<span class="${p.tests[i]?"pass":""}">${p.tests[i]?"✓":"○"} ${x}</span>`).join("");}
async function operate(operation){const a=algorithms[currentAlgorithm],text=el.input.value,key=el.key.value;if(!text){toast("Please enter text before continuing.","error");return;}if(a.requires_key&&!key){toast(`${a.name} requires a key.`,"error");return;}setBusy(true);const started=performance.now();try{const r=await fetch(`/api/${operation}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({algorithm:currentAlgorithm,text,key})}),d=await r.json();if(!d.success)throw new Error(d.error);el.output.value=d.result;renderLiveTransformation(operation,text,key,d.result);el.status.style.display="inline";el.status.textContent=`${operation.toUpperCase()} COMPLETE`;showStats(text.length,d.result.length,performance.now()-started);saveHistory(operation,a.name,text.length,d.result.length);toast("Operation completed.");}catch(e){toast(e.message||"Operation failed.","error");}finally{setBusy(false);}}
function showStats(input,output,time){$("stats-card").classList.remove("hidden");$("stat-input").textContent=input;$("stat-output").textContent=output;$("stat-change").textContent=input?`${((output-input)/input*100).toFixed(1)}%`:"—";$("stat-time").textContent=`${time.toFixed(1)} ms`;}
function setBusy(b){[el.enc,el.dec].forEach(x=>{x.disabled=b;x.style.opacity=b?.65:1;});}

function liveEsc(v){return escapeHTML(String(v));}
function bit8(n){return Number(n).toString(2).padStart(8,"0");}
function letterPos(ch){return ch.toUpperCase().charCodeAt(0)-65;}
function letterAt(n,upper){let c=String.fromCharCode(((n%26+26)%26)+65);return upper?c:c.toLowerCase();}

function renderLiveTransformation(operation,text,key,result){
  const box=$("live-transformation-content"), status=$("live-status");
  const id=currentAlgorithm, a=algorithms[id], input=[...text].slice(0,60);
  status.textContent=operation==="encrypt"?"ENCRYPTION":"DECRYPTION";
  box.className="live-content";
  let out="";

  if(["caesar","vigenere","atbash"].includes(id)){
    let rows=[], ki=0, cleanKey=(key||"").replace(/[^A-Za-z]/g,"");
    for(let i=0;i<input.length;i++){
      const ch=input[i];
      if(!/[A-Za-z]/.test(ch)){rows.push(`<tr><td>${i+1}</td><td>${liveEsc(ch===" "?"␠":ch)}</td><td>Non-letter</td><td>—</td><td>${liveEsc(ch===" "?"␠":ch)}</td></tr>`);continue;}
      const p=letterPos(ch); let r, detail, calc;
      if(id==="caesar"){
        let sh=((parseInt(key,10)||0)%26+26)%26; if(operation==="decrypt")sh=-sh;
        r=letterAt(p+sh,ch===ch.toUpperCase()); detail=`Shift ${sh>=0?"+":"−"}${Math.abs(sh)}`; calc=`${p} ${sh>=0?"+":"−"} ${Math.abs(sh)} → ${((p+sh)%26+26)%26}`;
      }else if(id==="atbash"){
        r=letterAt(25-p,ch===ch.toUpperCase()); detail="Mirror alphabet"; calc=`25 − ${p} → ${25-p}`;
      }else{
        if(!cleanKey){out="<p class='live-warning'>Enter a valid alphabetic Vigenère key.</p>";break;}
        const kc=cleanKey[ki%cleanKey.length], kp=letterPos(kc); let sh=operation==="encrypt"?kp:-kp;
        r=letterAt(p+sh,ch===ch.toUpperCase()); detail=`Key ${kc} (${kp})`; calc=`(${p} ${sh>=0?"+":"−"} ${Math.abs(sh)}) mod 26 → ${((p+sh)%26+26)%26}`; ki++;
      }
      rows.push(`<tr><td>${i+1}</td><td>${liveEsc(ch)}</td><td>${p}</td><td>${detail}</td><td>${calc}</td><td>${liveEsc(r)}</td></tr>`);
    }
    if(!out)out=`<div class="live-summary"><b>${liveEsc(a.name)}</b><span>Exact transformation of your current input</span></div><div class="live-table-wrap"><table class="live-table"><thead><tr><th>#</th><th>Input</th><th>Position</th><th>Operation</th><th>Calculation</th><th>Output</th></tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
  } else if(id==="xor"){
    const rows=input.map((ch,i)=>{let k=key[i%key.length],x=ch.charCodeAt(0)^k.charCodeAt(0);return `<tr><td>${i+1}</td><td>${liveEsc(ch)}</td><td><code>${bit8(ch.charCodeAt(0))}</code></td><td>${liveEsc(k)}</td><td><code>${bit8(k.charCodeAt(0))}</code></td><td><code>${bit8(x)}</code></td></tr>`;});
    out=`<div class="live-summary"><b>Repeating-key XOR</b><span>Byte-by-byte XOR operation</span></div><div class="live-table-wrap"><table class="live-table"><thead><tr><th>#</th><th>Input</th><th>Input binary</th><th>Key</th><th>Key binary</th><th>XOR result</th></tr></thead><tbody>${rows.join("")}</tbody></table></div>`;
  } else if(id==="rail_fence"){
    const rails=Math.max(2,parseInt(key,10)||2), pattern=[];let rail=0,dir=1;
    input.forEach((ch,i)=>{pattern.push([ch,rail,i]);rail+=dir;if(rail===rails-1||rail===0)dir*=-1;});
    let lines=[];for(let r=0;r<rails;r++)lines.push(`Rail ${r+1}: `+pattern.map(x=>x[1]===r?(x[0]===" "?"␠":x[0]):"·").join(" "));
    out=`<div class="live-summary"><b>Rail Fence path</b><span>${rails} rails • zig-zag character placement</span></div><pre class="rail-visual">${liveEsc(lines.join("\\n"))}</pre><div class="live-mini-list">${pattern.map(x=>`<span>${x[2]+1}. ${liveEsc(x[0]===" "?"␠":x[0])} → Rail ${x[1]+1}</span>`).join("")}</div>`;
  } else {
    const bytes=input.map(ch=>ch.charCodeAt(0).toString(16).padStart(2,"0").toUpperCase()).join(" ");
    const name=id==="aes_gcm"?"AES-256-GCM":"Fernet";
    out=`<div class="live-summary"><b>${name} pipeline</b><span>Modern encryption is not a one-character substitution.</span></div><div class="modern-pipeline"><div><b>1. Plaintext</b><small>${liveEsc(input.join(""))}</small></div><div>↓</div><div><b>2. UTF-8 bytes</b><code>${bytes}</code></div><div>↓</div><div><b>3. Password + random salt</b><small>scrypt derives an encryption key</small></div><div>↓</div><div><b>4. ${name}</b><small>Authenticated encryption with fresh randomness</small></div><div>↓</div><div><b>5. Ciphertext</b><code>${liveEsc(result.slice(0,180))}${result.length>180?"…":""}</code></div></div><p class="live-warning">The same plaintext may produce different ciphertext because modern encryption uses fresh randomness. A character-to-character mapping would be technically incorrect.</p>`;
  }
  if(text.length>60)out+=`<p class="live-limit">Showing the first 60 characters to keep this visualization readable.</p>`;
  box.innerHTML=out;
}

function saveHistory(operation,algorithm,inputLength,outputLength){const h=JSON.parse(localStorage.getItem(historyKey)||"[]");h.unshift({operation,algorithm,inputLength,outputLength,time:new Date().toLocaleString()});localStorage.setItem(historyKey,JSON.stringify(h.slice(0,30)));loadHistory();}
function loadHistory(){const h=JSON.parse(localStorage.getItem(historyKey)||"[]");el.history.innerHTML=h.length?"":"<div class='history-item'>No operations yet.</div>";h.forEach(i=>{const d=document.createElement("div");d.className="history-item";d.innerHTML=`<div><span class="badge ${i.operation==="decrypt"?"dec":""}">${i.operation==="encrypt"?"ENC":"DEC"}</span> <b>${escapeHTML(i.algorithm)}</b> <span style="color:var(--muted)"> ${i.inputLength} → ${i.outputLength} chars</span></div><span class="history-time">${escapeHTML(i.time)}</span>`;el.history.append(d);});}
function renderCompareSelector(){
  $("compare-selector").innerHTML=Object.entries(algorithms).map(([id,a])=>
    `<label class="compare-option"><input type="checkbox" value="${id}" ${["caesar","vigenere","atbash","rail_fence"].includes(id)?"checked":""}>
      <span>${escapeHTML(a.name)}<small>${escapeHTML(a.category)}</small></span>
    </label>`).join("");
  document.querySelectorAll('#compare-selector input').forEach(input=>input.addEventListener("change",renderCompareKeys));
  renderCompareKeys();
}
function renderCompareKeys(){
  const selected=[...document.querySelectorAll('#compare-selector input:checked')].map(x=>x.value);
  const previous={};
  document.querySelectorAll("#compare-keys input").forEach(input=>previous[input.dataset.algorithm]=input.value);

  const required=selected.filter(id=>algorithms[id]?.requires_key);
  $("compare-keys").innerHTML=required.length
    ? `<div class="compare-key-title">Keys for selected techniques</div>`+required.map(id=>{
        const a=algorithms[id];
        const type=a.key_type==="Password"?"password":"text";
        const placeholder=a.key_type==="Numeric Shift"?"Enter numeric shift (e.g. 3)"
          :a.key_type==="Numeric Rails"?"Enter number of rails (e.g. 3)"
          :a.key_type==="Password"?"Enter password"
          :"Enter key";
        return `<div class="compare-key-row">
          <label for="compare-key-${id}">${escapeHTML(a.name)} <span>${escapeHTML(a.key_type)}</span></label>
          <input id="compare-key-${id}" data-algorithm="${id}" type="${type}" value="${escapeHTML(previous[id]||"")}" placeholder="${placeholder}" autocomplete="off">
        </div>`;
      }).join("")
    : "";
}
async function runComparison(){
  const text=$("compare-input").value;
  if(!text)return toast("Enter text to compare.","error");
  const selected=[...document.querySelectorAll('#compare-selector input:checked')].map(x=>x.value);
  if(!selected.length)return toast("Select at least one technique.","error");

  const keys={};
  let missing=[];
  selected.forEach(id=>{
    const a=algorithms[id];
    if(a.requires_key){
      const input=document.querySelector(`#compare-key-${id}`);
      keys[id]=input?input.value:"";
      if(!keys[id].trim())missing.push(a.name);
    }
  });
  if(missing.length){
    toast(`Enter a key for: ${missing.join(", ")}.`,"error");
    return;
  }

  $("compare-results").innerHTML="<div class='panel'>Running comparison…</div>";
  try{
    const r=await fetch("/api/compare",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text,algorithms:selected,keys})}),d=await r.json();
    if(!d.success)throw new Error(d.error);
    $("compare-results").innerHTML=d.results.map(x=>x.success
      ?`<article class="compare-card"><div><span class="eyebrow">${escapeHTML(x.category)}</span><h2>${escapeHTML(x.name)}</h2><span class="security-mini">${escapeHTML(x.security_level)}</span></div><div class="compare-output">${escapeHTML(x.result)}</div><div class="compare-footer">${x.output_length} characters</div></article>`
      :`<article class="compare-card error-card"><h2>${escapeHTML(x.name)}</h2><p>${escapeHTML(x.error)}</p></article>`).join("");
  }catch(e){
    $("compare-results").innerHTML="";
    toast(e.message||"Comparison failed.","error");
  }
}
function renderSecurityTable(){
  const modern=new Set(["fernet","aes_gcm"]);
  const rows=Object.entries(algorithms).map(([id,a])=>{
    const secure=modern.has(id);
    return `<tr><td><b>${escapeHTML(a.name)}</b><small>${escapeHTML(a.category)}</small></td><td>${secure?"✓":"✗"}</td><td>${secure?"✓":"✗"}</td><td>${secure?"✓":"✗"}</td><td>${secure?"Yes, with correct implementation and key management":"No — educational"}</td></tr>`;
  });
  $("security-table").innerHTML=rows.join("");
}
function openView(view){document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x.dataset.view===view));document.querySelectorAll(".view").forEach(x=>x.classList.remove("active"));$(view).classList.add("active");window.scrollTo({top:0,behavior:"smooth"});}
function escapeHTML(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function toast(message,type="success"){const d=document.createElement("div");d.className=`toast ${type}`;d.textContent=message;$("toast-container").append(d);setTimeout(()=>d.remove(),3200);}
function bind(){el.search.oninput=e=>renderNav(e.target.value);el.menu.onclick=()=>el.sidebar.classList.toggle("open");el.input.oninput=()=>el.count.textContent=`${el.input.value.length} chars`;el.key.oninput=updatePasswordMeter;el.enc.onclick=()=>operate("encrypt");el.dec.onclick=()=>operate("decrypt");$("open-working").onclick=()=>openView("working");document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>openView(t.dataset.view));$("btn-compare").onclick=runComparison;el.clear.onclick=()=>{el.input.value="";el.output.value="";el.key.value="";el.count.textContent="0 chars";el.status.style.display="none";$("stats-card").classList.add("hidden");$("live-status").textContent="WAITING";$("live-transformation-content").className="live-empty";$("live-transformation-content").textContent="Run an encryption or decryption operation to see how your input is transformed.";updatePasswordMeter();};$("toggle-key").onclick=()=>el.key.type=el.key.type==="password"?"text":"password";el.copy.onclick=async()=>{if(!el.output.value)return toast("Nothing to copy.","error");try{await navigator.clipboard.writeText(el.output.value);toast("Copied to clipboard.");}catch{toast("Clipboard access failed.","error");}};el.swap.onclick=()=>{if(!el.output.value)return;el.input.value=el.output.value;el.count.textContent=`${el.input.value.length} chars`;el.output.value="";el.status.style.display="none";};el.download.onclick=()=>{if(!el.output.value)return toast("Nothing to download.","error");const a=algorithms[currentAlgorithm],content=`CipherVault Result\n==================\nAlgorithm: ${a.name}\nGenerated: ${new Date().toISOString()}\n\nResult:\n${el.output.value}\n`,u=URL.createObjectURL(new Blob([content],{type:"text/plain"})),x=document.createElement("a");x.href=u;x.download=`ciphervault-${currentAlgorithm}-result.txt`;x.click();URL.revokeObjectURL(u);};el.clearHistory.onclick=()=>{localStorage.removeItem(historyKey);loadHistory();toast("History cleared.");};document.addEventListener("keydown",e=>{if(e.ctrlKey&&e.key==="Enter"){e.preventDefault();operate("encrypt");}if(e.ctrlKey&&e.shiftKey&&e.key==="Enter"){e.preventDefault();operate("decrypt");}});loadHistory();}
init();
