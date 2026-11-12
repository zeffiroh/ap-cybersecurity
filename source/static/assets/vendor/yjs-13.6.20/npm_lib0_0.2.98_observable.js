/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/lib0@0.2.98/observable.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const t=()=>new Map,n=(o,e,r)=>{let s=o.get(e);return s===void 0&&o.set(e,s=r()),s},f=()=>new Set,c=Array.from;class b{constructor(){this._observers=t()}on(e,r){return n(this._observers,e,f).add(r),r}once(e,r){const s=(...i)=>{this.off(e,s),r(...i)};this.on(e,s)}off(e,r){const s=this._observers.get(e);s!==void 0&&(s.delete(r),s.size===0&&this._observers.delete(e))}emit(e,r){return c((this._observers.get(e)||t()).values()).forEach(s=>s(...r))}destroy(){this._observers=t()}}class d{constructor(){this._observers=t()}on(e,r){n(this._observers,e,f).add(r)}once(e,r){const s=(...i)=>{this.off(e,s),r(...i)};this.on(e,s)}off(e,r){const s=this._observers.get(e);s!==void 0&&(s.delete(r),s.size===0&&this._observers.delete(e))}emit(e,r){return c((this._observers.get(e)||t()).values()).forEach(s=>s(...r))}destroy(){this._observers=t()}}export{d as Observable,b as ObservableV2};
//# sourceMappingURL=/sm/8851a8a425e44c28b687ddf3b0926871e9937b33802b7934270adbea8e89f2ff.map