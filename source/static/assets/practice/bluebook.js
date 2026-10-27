
// Bluebook-like single-question, distraction-free quiz runner.
// Reads window.QUIZ = {atom, title, items:[{id,type,prompt,options,answer,accept,points,explain,grader}]}.
(function(){
  var quiz = window.QUIZ;
  if(!quiz) return;
  var items = quiz.items.filter(function(it){ return it.type !== 'code'; });
  var codeItems = quiz.items.filter(function(it){ return it.type === 'code'; });
  var idx = 0;
  var answers = {};
  var root = document.getElementById('bb-root');

  function saveResult(score, max){
    var key = 'bb_results';
    var all = {};
    try{ all = JSON.parse(localStorage.getItem(key)||'{}'); }catch(e){}
    var prev = all[quiz.atom] || {attempts:0};
    all[quiz.atom] = {score:score, max:max, attempts:(prev.attempts||0)+1, last: Date.now()};
    localStorage.setItem(key, JSON.stringify(all));
  }

  // Exit-ticket use: also send the auto-graded score to the class gradebook
  // (platform backend-client.js; saved locally, mirrored to Neon if set up).
  function submitToGradebook(score, max){
    if(!window.Backend || !window.Identity || !max) return;
    Identity.ensureEmail(function(email){
      Backend.submit({
        email: email,
        topic_id: quiz.atom.split('.').slice(0,2).join('.'),
        atom_id: quiz.atom,
        kind: 'atom_quiz',
        item_id: 'atom-quiz-' + quiz.atom,
        correct: score === max,
        points: score,
        maxPoints: max,
        response: '',
        explanation: quiz.title
      });
    });
  }

  function renderPalette(){
    var html = '<div class="bb-palette">';
    items.forEach(function(it,i){
      var st = answers[it.id]!==undefined ? 'answered' : 'unanswered';
      html += '<span class="bb-dot bb-'+st+(i===idx?' bb-current':'')+'" onclick="window.__bbGo('+i+')">'+(i+1)+'</span>';
    });
    html += '</div>';
    return html;
  }

  window.__bbGo = function(i){ idx = i; renderQuestion(); };

  function renderQuestion(){
    var it = items[idx];
    var html = '<div class="bb-shell">';
    html += '<div class="bb-top">Question '+(idx+1)+' of '+items.length+', '+quiz.title+'</div>';
    html += renderPalette();
    html += '<div class="bb-q"><p><b>'+esc(it.prompt)+'</b></p>';
    if(it.type==='mcq'){
      it.options.forEach(function(opt,i){
        var checked = answers[it.id]===i ? 'checked' : '';
        html += '<label class="bb-opt"><input type="radio" name="opt" '+checked+' onclick="window.__bbAns('+i+')"> '+esc(opt)+'</label>';
      });
    } else if(it.type==='multi'){
      it.options.forEach(function(opt,i){
        var sel = (answers[it.id]||[]).indexOf(i) >= 0 ? 'checked' : '';
        html += '<label class="bb-opt"><input type="checkbox" '+sel+' onclick="window.__bbAnsMulti('+i+')"> '+esc(opt)+'</label>';
      });
    } else if(it.type==='short'){
      html += '<input type="text" class="bb-short" value="'+esc(answers[it.id]||'')+'" oninput="window.__bbAnsText(this.value)">';
    }
    html += '</div>';
    html += '<div class="bb-nav">';
    html += '<button class="btn" '+(idx===0?'disabled':'')+' onclick="window.__bbPrev()">&larr; Back</button>';
    if(idx < items.length-1){
      html += '<button class="btn" onclick="window.__bbNext()">Next &rarr;</button>';
    } else {
      html += '<button class="btn" onclick="window.__bbReview()">Review &amp; submit</button>';
    }
    html += '</div></div>';
    root.innerHTML = html;
  }

  window.__bbAns = function(i){ answers[items[idx].id] = i; };
  window.__bbAnsMulti = function(i){
    var it = items[idx];
    var arr = answers[it.id] || [];
    var p = arr.indexOf(i);
    if(p>=0) arr.splice(p,1); else arr.push(i);
    answers[it.id] = arr;
  };
  window.__bbAnsText = function(v){ answers[items[idx].id] = v; };
  window.__bbNext = function(){ idx = Math.min(items.length-1, idx+1); renderQuestion(); };
  window.__bbPrev = function(){ idx = Math.max(0, idx-1); renderQuestion(); };

  window.__bbReview = function(){
    var html = '<div class="bb-shell"><div class="bb-top">Review, '+quiz.title+'</div>';
    html += renderPalette();
    html += '<p>'+items.length+' question(s). Unanswered are marked in red. Submit when ready.</p>';
    html += '<button class="btn" onclick="window.__bbSubmit()">Submit quiz</button></div>';
    root.innerHTML = html;
  };

  function grade(){
    var score = 0, max = 0, rows = [];
    items.forEach(function(it){
      max += it.points||1;
      var a = answers[it.id];
      var correct = false;
      if(it.type==='mcq'){ correct = a===it.answer; }
      else if(it.type==='multi'){
        var got=(a||[]).slice().sort().join(',');
        var want=(it.answer||[]).slice().sort().join(',');
        correct = got===want && got!=='';
      } else if(it.type==='short'){
        var v=(a||'').toLowerCase().trim();
        correct = (it.accept||[]).some(function(s){ return v.indexOf(s.toLowerCase())>=0; });
      }
      if(correct) score += it.points||1;
      rows.push({it:it, a:a, correct:correct});
    });
    return {score:score, max:max, rows:rows};
  }

  window.__bbSubmit = function(){
    var g = grade();
    saveResult(g.score, g.max + codeItems.reduce(function(s,it){return s+(it.points||1);},0));
    submitToGradebook(g.score, g.max);
    var html = '<div class="bb-shell"><div class="bb-top">Results, '+quiz.title+'</div>';
    html += '<p><b>Score: '+g.score+' / '+g.max+'</b></p>';
    g.rows.forEach(function(r){
      html += '<div class="bb-result '+(r.correct?'ok':'bad')+'"><b>'+(r.correct?'Correct':'Incorrect')+'</b>, '+esc(r.it.prompt)+'<br><span class="lo">'+esc(r.it.explain||'')+'</span></div>';
    });
    if(codeItems.length){
      html += '<p class="lo">'+codeItems.length+' coding item(s): graded on the Code page.</p>';
    }
    html += '<a class="btn" href="../../../results.html">Saved results</a>';
    html += '</div>';
    root.innerHTML = html;
  };

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  var style = document.createElement('style');
  style.textContent = '.bb-shell{max-width:760px;margin:8px 0 0;}'+
    '.bb-top{font-weight:650;border-bottom:1px solid var(--aa-line);padding-bottom:8px;margin-bottom:10px;}'+
    '.bb-palette{margin-bottom:12px;}'+
    '.bb-dot{display:inline-block;width:26px;height:26px;text-align:center;line-height:24px;margin:2px;border:1px solid var(--aa-line);border-radius:4px;cursor:pointer;font-size:12px;}'+
    '.bb-answered{background:var(--aa-accent-tint);} .bb-unanswered{background:var(--aa-soft);} .bb-current{outline:2px solid var(--aa-accent);}'+
    '.bb-opt{display:block;padding:8px 10px;margin:6px 0;border:1px solid var(--aa-line);border-radius:4px;cursor:pointer;}'+
    '.bb-opt:hover{border-color:var(--aa-accent);}'+
    '.bb-short{width:100%;padding:8px;font-family:var(--aa-mono);border:1px solid var(--aa-line);border-radius:4px;}'+
    '.bb-nav{margin-top:16px;display:flex;justify-content:space-between;}'+
    '.bb-result{border:1px solid var(--aa-line);border-radius:4px;padding:8px 10px;margin:8px 0;font-size:14.5px;}'+
    '.bb-result.ok{background:var(--aa-accent-tint);} .bb-result.bad{background:#fdecec;}';
  document.head.appendChild(style);

  renderQuestion();
})();
