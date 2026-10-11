
var D = JSON.parse(document.getElementById('data').textContent);
var L = D.L, NN = L*L, T = D.T, S = {t: 128, playing:false, sel: 1};
var P = D.panels.map(function(p){ return {name:p.name, beta:p.beta,
  HZ: DEC.hazard(DEC.unzrle(U.b64(p.haz0), NN), U.b64(p.hazd), T, NN), SM: DEC.unzrle(U.b64(p.smoke), T*NN)}; });
var COL = {};
function mix(a, b, u){ function h(x){ x=x.replace('#',''); return [0,2,4].map(function(i){return parseInt(x.substr(i,2),16);}); } var x=h(a), y=h(b); return 'rgb('+[0,1,2].map(function(i){return Math.round(x[i]*(1-u)+y[i]*u);}).join(',')+')'; }
function readColors(){ ['fuel','burning','burnt','smoke_hatch','map_gridline','map_bg','map_ink'].forEach(function(k){ COL[k]=U.css(k); });
  COL.state=[COL.fuel,COL.burning,COL.burnt]; COL.gridl = COL.state.map(function(c){ return mix(c, COL.map_gridline, 0.16); }); }
var cvs = [], trio = document.getElementById('trio');
D.levels.forEach(function(lv, i){ var f = U.el('figure'), c = U.el('canvas', {role:'img', 'aria-label': lv.name + ' severity fire state', tabindex:0});
  f.appendChild(c); f.appendChild(U.el('figcaption', null, lv.name + ' · β ' + lv.beta.toFixed(2) + ' · ' + lv.txt + ' (no agents)'));
  c.addEventListener('click', function(){ S.sel = i; render(); }); c.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); S.sel=i; render(); } });
  trio.appendChild(f); cvs.push(c); });
function drawPanel(i){
  var c = cvs[i], dpr = window.devicePixelRatio||1, s = Math.max(2, Math.floor((c.clientWidth||200)*dpr/L)); c.width = c.height = s*L;
  var x = c.getContext('2d'), p = P[i], t = S.t, g = Math.max(1, Math.round(s/8));
  for(var k=0;k<NN;k++){ var h = p.HZ[t*NN+k], cx = (k%L)*s, cy = ((k/L)|0)*s; x.fillStyle = COL.state[h]; x.fillRect(cx, cy, s, s);
    if(s >= 4){ x.fillStyle = COL.gridl[h]; x.fillRect(cx+s-g, cy, g, s); x.fillRect(cx, cy+s-g, s, g); }
    var r = p.SM[t*NN+k]; if(r > 0){ var lv = Math.round(r/255*15)/15; if(lv>0){ x.save(); x.beginPath(); x.rect(cx, cy, s-g, s-g); x.clip(); x.globalAlpha = lv*0.9; x.strokeStyle = COL.smoke_hatch; x.lineWidth = g;
      for(var q=-s;q<=2*s;q+=s/2){ x.beginPath(); x.moveTo(cx+q, cy); x.lineTo(cx+q-s, cy+s); x.stroke(); } x.restore(); x.globalAlpha=1; } } }
  c.parentNode.className = (i===S.sel) ? 'on' : '';
}
function chart(){
  var W = 420, H = 300, l = 48, r = 12, t = 14, b = 40, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'P_span against beta'});
  var X = function(v){ return l + (v-0.3)/(0.8-0.3)*(W-l-r); }, Y = function(v){ return t + (1-v)*(H-t-b); };
  [0,0.25,0.5,0.75,1].forEach(function(v){ svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:Y(v), y2:Y(v), 'class':'gl'})); svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, String(v))); });
  [0.3,0.4,0.5,0.6,0.7,0.8].forEach(function(v){ svg.appendChild(U.svg('text', {x:X(v), y:H-b+15, 'text-anchor':'middle', 'class':'tick'}, v.toFixed(1))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-6, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, 'β, per-neighbour ignition probability'));
  // locked levels
  D.levels.forEach(function(lv, i){ var x = X(lv.beta), on = i===S.sel;
    svg.appendChild(U.svg('line', {x1:x, x2:x, y1:t, y2:H-b, stroke:'var(--ink)', 'stroke-width': on ? 2 : 1}));
    svg.appendChild(U.svg('text', {x:x + (i===0 ? -4 : 4), y: i===1 ? H-b-8 : t+10, 'text-anchor': i===0 ? 'end' : 'start', 'font-size':10.5, 'font-weight': on ? 700 : 400, style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, lv.name + ' ' + lv.beta.toFixed(2))); });
  var styles = [{dash:null, mk:'circle'}, {dash:null, mk:'square'}, {dash:null, mk:'tri'}];
  var shades = ['var(--muted)', 'var(--ink2)', 'var(--ink)'];
  D.curves.forEach(function(cv, j){
    var pts = D.betas.map(function(bb, i){ return [bb, cv.p[i], cv.se[i]]; }).filter(function(q){ return q[0]>=0.3 && q[0]<=0.8; }).sort(function(a,b){return a[0]-b[0];});
    svg.appendChild(U.svg('path', {d: pts.map(function(q,i){ return (i?'L':'M') + X(q[0]) + ',' + Y(q[1]); }).join(''), fill:'none', stroke:shades[j], 'stroke-width':1.6}));
    pts.forEach(function(q){ var x = X(q[0]), y = Y(q[1]);
      if(q[2] > 0) svg.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(q[1]-q[2]), y2:Y(q[1]+q[2]), stroke:shades[j], 'stroke-width':1}));
      if(j===0) svg.appendChild(U.svg('circle', {cx:x, cy:y, r:2.4, fill:'var(--surface)', stroke:shades[j], 'stroke-width':1.2}));
      if(j===1) svg.appendChild(U.svg('rect', {x:x-2.2, y:y-2.2, width:4.4, height:4.4, fill:shades[j]}));
      if(j===2) svg.appendChild(U.svg('path', {d:'M'+x+','+(y-3)+'L'+(x+2.8)+','+(y+2)+'L'+(x-2.8)+','+(y+2)+'Z', fill:shades[j]})); });
  });
  var lg = U.svg('g'); [['L = 32','circle'],['L = 48','square'],['L = 64','tri']].forEach(function(e, j){ var y = H-b-56+j*16, x = X(0.58);
    lg.appendChild(U.svg('line', {x1:x, x2:x+18, y1:y, y2:y, stroke:shades[j], 'stroke-width':1.6})); lg.appendChild(U.svg('text', {x:x+24, y:y+4, 'font-size':11}, e[0])); }); svg.appendChild(lg);
  var xc = X(parseFloat(D.betac64)); svg.appendChild(U.svg('path', {d:'M'+xc+','+(H-b+1)+'l-4,7h8z', fill:'var(--ink)'}));
  svg.appendChild(U.svg('text', {x:X(0.535), y:H-b-74, 'font-size':9.5, style:'fill:var(--ink2)'}, '▲ β_c(64) ≈ ' + D.betac64 + ' (P_span = ½, L = 64)'));
  svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:Y(0.5), y2:Y(0.5), stroke:'var(--muted)', 'stroke-width':0.8}));
  return svg;
}
function table(){ var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['level','β','calibration at L = 64 (centre ignition, no agents)'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.levels.forEach(function(lv){ var tr = U.el('tr'); [lv.name, lv.beta.toFixed(2), lv.txt].forEach(function(c){ tr.appendChild(U.el('td', null, c)); }); tb.appendChild(tr); }); host.appendChild(tb); }
var scrub = document.getElementById('scrub'), playBtn = document.getElementById('play'), last = null, acc = 0; scrub.max = T-1;
function render(){ scrub.value = S.t; document.getElementById('tlab').textContent = 't = ' + S.t + ' / ' + (T-1);
  for(var i=0;i<3;i++) drawPanel(i); var ch = document.getElementById('chart'); U.clear(ch); ch.appendChild(chart()); }
function setPlaying(p){ S.playing = p; playBtn.setAttribute('aria-pressed', p?'true':'false'); playBtn.innerHTML = p ? '&#10074;&#10074; pause' : '&#9654; play'; last = null; acc = 0; if(p) requestAnimationFrame(loop); }
function loop(ts){ if(!S.playing) return; if(last===null) last = ts; acc += (ts-last)*16/1000; last = ts; var a = Math.floor(acc);
  if(a>0){ acc -= a; S.t = Math.min(T-1, S.t + a); render(); if(S.t >= T-1){ setPlaying(false); return; } } requestAnimationFrame(loop); }
playBtn.onclick = function(){ if(!S.playing && S.t >= T-1) S.t = 0; setPlaying(!S.playing); };
scrub.oninput = function(){ setPlaying(false); S.t = parseInt(scrub.value,10); render(); };
document.addEventListener('keydown', function(e){ var tg = (e.target&&e.target.tagName)||''; if(tg==='INPUT') return;
  if(e.key===' ' && tg!=='BUTTON'){ e.preventDefault(); playBtn.onclick(); }
  if(e.key==='ArrowRight'){ setPlaying(false); S.t = Math.min(T-1, S.t + (e.shiftKey?10:1)); render(); }
  if(e.key==='ArrowLeft'){ setPlaying(false); S.t = Math.max(0, S.t - (e.shiftKey?10:1)); render(); } });
function legend(){ var lg = document.getElementById('lg'); U.clear(lg);
  [['fuel', 0], ['burning', 1], ['burnt', 2]].forEach(function(e){ var sp = U.el('span', {style:'display:inline-flex;gap:5px;align-items:center'}), c = U.el('canvas', {width:24, height:24, style:'width:12px;height:12px'}), x = c.getContext('2d');
    x.fillStyle = COL.state[e[1]]; x.fillRect(0,0,24,24); sp.appendChild(c); sp.appendChild(document.createTextNode(e[0])); lg.appendChild(sp); });
  lg.appendChild(U.el('span', null, 'light hatching: smoke density ρ (environment field)')); }
window.__redraw = function(){ readColors(); legend(); render(); };
window.addEventListener('resize', function(){ render(); });
readColors(); legend(); table(); render();
