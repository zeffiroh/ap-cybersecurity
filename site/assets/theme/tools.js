(function(global){"use strict";var TOOLS={};function register(def){if(!def||!/^[a-z0-9][a-z0-9-]*$/.test(def.id||"")||typeof def.mount!=="function")throw new Error("A tool needs an id and a mount function.");TOOLS[def.id]=def;}
function get(id){return Object.prototype.hasOwnProperty.call(TOOLS,id)?TOOLS[id]:null;}
function list(){return Object.keys(TOOLS).map(function(k){return TOOLS[k];});}
function fence(id,state){return"```tool "+id+"\n"+JSON.stringify(state)+"\n```";}
function parse(text){try{var v=JSON.parse(text);return v&&typeof v==="object"&&!Array.isArray(v)?v:null;}catch(e){return null;}}
global.AayatTools={register:register,get:get,list:list,fence:fence,parse:parse};})(window);
