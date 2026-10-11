
var D = JSON.parse(document.getElementById('data').textContent);
var S = {m:'survival_rate', pred:true};
function hover(g, lines){
  g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
  g.addEventListener('mouseleave', function(){ U.tip.hide(); });
  g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
}
function simplex(){
  var W = 380, H = 330, l = 46, r = 16, t = 14, b = 44, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'training simplex in p and n'});
  var X = function(p){ return l + p*(W-l-r); }, Y = function(n){ return t + (1-n)*(H-t-b); };
  svg.appendChild(U.svg('path', {d:'M'+X(0)+','+Y(0)+'L'+X(1)+','+Y(0)+'L'+X(0)+','+Y(1)+'Z', fill:'var(--band)'}));
  [0,0.25,0.5,0.75,1].forEach(function(v){
    svg.appendChild(U.svg('text', {x:X(v), y:H-b+15, 'text-anchor':'middle', 'class':'tick'}, String(v)));
    svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, String(v))); });
  svg.appendChild(U.svg('line', {x1:X(0), x2:X(1), y1:Y(0), y2:Y(0), 'class':'ax'}));
  svg.appendChild(U.svg('line', {x1:X(0), x2:X(0), y1:Y(0), y2:Y(1), 'class':'ax'}));
  svg.appendChild(U.svg('text', {x:(X(0)+X(1))/2, y:H-8, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, 'p, share of episodes with A + B together'));
  svg.appendChild(U.svg('text', {x:12, y:(Y(0)+Y(1))/2, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)', transform:'rotate(-90 12 '+((Y(0)+Y(1))/2)+')'}, 'n, fire-only share'));
  // iso-marginal reference lines p − n = 2m − 1 inside the simplex
  D.isom.forEach(function(q){ var c = q.c; // p - n = c
    var pts = []; // intersections with p=0, n=0, p+n=1
    if(c<=0 && -c<=1) pts.push([0, -c]); if(c>=0 && c<=1) pts.push([c, 0]); var pp = (1+c)/2, nn = (1-c)/2; if(pp>=0&&pp<=1&&nn>=0&&nn<=1) pts.push([pp, nn]);
    if(pts.length<2 || (pts[0][0]===pts[1][0] && pts[0][1]===pts[1][1])) return;
    svg.appendChild(U.svg('line', {x1:X(pts[0][0]), y1:Y(pts[0][1]), x2:X(pts[1][0]), y2:Y(pts[1][1]), stroke:'var(--muted)', 'stroke-width':0.8}));
    var e = pts[pts.length-1]; svg.appendChild(U.svg('text', {x:X(e[0])+7, y:Y(e[1])+(q.m==='0.5'?12:-2), 'font-size':10, style:'fill:var(--muted)'}, 'm = ' + q.m)); });
  // sampled region: hull of the 8 arms
  svg.appendChild(U.svg('path', {d:'M'+X(0)+','+Y(0)+'L'+X(0.5)+','+Y(0.5)+'L'+X(0.4)+','+Y(0.6)+'L'+X(0)+','+Y(0.2)+'Z', fill:'var(--muted)', 'fill-opacity':0.18, stroke:'var(--muted)', 'stroke-width':0.8}));
  svg.appendChild(U.svg('text', {x:X(0.13), y:Y(0.29), 'font-size':10, style:'fill:var(--ink2);paint-order:stroke;stroke:var(--band);stroke-width:3px'}, 'sampled region'));
  D.arms.forEach(function(a){ var g = U.svg('g', {'class':'it', tabindex:0}), x = X(a.p), y = Y(a.n);
    g.appendChild(U.svg('circle', {'class':'hit', cx:x, cy:y, r:11, fill:'transparent'}));
    if(a.kind==='sweep') g.appendChild(U.svg('circle', {cx:x, cy:y, r:4.6, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':2}));
    else g.appendChild(U.svg('rect', {x:x-4, y:y-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.6}));
    hover(g, [[a.arm, ''], 'p ' + a.p + ' · n ' + (+a.n.toFixed(3)) + ' · m ' + a.m, 'k = 20']); svg.appendChild(g); });
  D.refs.forEach(function(a){ var g = U.svg('g', {'class':'it', tabindex:0}), x = X(a.p), y = Y(a.n);
    g.appendChild(U.svg('circle', {'class':'hit', cx:x, cy:y, r:12, fill:'transparent'}));
    g.appendChild(U.svg('circle', {cx:x, cy:y, r:8, fill:'none', stroke:'var(--ink)', 'stroke-width':1.8}));
    var lab = a.arm==='JOINT' ? 'JOINT, m = 1' : (a.arm==='ISO' ? 'ISO' : 'ISO-4');
    var tx = a.arm==='JOINT' ? x-10 : x+12, anchor = a.arm==='JOINT' ? 'end' : 'start', ty = a.arm==='JOINT' ? y-12 : (a.arm==='ISO' ? y+4 : y-10);
    g.appendChild(U.svg('text', {x:tx, y:ty, 'text-anchor':anchor, 'font-size':12, 'font-weight':600, style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, lab));
    hover(g, [[a.arm, ''], 'p ' + (+a.p.toFixed(3)) + ' · n ' + (a.arm==='ISO' ? '1/3' : a.n) + ' · m ' + a.m]); svg.appendChild(g); });
  return svg;
}
function meansPanel(){
  var mt = D.metrics[S.m], W = 380, H = 170, l = 46, r = 16, t = 10, b = 34;
  var vals = []; Object.keys(mt.means).forEach(function(k){ vals.push(mt.means[k].mean, mt.means[k].fit); });
  var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), pad = (hi-lo)*0.15; lo -= pad; hi += pad;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'arm means against p'});
  var X = function(p){ return l + p/0.55*(W-l-r); }, Y = function(v){ return t + (hi-v)/(hi-lo)*(H-t-b); };
  [0,0.125,0.25,0.375,0.5].forEach(function(p){ svg.appendChild(U.svg('text', {x:X(p), y:H-b+14, 'text-anchor':'middle', 'class':'tick'}, String(p))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-4, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)'}, 'p'));
  svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:H-b, y2:H-b, 'class':'ax'}));
  svg.appendChild(U.svg('text', {x:l-6, y:t+8, 'text-anchor':'end', 'class':'tick'}, 'higher'));
  svg.appendChild(U.svg('text', {x:l-6, y:H-b-2, 'text-anchor':'end', 'class':'tick'}, 'lower'));
  D.arms.forEach(function(a){ var d = mt.means[a.arm], x = X(a.p) + (a.kind==='ident'?5:-5);
    svg.appendChild(U.svg('line', {x1:x-7, x2:x+7, y1:Y(d.fit), y2:Y(d.fit), stroke:'var(--muted)', 'stroke-width':1.5}));
    var g = U.svg('g', {'class':'it', tabindex:0});
    g.appendChild(U.svg('circle', {'class':'hit', cx:x, cy:Y(d.mean), r:10, fill:'transparent'}));
    if(a.kind==='sweep') g.appendChild(U.svg('circle', {cx:x, cy:Y(d.mean), r:4.4, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':2}));
    else g.appendChild(U.svg('rect', {x:x-4, y:Y(d.mean)-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.6}));
    hover(g, [[a.arm, ''], 'arm mean (point) and the committed plane fit at this arm (grey tick)']); svg.appendChild(g); });
  return svg;
}
function estPanel(){
  var mt = D.metrics[S.m], rows = [].concat([{group:'secondary estimates, 95 %'}], mt.sec, S.pred ? mt.pred : []);
  var W = 470, rowH = 40, top = 8, H = top + rows.reduce(function(a, r){ return a + (r.group ? 22 : rowH); }, 0) + 40, x0 = 14, x1 = W - 14;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'secondary estimates and the plane prediction against measured contrasts'});
  var X = function(v){ return x0 + (v - mt.dom[0])/(mt.dom[1]-mt.dom[0])*(x1-x0); }, yAx = H - 32;
  var step = S.m==='survival_rate' ? 0.01 : 0.05;
  for(var v = Math.ceil(mt.dom[0]/step)*step; v <= mt.dom[1]+1e-12; v += step){ var xv = X(v);
    svg.appendChild(U.svg('line', {x1:xv, x2:xv, y1:top, y2:yAx, 'class': Math.abs(v)<1e-12 ? 'zero':'gl'}));
    svg.appendChild(U.svg('text', {x:xv, y:yAx+14, 'text-anchor':'middle', 'class':'tick'}, Math.abs(v)<1e-12 ? '0' : (v>0?'+':'−') + Math.abs(v).toFixed(2))); }
  svg.appendChild(U.svg('text', {x:(x0+x1)/2, y:H-4, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)'}, 'Δ ' + mt.name + ' (fraction), or per unit p / n'));
  var y = top;
  rows.forEach(function(r){
    if(r.group){ svg.appendChild(U.svg('text', {x:x0, y:y+15, 'font-size':10.5, 'font-style':'italic', style:'fill:var(--muted)'}, r.group)); y += 22; return; }
    var g = U.svg('g', {'class':'it', tabindex:0}), yb = y + 26;
    g.appendChild(U.svg('rect', {'class':'hit', x:2, y:y, width:W-4, height:rowH-2, fill:'transparent', rx:5}));
    g.appendChild(U.svg('text', {x:x0, y:y+11, 'font-size':11.5, style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, r.label + (r.est ? ':  ' + r.est + (r.ci ? ' ' + r.ci : '') : '')));
    var meas = r.kind==='meas';
    if(r.lo !== null){ g.appendChild(U.svg('line', {x1:X(r.lo), x2:X(r.hi), y1:yb, y2:yb, stroke:'var(--ink)', 'stroke-width': meas ? 2 : 1.1}));
      if(meas) [r.lo, r.hi].forEach(function(v){ g.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:yb-4, y2:yb+4, stroke:'var(--ink)', 'stroke-width':2})); }); }
    var x = X(r.g);
    if(r.kind==='sec') g.appendChild(U.svg('circle', {cx:x, cy:yb, r:4, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    if(r.kind==='pred') g.appendChild(U.svg('path', {d:'M'+x+','+(yb-5.5)+'L'+(x+5)+','+yb+'L'+x+','+(yb+5.5)+'L'+(x-5)+','+yb+'Z', fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    if(meas){ var sh = r.key==='g4' ? 'M'+x+','+(yb-5.5)+'L'+(x+5)+','+(yb+4)+'L'+(x-5)+','+(yb+4)+'Z' : r.key==='g4p' ? 'M'+x+','+(yb-6)+'L'+(x+5)+','+yb+'L'+x+','+(yb+6)+'L'+(x-5)+','+yb+'Z' : 'M'+(x-4.5)+','+(yb-4.5)+'h9v9h-9Z';
      g.appendChild(U.svg('path', {d:sh, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5})); }
    var lines = [[r.label, '']]; if(r.est) lines.push(['estimate', r.est]); if(r.ci) lines.push([meas ? 'Šidák 95 % CI' : '95 % CI', r.ci]);
    lines.push(meas ? 'measured contrast; Šidák 95 %' : (r.kind==='pred' ? 'plane prediction; secondary, non-verdict-bearing' : 'secondary, non-verdict-bearing; 95 % bootstrap, not family-corrected'));
    hover(g, lines); svg.appendChild(g); y += rowH;
  });
  return svg;
}
function table(){
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['metric','row','estimate','interval'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  Object.keys(D.metrics).forEach(function(k){ var mt = D.metrics[k]; mt.sec.concat(mt.pred).filter(function(r){ return !r.group; }).forEach(function(r){ var tr = U.el('tr');
    [mt.name, r.label, r.est || '(plotted)', r.ci || (r.lo===null ? '—' : '(plotted)')].forEach(function(c){ tr.appendChild(U.el('td', null, c)); }); tb.appendChild(tr); }); });
  host.appendChild(tb);
}
function render(){
  document.getElementById('msurv').setAttribute('aria-pressed', S.m==='survival_rate'?'true':'false');
  document.getElementById('mcomp').setAttribute('aria-pressed', S.m==='completion'?'true':'false');
  document.getElementById('tpred').setAttribute('aria-pressed', S.pred?'true':'false');
  var a = document.getElementById('simplex'); U.clear(a); a.appendChild(simplex());
  var b = document.getElementById('means'); U.clear(b); b.appendChild(meansPanel());
  var c = document.getElementById('est'); U.clear(c); c.appendChild(estPanel());
  document.getElementById('mh').textContent = 'arm means at θ*, ' + D.metrics[S.m].name + ', k = 20 per arm (grey tick: committed plane fit)';
  document.getElementById('eh').textContent = D.metrics[S.m].name + ': estimates';
  table(); U.tip.hide(); if(window.__fit) window.__fit();
}
document.getElementById('msurv').onclick = function(){ S.m='survival_rate'; render(); };
document.getElementById('mcomp').onclick = function(){ S.m='completion'; render(); };
document.getElementById('tpred').onclick = function(){ S.pred=!S.pred; render(); };
window.__redraw = render; render();
