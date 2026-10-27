(function(global){"use strict";function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function inline(s){s=esc(s);s=s.replace(/`([^`]+)`/g,"<code>$1</code>");s=s.replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>");return s;}
function render(md){var lines=(md||"").replace(/\r\n/g,"\n").split("\n");var out=[];var i=0;var listBuf=null;function flushList(){if(!listBuf)return;out.push("<"+listBuf.tag+">"+listBuf.items.map(function(it){return"<li>"+inline(it)+"</li>";}).join("")+"</"+listBuf.tag+">");listBuf=null;}
while(i<lines.length){var line=lines[i];var fence=line.match(/^```(\w*)\s*$/);if(fence){flushList();var codeLines=[];i++;while(i<lines.length&&!/^```\s*$/.test(lines[i])){codeLines.push(lines[i]);i++;}
i++;out.push('<pre class="pg-md-code"><code>'+esc(codeLines.join("\n"))+"</code></pre>");continue;}
var h=line.match(/^(#{1,4})\s+(.*)$/);if(h){flushList();var level=Math.min(h[1].length+3,6);out.push("<h"+level+">"+inline(h[2])+"</h"+level+">");i++;continue;}
var bullet=line.match(/^\s*-\s+(.*)$/);if(bullet){if(!listBuf||listBuf.tag!=="ul"){flushList();listBuf={tag:"ul",items:[]};}
listBuf.items.push(bullet[1]);i++;continue;}
var numbered=line.match(/^\s*\d+\.\s+(.*)$/);if(numbered){if(!listBuf||listBuf.tag!=="ol"){flushList();listBuf={tag:"ol",items:[]};}
listBuf.items.push(numbered[1]);i++;continue;}
flushList();if(/^\s*$/.test(line)){i++;continue;}
var para=[line];i++;while(i<lines.length&&!/^\s*$/.test(lines[i])&&!/^```/.test(lines[i])&&!/^#{1,4}\s/.test(lines[i])&&!/^\s*-\s+/.test(lines[i])&&!/^\s*\d+\.\s+/.test(lines[i])){para.push(lines[i]);i++;}
out.push("<p>"+inline(para.join(" "))+"</p>");}
flushList();return out.join("\n");}
global.MDLite={render:render};})(window);
