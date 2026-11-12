/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/object.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const y=()=>Object.create(null),l=Object.assign,s=Object.keys,a=(e,t)=>{for(const n in e)t(e[n],n)},p=(e,t)=>{const n=[];for(const r in e)n.push(t(e[r],r));return n},h=e=>s(e).length,c=e=>s(e).length,k=(e,t)=>{for(const n in e)if(t(e[n],n))return!0;return!1},O=e=>{for(const t in e)return!1;return!0},o=(e,t)=>{for(const n in e)if(!t(e[n],n))return!1;return!0},f=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),g=(e,t)=>e===t||c(e)===c(t)&&o(e,(n,r)=>(n!==void 0||f(t,r))&&t[r]===n),u=Object.freeze,i=e=>{for(const t in e){const n=e[t];(typeof n=="object"||typeof n=="function")&&i(e[t])}return u(e)};export{l as assign,y as create,i as deepFreeze,g as equalFlat,o as every,a as forEach,u as freeze,f as hasProperty,O as isEmpty,s as keys,h as length,p as map,c as size,k as some};
//# sourceMappingURL=/sm/00da94b4c8dbafcf7d7441875819648190449052c3ae745def225f67564fd766.map