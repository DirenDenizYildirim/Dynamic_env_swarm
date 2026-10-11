
var D = JSON.parse(document.getElementById('data').textContent);
var S = {rung: 1, all: false, mde: true, floor: true, k60: false};
(function(){ var h=(location.hash||'').replace('#',''); h.split('&').forEach(function(kv){ var p=kv.split('=');
  if(p[0]==='rung'){ var r=parseInt(p[1],10); if(r>=1&&r<=4) S.rung=r; } if(p[0]==='all'&&p[1]==='1') S.all=true; if(p[0]==='k60'&&p[1]==='1') S.k60=true; }); })();
if(window.matchMedia && window.matchMedia('print').matches) S.all = true;
var RUNGS = [{n:1, t:'1  Γ'}, {n:2, t:'2  Γ₄'}, {n:3, t:'3  Γ₄′'}, {n:4, t:'4  B̂'}];
var rb = document.getElementById('rungs');
RUNGS.forEach(function(r){ var b = U.el('button', {'class':'pill', 'aria-pressed':'false'}, r.t);
  b.addEventListener('click', function(){ S.rung = r.n; S.all = false; render(); }); rb.appendChild(b); });
document.getElementById('prev').onclick = function(){ S.all=false; S.rung = Math.max(1, S.rung-1); render(); };
document.getElementById('next').onclick = function(){ S.all=false; S.rung = Math.min(4, S.rung+1); render(); };
document.getElementById('all').onclick = function(){ S.all = !S.all; if(S.all) S.rung = 4; render(); };
function tog(id, key){ var b = document.getElementById(id); b.onclick = function(){ S[key] = !S[key]; render(); }; }
tog('tmde','mde'); tog('tfloor','floor'); tog('t60','k60');
document.addEventListener('keydown', function(e){
  if(e.key==='ArrowRight'){ S.all=false; S.rung=Math.min(4,S.rung+1); render(); }
  if(e.key==='ArrowLeft'){ S.all=false; S.rung=Math.max(1,S.rung-1); render(); }
  if(/^[1-4]$/.test(e.key)){ S.all=false; S.rung=parseInt(e.key,10); render(); }
});
document.getElementById('foot').textContent = D.foot;

function marker(g, shape, x, y, r){
  var ink = 'var(--ink)', sf = 'var(--surface)';
  if(shape==='dot') g.appendChild(U.svg('circle', {cx:x, cy:y, r:r, fill:ink, stroke:sf, 'stroke-width':2}));
  if(shape==='ring') g.appendChild(U.svg('circle', {cx:x, cy:y, r:r, fill:sf, stroke:ink, 'stroke-width':2}));
  if(shape==='tri') g.appendChild(U.svg('path', {d:'M'+x+','+(y-r*1.25)+'L'+(x+r*1.15)+','+(y+r*0.8)+'L'+(x-r*1.15)+','+(y+r*0.8)+'Z', fill:ink, stroke:sf, 'stroke-width':1.5}));
  if(shape==='diamond') g.appendChild(U.svg('path', {d:'M'+x+','+(y-r*1.3)+'L'+(x+r*1.1)+','+y+'L'+x+','+(y+r*1.3)+'L'+(x-r*1.1)+','+y+'Z', fill:ink, stroke:sf, 'stroke-width':1.5}));
  if(shape==='square') g.appendChild(U.svg('rect', {x:x-r, y:y-r, width:2*r, height:2*r, fill:ink, stroke:sf, 'stroke-width':1.5}));
}
function chip(g, x, y, text, kind){
  var w = 10; for(var i=0;i<text.length;i++){ var ch = text[i]; w += (ch >= 'A' && ch <= 'Z') ? 7.4 : (ch===' ' ? 3.2 : 6.0); }
  var h = 16;
  var fill = kind==='fill' ? 'var(--chipfill)' : (kind==='weak' ? 'url(#stip)' : 'none');
  g.appendChild(U.svg('rect', {x:x, y:y-h+4, width:w, height:h, rx:8, fill:fill, stroke:'var(--ink)', 'stroke-width':1}));
  var t = U.svg('text', {x:x+w/2, y:y-0.5, 'text-anchor':'middle', 'font-size':10.5, 'font-weight':600, 'class':'ct'}, text);
  if(kind==='fill') t.setAttribute('style','fill:var(--chiptext)');
  g.appendChild(t); return w;
}
function visibleRows(){ return D.rows.filter(function(r){ return !(r.optional && !S.k60); }); }

function panel(mt){
  var W = 470, x0 = 14, x1 = W - 14, top = 26;
  var rows = visibleRows();
  var RH = function(r){ return 80 + (r.date ? 13 : 0) + (r.id==='G4' ? 24 : 0); };
  var H = top + rows.reduce(function(a, r){ return a + RH(r) + (r.family ? 18 : 0); }, 0) + 44;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': mt.name + ' contrasts in registered order'});
  var defs = U.svg('defs'); var pat = U.svg('pattern', {id:'stip', width:3, height:3, patternUnits:'userSpaceOnUse'});
  pat.appendChild(U.svg('circle', {cx:1.5, cy:1.5, r:0.75, fill:'var(--muted)'})); defs.appendChild(pat); svg.appendChild(defs);
  var X = function(v){ return x0 + (v - mt.dom[0])/(mt.dom[1]-mt.dom[0])*(x1-x0); };
  var step = (mt.k==='completion') ? 0.02 : 0.005, yAxis = H - 40;
  for(var v = Math.ceil(mt.dom[0]/step)*step; v <= mt.dom[1]+1e-12; v += step){
    var xv = X(v); svg.appendChild(U.svg('line', {x1:xv, x2:xv, y1:top-8, y2:yAxis, 'class': Math.abs(v)<1e-12 ? 'zero':'gl'}));
    svg.appendChild(U.svg('text', {x:xv, y:yAxis+14, 'text-anchor':'middle', 'class':'tick'}, (Math.abs(v)<1e-12?'0':(v>0?'+':'−')+Math.abs(v).toFixed(mt.k==='completion'?2:3))));
  }
  svg.appendChild(U.svg('text', {x:(x0+x1)/2, y:H-6, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, mt.axis));
  var y = top;
  rows.forEach(function(r){
    var d = r.m[mt.k], vis = S.all || r.rung <= S.rung, cur = !S.all && r.rung === S.rung;
    if(r.family){
      var fl = U.svg('text', {x:4, y:y+6, 'font-size':10.5, 'font-style':'italic', style:'fill:var(--muted)'}, r.family);
      svg.appendChild(fl); if(y > top) svg.appendChild(U.svg('line', {x1:2, x2:W-2, y1:y-6, y2:y-6, 'class':'ax'}));
      y += 18;
    }
    var g = U.svg('g', {'class':'row' + (vis && !cur && !S.all ? ' dim' : ''), tabindex: vis ? 0 : null});
    var bg = U.svg('rect', {x:2, y:y-2, width:W-4, height:RH(r)-8, rx:6, fill: cur ? 'var(--hover)' : 'transparent'}); g.appendChild(bg);
    var yy = y + 12;
    var idt = U.svg('text', {x:x0, y:yy, 'font-size':12.5});
    var t1 = U.svg('tspan', {'font-weight':600}, r.sym + '  ' + r.contrast); idt.appendChild(t1);
    g.appendChild(idt); yy += 14;
    g.appendChild(U.svg('text', {x:x0, y:yy, 'font-size':10.5, style:'fill:var(--ink2)'}, r.k + ' · ' + r.unit)); yy += 13;
    if(r.date){ g.appendChild(U.svg('text', {x:x0, y:yy, 'font-size':10.5, style:'fill:var(--muted)'}, r.date)); yy += 13; }
    if(!vis){ g.appendChild(U.svg('text', {x:x0, y:yy+14, 'font-size':11, style:'fill:var(--muted)'}, 'rung ' + r.rung + ': not yet read')); svg.appendChild(g); y += RH(r); return; }
    var cx = x0, cy = yy + 10;
    (r.chips||[]).forEach(function(c){ cx += chip(g, cx, cy, c, 'weak') + 4; });
    if(!r.noverdict) cx += chip(g, cx, cy, d.reject ? 'REJECT' : 'null', d.reject ? 'fill' : 'line') + 8;
    g.appendChild(U.svg('text', {x:cx, y:cy, 'font-size':11.5, 'class':'num'}, (d.est||'') + (d.ci ? '  ' + d.ci : '')));
    var yb = cy + 17;
    if(S.mde && d.band){ g.appendChild(U.svg('rect', {x:X(-d.X), y:yb-8, width:X(d.X)-X(-d.X), height:16, fill:'var(--band)'})); }
    if(S.floor && d.floor){ g.appendChild(U.svg('rect', {x:X(-d.floor), y:yb-8, width:X(d.floor)-X(-d.floor), height:16, fill:'url(#stip)'})); }
    g.appendChild(U.svg('line', {x1:X(d.lo), x2:X(d.hi), y1:yb, y2:yb, stroke:'var(--ink)', 'stroke-width':2}));
    [d.lo, d.hi].forEach(function(v){ g.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:yb-5, y2:yb+5, stroke:'var(--ink)', 'stroke-width':2})); });
    marker(g, r.shape, X(d.gamma), yb, 4.6);
    if(r.id==='G4'){ var cq = D.consequence[mt.k], kind = mt.k==='survival_rate' ? 'fill' : 'line';
      chip(g, x0, yb + 26, cq + (mt.k==='completion' && d.Xt ? ', X₄ = ' + d.Xt : ''), kind); }
    var lines = [[r.sym + ' = ' + r.contrast, '· ' + mt.name]];
    if(!r.noverdict) lines.push(((r.chips||[]).concat([d.reject ? 'REJECT' : 'null'])).join(' · ') + ' at Šidák z_α (m = 2)');
    else lines.push('no registered test: estimate and interval only');
    if(d.est) lines.push(['estimate', d.est]); if(d.ci) lines.push(['Šidák 95 % CI', d.ci]); if(d.z) lines.push(['z', d.z]);
    if(d.Xt) lines.push(['80 %-power MDE, X', d.Xt]);
    lines.push(r.k.replace(' †','') + ' · ' + r.unit);
    g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
    g.addEventListener('mouseleave', function(){ U.tip.hide(); });
    g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
    svg.appendChild(g); y += RH(r);
  });
  return svg;
}
function table(){
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table');
  var hr = U.el('tr'); ['contrast','k','metric','reading','estimate','Šidák 95 % CI','z'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  visibleRows().forEach(function(r){ D.metrics.forEach(function(mt){ var d = r.m[mt.k], tr = U.el('tr');
    [r.sym + ' = ' + r.contrast, r.k.replace(' †',''), mt.name, r.noverdict ? '—' : ((r.chips||[]).join(' ') + ' ' + (d.reject?'REJECT':'null')).trim(), d.est||'', d.ci||'(plotted)', d.z||''].forEach(function(c){ tr.appendChild(U.el('td', null, c)); });
    tb.appendChild(tr); }); });
  host.appendChild(tb);
}
function render(){
  Array.prototype.forEach.call(rb.children, function(b, i){ b.setAttribute('aria-pressed', (!S.all && i+1===S.rung) ? 'true':'false'); });
  document.getElementById('all').setAttribute('aria-pressed', S.all?'true':'false');
  document.getElementById('tmde').setAttribute('aria-pressed', S.mde?'true':'false');
  document.getElementById('tfloor').setAttribute('aria-pressed', S.floor?'true':'false');
  document.getElementById('t60').setAttribute('aria-pressed', S.k60?'true':'false');
  var host = document.getElementById('panels'); U.clear(host);
  D.metrics.forEach(function(mt){ var p = U.el('div', {'class':'panel'}); p.appendChild(U.el('h3', null, mt.name)); p.appendChild(panel(mt)); host.appendChild(p); });
  table(); U.tip.hide(); if(window.__fit) window.__fit();
}
window.__redraw = render;
window.addEventListener('beforeprint', function(){ S.all = true; render(); });
render();
