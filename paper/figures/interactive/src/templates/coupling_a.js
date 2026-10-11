
var D = JSON.parse(document.getElementById('data').textContent);
function hover(g, lines){ g.setAttribute('tabindex', 0);
  g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); }); g.addEventListener('mouseleave', function(){ U.tip.hide(); });
  g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); }); }
function frame(W, H, l, b, t, r, ymin, ymax, yticks, fmt, ylab){
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img'}), Y = function(v){ return t + (ymax-v)/(ymax-ymin)*(H-t-b); };
  yticks.forEach(function(v){ svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:Y(v), y2:Y(v), 'class':'gl'})); svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, fmt(v))); });
  svg.appendChild(U.svg('text', {x:12, y:(t+H-b)/2, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)', transform:'rotate(-90 12 '+((t+H-b)/2)+')'}, ylab));
  return {svg:svg, Y:Y};
}
function panelA(){
  var W = 420, H = 250, l = 48, b = 40, t = 40, r = 14, f = frame(W, H, l, b, t, r, 0, 4.6, [0,1,2,3,4], String, 'per episode'), svg = f.svg, Y = f.Y;
  var X = function(i){ return l + 40 + i*((W-l-r-80)/2); };
  D.sev.forEach(function(s, i){ svg.appendChild(U.svg('text', {x:X(i), y:H-b+16, 'text-anchor':'middle', 'class':'tick'}, s.name)); svg.appendChild(U.svg('text', {x:X(i), y:H-b+29, 'text-anchor':'middle', 'class':'tick'}, 'β ' + s.beta.toFixed(2))); });
  D.seeded.forEach(function(sr, j){ var off = j ? 9 : -9;
    sr.vals.forEach(function(v, i){ var g = U.svg('g'), x = X(i) + off;
      g.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(v.lo), y2:Y(v.hi), stroke:'var(--ink)', 'stroke-width':1.5}));
      if(j===0) g.appendChild(U.svg('circle', {cx:x, cy:Y(v.mean), r:4.4, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
      else g.appendChild(U.svg('rect', {x:x-4, y:Y(v.mean)-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
      hover(g, [[sr.series, '· ' + D.sev[i].name], ['seeded ignitions per episode', sr.text[i]]]); svg.appendChild(g); });
    svg.appendChild(U.svg('text', {x:l+4, y:12 + j*14, 'font-size':11}, (j ? '■ ' : '● ') + sr.series + ' · Low / High ' + sr.fall));
  });
  return svg;
}
function panelB(){
  var W = 420, H = 250, l = 48, b = 40, t = 12, r = 96, f = frame(W, H, l, b, t, r, 0.10, 0.25, [0.10,0.15,0.20,0.25], function(v){ return v.toFixed(2); }, 'share'), svg = f.svg, Y = f.Y;
  var X = function(i){ return l + 30 + i*((W-l-r-60)/2); };
  var lo = Math.min.apply(null, D.shares.map(function(s){return s.mean;})), hi = Math.max.apply(null, D.shares.map(function(s){return s.mean;}));
  svg.appendChild(U.svg('rect', {x:l, y:Y(hi), width:W-l-r, height:Y(lo)-Y(hi), fill:'var(--band)'}));
  svg.appendChild(U.svg('text', {x:W-r+6, y:(Y(hi)+Y(lo))/2+4, 'font-size':11}, D.share_range));
  svg.appendChild(U.svg('text', {x:W-r+6, y:(Y(hi)+Y(lo))/2+18, 'font-size':10, style:'fill:var(--muted)'}, 'range, 9 cells'));
  D.sev.forEach(function(s, i){ svg.appendChild(U.svg('text', {x:X(i), y:H-b+16, 'text-anchor':'middle', 'class':'tick'}, s.name)); });
  var ser = ['m44, κ_B 1.0 arm', 'm44, κ_B 0 arm', 'm35, κ_A on arm'];
  D.shares.forEach(function(s){ var j = ser.indexOf(s.series), i = D.sev.findIndex(function(q){return q.name===s.sev;}), x = X(i) + (j-1)*12, g = U.svg('g');
    g.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(s.lo), y2:Y(s.hi), stroke:'var(--muted)', 'stroke-width':1.2}));
    if(j===0) g.appendChild(U.svg('circle', {cx:x, cy:Y(s.mean), r:4, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
    if(j===1) g.appendChild(U.svg('circle', {cx:x, cy:Y(s.mean), r:4, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    if(j===2) g.appendChild(U.svg('rect', {x:x-4, y:Y(s.mean)-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    hover(g, [[s.series, '· ' + s.sev], 'inside the range ' + D.share_range]); svg.appendChild(g); });
  svg.appendChild(U.svg('text', {x:l+4, y:t+12, 'font-size':10, style:'fill:var(--muted)'}, '● m44 κ_B 1.0 · ○ m44 κ_B 0 · ■ m35 κ_A on'));
  return svg;
}
function panelC(){
  var p = D.prop3, W = 420, H = 250, l = 54, b = 40, t = 12, r = 14, f = frame(W, H, l, b, t, r, 0, 500, [0,100,200,300,400,500], String, 'E[B_T], burnt cells at the horizon'), svg = f.svg, Y = f.Y;
  var X = function(v){ return l + v/11*(W-l-r); };
  [0,2,4,6,8,10].forEach(function(v){ svg.appendChild(U.svg('text', {x:X(v), y:H-b+16, 'text-anchor':'middle', 'class':'tick'}, String(v))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-6, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)'}, 'E[N_seeds], collapse-seeded ignitions per run'));
  var xe = Math.min(11, 500/p.slope); svg.appendChild(U.svg('line', {x1:X(0), y1:Y(0), x2:X(xe), y2:Y(p.slope*xe), stroke:'var(--ink2)', 'stroke-width':1.2}));
  p.x.forEach(function(x, i){ var g = U.svg('g');
    g.appendChild(U.svg('line', {x1:X(x), x2:X(x), y1:Y(p.y[i]-p.se[i]), y2:Y(p.y[i]+p.se[i]), stroke:'var(--ink)', 'stroke-width':1.5}));
    g.appendChild(U.svg('circle', {cx:X(x), cy:Y(p.y[i]), r:4.2, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
    hover(g, [['λ₀ sweep point', ''], 'mean ± 1 SE']); svg.appendChild(g); });
  svg.appendChild(U.svg('text', {x:l+10, y:t+14, 'font-size':11.5}, 'committed through-origin fit, R² ' + p.r2));
  return svg;
}
function render(){
  [['pA', panelA], ['pB', panelB], ['pC', panelC]].forEach(function(q){ var h = document.getElementById(q[0]); U.clear(h); h.appendChild(q[1]()); });
  document.getElementById('p3n').textContent = D.prop3.note;
  var c = document.getElementById('pD'); U.clear(c); D.handshake.lines.forEach(function(s, i){ c.appendChild(U.el('div', i < 2 ? {style:'font-weight:600'} : {style:'color:var(--ink2)'}, s)); });
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['series','Low','Medium','High','Low / High'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.seeded.forEach(function(sr){ var tr = U.el('tr'); [sr.series].concat(sr.text).concat([sr.fall]).forEach(function(v){ tr.appendChild(U.el('td', null, v)); }); tb.appendChild(tr); });
  host.appendChild(tb); if(window.__fit) window.__fit();
}
window.__redraw = render; render();
