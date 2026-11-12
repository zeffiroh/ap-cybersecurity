/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/time.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const r=Math.floor,f=Math.round,x=Math.log10,h=n=>Math.pow(10,n),m=["","k","M","G","T","P","E","Z","Y"],w=["","m","\u03BC","n","p","f","a","z","y"],u=(n,t=0)=>{const c=n===0?0:x(n);let o=0;for(;c<o*3&&t>-8;)t--,o--;for(;c>=3+o*3&&t<8;)t++,o++;const s=t<0?w[-t]:m[t];return{n:f((o>0?n/h(o*3):n*h(o*-3))*1e12)/1e12,prefix:s}},a=()=>new Date,i=Date.now,p=n=>{if(n<6e4){const e=u(n,-1);return f(e.n*100)/100+e.prefix+"s"}n=r(n/1e3);const t=n%60,c=r(n/60)%60,o=r(n/3600)%24,s=r(n/86400);return s>0?s+"d"+(o>0||c>30?" "+(c>30?o+1:o)+"h":""):o>0?o+"h"+(c>0||t>30?" "+(t>30?c+1:c)+"min":""):c+"min"+(t>0?" "+t+"s":"")};export{a as getDate,i as getUnixTime,p as humanizeDuration};
//# sourceMappingURL=/sm/caf92126edcb3e21469701b4cacb45ddd6cd6c4bf1042451893b4e2912c2f34d.map