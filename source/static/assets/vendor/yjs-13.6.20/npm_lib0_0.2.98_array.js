/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/array.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const i=()=>new Set,a=t=>new Set(t),h=t=>t[t.length-1],p=()=>[],y=t=>t.slice(),g=(t,n)=>{for(let e=0;e<n.length;e++)t.push(n[e])},l=Array.from,u=(t,n)=>{for(let e=0;e<t.length;e++)if(!n(t[e],e,t))return!1;return!0},d=(t,n)=>{for(let e=0;e<t.length;e++)if(n(t[e],e,t))return!0;return!1},m=(t,n)=>t.length===n.length&&u(t,(e,o)=>e===n[o]),A=t=>f(t,[],(n,e)=>n.concat(e)),q=(t,n)=>{const e=new Array(t);for(let o=0;o<t;o++)e[o]=n(o,e);return e},f=(t,n,e)=>t.reduce(e,n),w=Array.isArray,S=t=>l(a(t)),$=(t,n)=>{const e=i(),o=[];for(let s=0;s<t.length;s++){const c=t[s],r=n(c);e.has(r)||(e.add(r),o.push(c))}return o},v=(t,n)=>{const e=Array(t.length);for(let o=0;o<t.length;o++)e[o]=n(t[o],o,t);return e};export{g as appendTo,y as copy,p as create,m as equalFlat,u as every,A as flatten,f as fold,l as from,w as isArray,h as last,v as map,d as some,q as unfold,S as unique,$ as uniqueBy};
//# sourceMappingURL=/sm/2df3bd940f06f5c46a2eba66dbab7ef573ed81ba696367827126d7e27c896399.map