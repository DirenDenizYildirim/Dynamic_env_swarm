
var D = JSON.parse(document.getElementById('data').textContent);
var S = {single:false, floor:true};
function panel(mt){
  var W = 470, H = 316, l = 62, r = 14, top = 60, bot = 46;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': mt.name + ': Γ(t) at 11 checkpoints'});
  var defs = U.svg('defs'); var pat = U.svg('pattern', {id:'stip'+mt.k, width:3, height:3, patternUnits:'userSpaceOnUse'});
  pat.appendChild(U.svg('circle', {cx:1.5, cy:1.5, r:0.75, fill:'var(--muted)'})); defs.appendChild(pat); svg.appendChild(defs);
  var X = function(t){ return l + (t-475)/(1025-475)*(W-l-r); }, Y = function(v){ return top + (mt.dom[1]-v)/(mt.dom[1]-mt.dom[0])*(H-top-bot); };
  var step = mt.k==='completion' ? 0.01 : 0.005;
  for(var v = Math.ceil(mt.dom[0]/step)*step; v <= mt.dom[1]+1e-12; v += step){
    svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:Y(v), y2:Y(v), 'class': Math.abs(v)<1e-12 ? 'zero':'gl'}));
    svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, Math.abs(v)<1e-12 ? '0' : (v>0?'+':'−') + Math.abs(v).toFixed(mt.k==='completion'?2:3)));
  }
  [500,600,700,800,900,1000].forEach(function(t){ svg.appendChild(U.svg('text', {x:X(t), y:H-bot+16, 'text-anchor':'middle', 'class':'tick'}, String(t))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-8, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, 'training update t'));
  svg.appendChild(U.svg('text', {x:12, y:(top+H-bot)/2, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)', transform:'rotate(-90 12 '+((top+H-bot)/2)+')'}, 'Γ(t), Δ ' + mt.name));
  // which intervals are registered: only t = T* = 1000 (labels, before the marks)
  var xa = X(500) - 9, xb = X(950) + 9, yb = 38;
  svg.appendChild(U.svg('path', {d:'M'+xa+','+(yb+5)+'V'+yb+'H'+xb+'V'+(yb+5), fill:'none', stroke:'var(--muted)', 'stroke-width':1}));
  svg.appendChild(U.svg('text', {x:(xa+xb)/2, y:yb-3, 'text-anchor':'middle', 'font-size':10, style:'fill:var(--ink2)'}, 'descriptive intervals (no registered test at t ≠ T*)'));
  svg.appendChild(U.svg('text', {x:X(1000), y:yb-3, 'text-anchor':'middle', 'font-size':10, 'font-weight':600}, 'T*'));
  svg.appendChild(U.svg('text', {x:X(1000), y:yb+9, 'text-anchor':'middle', 'font-size':9.5, style:'fill:var(--ink2)'}, 'registered'));
  // sign string, first
  svg.appendChild(U.svg('text', {x:l-6, y:20, 'text-anchor':'end', 'font-size':10.5, style:'fill:var(--muted)'}, 'sign'));
  mt.pts.forEach(function(p){
    if(p.disagree) svg.appendChild(U.svg('circle', {cx:X(p.t), cy:16, r:8, fill:'none', stroke:'var(--ink)', 'stroke-width':1.3}));
    svg.appendChild(U.svg('text', {x:X(p.t), y:21, 'text-anchor':'middle', 'font-size':14, 'font-weight':600}, p.sign==='+'?'+':'−'));
  });
  if(S.floor){ var x = X(1000); svg.appendChild(U.svg('rect', {x:x-13, y:Y(mt.floor), width:26, height:Y(-mt.floor)-Y(mt.floor), fill:'url(#stip'+mt.k+')'})); }
  mt.pts.forEach(function(p){
    var q = (S.single && p.t===1000) ? Object.assign({}, p, mt.single) : p;
    var g = U.svg('g', {'class':'pt', tabindex:0}), x = X(q.t);
    g.appendChild(U.svg('rect', {'class':'hit', x:x-12, y:top-6, width:24, height:H-top-bot+6, fill:'transparent', rx:4}));
    var sw = q.t===1000 ? 2.4 : 1.4;
    g.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(q.lo), y2:Y(q.hi), stroke:'var(--ink)', 'stroke-width':sw}));
    [q.lo, q.hi].forEach(function(v){ g.appendChild(U.svg('line', {x1:x-4, x2:x+4, y1:Y(v), y2:Y(v), stroke:'var(--ink)', 'stroke-width':sw})); });
    var single = S.single && p.t===1000;
    g.appendChild(U.svg('circle', {cx:x, cy:Y(q.g), r:4.4, fill: single ? 'var(--surface)' : 'var(--ink)', stroke: single ? 'var(--ink)' : 'var(--surface)', 'stroke-width':2}));
    var lines = [['t = ' + q.t, '· ' + mt.name], ['sign', p.sign==='+'?'+':'−'] ];
    if(q.est) lines.push(['Γ(t)', q.est]); if(q.ci) lines.push([q.t===1000 ? 'Šidák 95 % CI' : 'Šidák 95 % CI, descriptive', q.ci]);
    lines.push(q.t===1000 ? (single ? 'post-unblind card (single-card curve), descriptive' : 'grid card, the registered Γ') : 'post-unblind card; descriptive (no registered test at t ≠ T*)');
    g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
    g.addEventListener('mouseleave', function(){ U.tip.hide(); });
    g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
    svg.appendChild(g);
  });
  return svg;
}
function render(){
  document.getElementById('tsingle').setAttribute('aria-pressed', S.single?'true':'false');
  document.getElementById('tfloor').setAttribute('aria-pressed', S.floor?'true':'false');
  var host = document.getElementById('panels'); U.clear(host);
  D.metrics.forEach(function(mt){ var p = U.el('div', {'class':'panel'}), h = U.el('h3');
    h.appendChild(U.el('span', {'class':'chip line'}, D.verdict)); h.appendChild(document.createTextNode(mt.name));
    p.appendChild(h); p.appendChild(panel(mt)); host.appendChild(p); });
  var host2 = document.getElementById('tbl'); U.clear(host2); var tb = U.el('table'), hr = U.el('tr');
  ['metric','t','sign','Γ(t)','Šidák 95 % CI (t ≠ 1000: descriptive)'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.metrics.forEach(function(mt){ mt.pts.forEach(function(p){ var tr = U.el('tr');
    [mt.name, p.t, p.sign==='+'?'+':'−', p.est||'(plotted)', p.ci||'(plotted)'].forEach(function(c){ tr.appendChild(U.el('td', null, String(c))); }); tb.appendChild(tr); }); });
  host2.appendChild(tb); U.tip.hide(); if(window.__fit) window.__fit();
}
document.getElementById('tsingle').onclick = function(){ S.single = !S.single; render(); };
document.getElementById('tfloor').onclick = function(){ S.floor = !S.floor; render(); };
window.__redraw = render; render();
