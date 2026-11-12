/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/promise.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const o=Date.now,i=e=>new Promise(e),v=e=>new Promise(e),w=Promise.all.bind(Promise),P=e=>Promise.reject(e),u=e=>Promise.resolve(e),T=e=>Promise.resolve(e),f=(e,t,n=10)=>i((s,r)=>{const l=o(),m=e>0,c=setInterval(()=>{t()?(clearInterval(c),s()):m&&o()-l>e&&(clearInterval(c),r(new Error("Timeout")))},n)}),h=async(e,t=0,n=10)=>{const s=o(),r=t<=0;for(;r||o()-s<=t;){if(await e())return;await a(n)}throw new Error("Timeout")},a=e=>i((t,n)=>setTimeout(t,e)),I=e=>e instanceof Promise||e&&e.then&&e.catch&&e.finally;export{w as all,i as create,v as createEmpty,I as isPromise,P as reject,u as resolve,T as resolveWith,f as until,h as untilAsync,a as wait};
//# sourceMappingURL=/sm/5de4211df1ed0521719d7005b9dc97315786669806b577d049554c4587bbef84.map