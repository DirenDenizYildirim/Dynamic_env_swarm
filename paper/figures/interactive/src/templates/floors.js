
var D = JSON.parse(document.getElementById('data').textContent);
var TABS = [{k:'card', t:'per card (and tree, and config)'}, {k:'artifact', t:'per artifact'}, {k:'length', t:'per run length'}, {k:'beat', t:'the grid against its floor'}];
var S = {tab: 'card'};
(function(){ var h=(location.hash||'').replace('#',''); TABS.forEach(function(x){ if(h==='tab='+x.k) S.tab=x.k; }); })();
var tabs = document.getElementById('tabs');
TABS.forEach(function(x){ var b = U.el('button', {'class':'pill', role:'tab', 'aria-selected':'false', 'aria-pressed':'false'}, x.t);
  b.onclick = function(){ S.tab = x.k; render(); }; tabs.appendChild(b); });
function txt(svg, x, y, s, o){ var a = {x:x, y:y, 'font-size':11.5}; for(var k in (o||{})) a[k]=o[k]; svg.appendChild(U.svg('text', a, s)); }
function hover(g, lines){ g.setAttribute('tabindex', 0);
  g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); }); g.addEventListener('mouseleave', function(){ U.tip.hide(); });
  g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); }); }
function card(){
  var d = D.card, W = 620, H = 220, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'Medium reproducibility floors on two runs'});
  var x0 = 170, x1 = 560, X = function(v){ return x0 + v/0.045*(x1-x0); };
  [0,0.01,0.02,0.03,0.04].forEach(function(v){ svg.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:18, y2:H-34, 'class':'gl'})); txt(svg, X(v), H-18, v.toFixed(2), {'text-anchor':'middle', 'class':'tick'}); });
  txt(svg, (x0+x1)/2, H-2, 'rerun floor: sd over identical runs', {'text-anchor':'middle', style:'fill:var(--ink2)', 'font-size':11});
  [['completion','completion','ct'],['survival','survival rate','st']].forEach(function(m, i){
    var y = 30 + i*86; txt(svg, 6, y+4, m[1], {'font-weight':600});
    d.runs.forEach(function(r, j){ var yy = y + 16 + j*26, v = r[m[0]], g = U.svg('g');
      g.appendChild(U.svg('text', {x:6, y:yy+5, 'font-size':11, style:'fill:var(--ink2)'}, r.name));
      g.appendChild(U.svg('rect', {x:x0, y:yy-7, width:X(v)-x0, height:14, rx:3, fill: j ? 'var(--ink)' : 'var(--muted)'}));
      g.appendChild(U.svg('text', {x:X(v)+6, y:yy+5, 'font-size':11.5, 'font-weight':600, 'class':'num'}, r[m[2]]));
      hover(g, [[r.name, '· ' + m[1]], ['floor (sd)', r[m[2]]], 'identical runs, same seed']); svg.appendChild(g); });
    if(i===0) txt(svg, X(0.0399)+52, y+33, d.ratio, {'font-size':11, style:'fill:var(--ink2)'});
  });
  return svg;
}
function artifact(){
  var d = D.artifact, W = 620, H = 170, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'per-artifact rerun comparisons'});
  txt(svg, 190, 16, 'each square: one rerun comparison · filled: field digests differed', {'font-size':10.5, style:'fill:var(--muted)'});
  d.rows.forEach(function(r, i){ var y = 44 + i*42, g = U.svg('g');
    g.appendChild(U.svg('text', {x:6, y:y+5, 'font-size':12, 'font-weight':600}, r.name));
    for(var k=0;k<r.n;k++){ g.appendChild(U.svg('rect', {x:190+k*26, y:y-10, width:20, height:20, rx:3, fill: k < r.diff ? 'var(--ink)' : 'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.3})); }
    if(r.text) g.appendChild(U.svg('text', {x:190+5*26+12, y:y+5, 'font-size':11, style:'fill:var(--ink2)'}, r.text));
    hover(g, r.text ? [[r.name, ''], r.text] : [[r.name, '']]); svg.appendChild(g); });
  return svg;
}
function length(){
  var d = D.length, W = 620, H = 250, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'completion floor reps at two run lengths'});
  var all = []; d.arms.forEach(function(a){ all = all.concat(a.v500, a.v1000); });
  var lo = Math.min.apply(null, all) - 0.01, hi = Math.max.apply(null, all) + 0.01, y0 = 20, y1 = H-40;
  var Y = function(v){ return y1 - (v-lo)/(hi-lo)*(y1-y0); };
  txt(svg, 6, y0+6, 'completion,', {'font-size':10.5, style:'fill:var(--muted)'}); txt(svg, 6, y0+19, 'one dot per run', {'font-size':10.5, style:'fill:var(--muted)'});
  for(var v = Math.ceil(lo*50)/50; v <= hi; v += 0.02){ svg.appendChild(U.svg('line', {x1:130, x2:W-20, y1:Y(v), y2:Y(v), 'class':'gl'})); txt(svg, 124, Y(v)+4, v.toFixed(2), {'text-anchor':'end', 'class':'tick'}); }
  d.arms.forEach(function(a, i){ var xb = 170 + i*230;
    txt(svg, xb+60, H-6, a.name + ' · floor growth ' + a.g, {'text-anchor':'middle', 'font-weight':600});
    [['T = 500', a.v500, 0], ['T = 1000', a.v1000, 1]].forEach(function(s){ var x = xb + s[2]*120, g = U.svg('g');
      txt(svg, x, H-24, s[0], {'text-anchor':'middle', 'class':'tick'});
      var mean = s[1].reduce(function(p,c){return p+c;},0)/s[1].length;
      s[1].slice().sort(function(p,q){return p-q;}).forEach(function(v, k){ g.appendChild(U.svg('circle', {cx:x + ((k%2)?6:-6), cy:Y(v), r:3.6, fill: s[2] ? 'var(--ink)' : 'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.3})); });
      g.appendChild(U.svg('line', {x1:x-18, x2:x+18, y1:Y(mean), y2:Y(mean), stroke:'var(--muted)', 'stroke-width':1.5}));
      hover(g, [[a.name + ', ' + s[0], ''], 'identical runs, same seed', 'grey tick: their mean']); svg.appendChild(g); });
  });
  return svg;
}
function beat(){
  var d = D.beat, W = 620, H = 210, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'seed dispersion over the rerun floor'});
  var x0 = 170, x1 = 560, X = function(v){ return x0 + v/6*(x1-x0); };
  [0,1,2,3,4,5,6].forEach(function(v){ svg.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:10, y2:H-34, 'class': v===1 ? 'zero' : 'gl'})); txt(svg, X(v), H-18, v + '×', {'text-anchor':'middle', 'class':'tick'}); });
  txt(svg, X(1)+4, 16, '1× = the floor', {'font-size':10.5, style:'fill:var(--muted)'});
  d.rows.concat([{name:'survival Γ / floor-basis sd(Γ)', v:d.gamma.v, t:d.gamma.t, g:1}]).forEach(function(r, i){ var y = 34 + i*30 + (r.g ? 10 : 0), g = U.svg('g');
    g.appendChild(U.svg('text', {x:6, y:y+4, 'font-size':11, style:'fill:var(--ink2)'}, r.name));
    g.appendChild(U.svg('rect', {x:x0, y:y-7, width:X(r.v)-x0, height:14, rx:3, fill: r.g ? 'var(--ink)' : 'var(--muted)'}));
    g.appendChild(U.svg('text', {x:X(r.v)+6, y:y+4, 'font-size':11.5, 'font-weight':600, 'class':'num'}, r.t));
    hover(g, [[r.name, r.t]]); svg.appendChild(g); });
  return svg;
}
function render(){
  Array.prototype.forEach.call(tabs.children, function(b, i){ var on = TABS[i].k===S.tab; b.setAttribute('aria-selected', on?'true':'false'); b.setAttribute('aria-pressed', on?'true':'false'); });
  var host = document.getElementById('panel'); U.clear(host); var d = D[S.tab];
  host.appendChild({card:card, artifact:artifact, length:length, beat:beat}[S.tab]());
  document.getElementById('sub').textContent = d.sub;
  var cf = document.getElementById('conf'); cf.textContent = d.confound ? 'confound: ' + d.confound : ''; cf.style.display = d.confound ? '' : 'none';
  U.tip.hide(); if(window.__fit) window.__fit();
}
document.addEventListener('keydown', function(e){ var i = TABS.findIndex(function(x){return x.k===S.tab;});
  if(e.key==='ArrowRight'){ S.tab = TABS[Math.min(3,i+1)].k; render(); } if(e.key==='ArrowLeft'){ S.tab = TABS[Math.max(0,i-1)].k; render(); } });
window.__redraw = render; render();
