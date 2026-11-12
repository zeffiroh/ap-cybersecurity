/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/random.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
import{getRandomValues as n}from"./npm_lib0_0.2.98_webcrypto.js";const r=Math.floor,s=1<<21,c=s-1,a=4294967295,o=Math.random,e=()=>n(new Uint32Array(1))[0],i=()=>{const t=n(new Uint32Array(8));return(t[0]&c)*(a+1)+(t[1]>>>0)},u=t=>t[r(o()*t.length)],F="10000000-1000-4000-8000"+-1e11,l=()=>F.replace(/[018]/g,t=>(t^e()&15>>t/4).toString(16));export{u as oneOf,o as rand,e as uint32,i as uint53,l as uuidv4};
//# sourceMappingURL=/sm/2bf0b29ea55813cff0a8db1fb5e76689e8585f9ccb3d604d47c394b4d0dfff04.map