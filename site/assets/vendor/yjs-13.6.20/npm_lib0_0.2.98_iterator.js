/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/iterator.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const a=(t,r)=>({[Symbol.iterator](){return this},next(){const e=t.next();return{value:e.done?void 0:r(e.value),done:e.done}}}),n=t=>({[Symbol.iterator](){return this},next:t}),u=(t,r)=>n(()=>{let e;do e=t.next();while(!e.done&&!r(e.value));return e}),d=(t,r)=>n(()=>{const{done:e,value:o}=t.next();return{done:e,value:e?void 0:r(o)}});export{n as createIterator,u as iteratorFilter,d as iteratorMap,a as mapIterator};
//# sourceMappingURL=/sm/aababf1905a5998ca4b257783245da6e2193800bd3523190667a51e8f747c17d.map