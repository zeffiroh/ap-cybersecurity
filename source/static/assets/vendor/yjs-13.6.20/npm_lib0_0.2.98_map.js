/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/map.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const o=()=>new Map,f=n=>{const e=o();return n.forEach((r,t)=>{e.set(t,r)}),e},c=(n,e,r)=>{let t=n.get(e);return t===void 0&&n.set(e,t=r()),t},u=(n,e)=>{const r=[];for(const[t,s]of n)r.push(e(s,t));return r},a=(n,e)=>{for(const[r,t]of n)if(e(t,r))return!0;return!1},l=(n,e)=>{for(const[r,t]of n)if(!e(t,r))return!1;return!0};export{l as all,a as any,f as copy,o as create,u as map,c as setIfUndefined};
//# sourceMappingURL=/sm/da42bf1d9c7f79a0230042cc83068443ec77cafdfd9d9c44dddd198ff2820e82.map