
var D = JSON.parse(document.getElementById('data').textContent);
var M = D.meta, L = M.L, NN = L*L, T = M.T, NA = M.N, K = M.K, KK = K*K, R = (K-1)/2;
var HZ = DEC.hazard(DEC.unzrle(U.b64(D.haz0), NN), U.b64(D.hazd), T, NN);
var SM = DEC.unzrle(U.b64(D.smoke), T*NN);
var WEAK = DEC.unbits(U.b64(D.weak), NN);
var COLLL = DEC.cells(U.b64(D.coll), T), SEEDL = DEC.cells(U.b64(D.seed), T), FOODL = DEC.cells(U.b64(D.foodd), T);
var COLL = new Uint8Array(T*NN), FOOD = new Uint8Array(T*NN);
(function(){ var f0 = DEC.unbits(U.b64(D.food0), NN); FOOD.set(f0, 0);
  for(var f=0; f<T; f++){ if(f>0){ COLL.copyWithin(f*NN,(f-1)*NN,f*NN); FOOD.copyWithin(f*NN,(f-1)*NN,f*NN);}
    COLLL[f].forEach(function(c){ COLL[f*NN+c]=1; }); FOODL[f].forEach(function(c){ FOOD[f*NN+c]=0; }); } })();
var SEEDT = new Int16Array(NN).fill(-1);
SEEDL.forEach(function(a, f){ a.forEach(function(c){ SEEDT[c] = f; }); });
var POS = U.b64(D.pos), ALIVE = DEC.unbits(U.b64(D.alive), T*NA);
var REV = DEC.unbits(U.b64(D.reveal), T*NA*KK), TAUQ = DEC.unzrle(U.b64(D.tau), T*NA*KK);
var EVENTS = []; for(var f=0; f<T; f++){ if(COLLL[f].length || SEEDL[f].length) EVENTS.push(f); }

var LAYERS = [
  {k:'fire', name:'fire state', on:true},
  {k:'smoke', name:'smoke density ρ (environment field)', on:true},
  {k:'weak', name:'weak floor', on:false},
  {k:'coll', name:'collapsed floor', on:true},
  {k:'seed', name:'collapse-seeded ignitions', on:true},
  {k:'food', name:'food', on:true},
  {k:'agents', name:'agents (alive, dead)', on:true}
];
var S = {t: M.t0, agent: M.agent0, playing: false, speed: 1, layers: {}};
LAYERS.forEach(function(l){ S.layers[l.k] = l.on; });
(function parseHash(){
  var h = (location.hash||'').replace(/^#/,''); if(!h) return;
  h.split('&').forEach(function(kv){ var p = kv.split('='), k = p[0], v = decodeURIComponent(p[1]||'');
    if(k==='t'){ var t = parseInt(v,10); if(t>=0 && t<T) S.t = t; }
    if(k==='agent'){ var a = parseInt(v,10); if(a>=1 && a<=NA) S.agent = a-1; if(v==='none') S.agent = -1; }
    if(k==='layers'){ var on = v.split(','); LAYERS.forEach(function(l){ S.layers[l.k] = on.indexOf(l.k)>=0; }); }
  });
})();
function writeHash(){
  try{ var on = LAYERS.filter(function(l){return S.layers[l.k];}).map(function(l){return l.k;}).join(',');
    history.replaceState(null, '', '#t='+S.t+'&agent='+(S.agent>=0?S.agent+1:'none')+'&layers='+on); }catch(e){}
}

document.getElementById('pol').textContent = M.label;
document.getElementById('sub').textContent = M.sub;

// ---------- colours (map imagery = the restyled GIFs' palette, both themes) ----------
var COL = {};
function hexRgb(h){ h = h.replace('#',''); return [parseInt(h.substr(0,2),16), parseInt(h.substr(2,2),16), parseInt(h.substr(4,2),16)]; }
function mix(a, b, u){ var x = hexRgb(a), y = hexRgb(b); return 'rgb(' + [0,1,2].map(function(i){ return Math.round(x[i]*(1-u) + y[i]*u); }).join(',') + ')'; }
function readColors(){
  ['fuel','burning','burnt','smoke_hatch','map_gridline','agent','food','map_white','map_bg','map_ink','outside','unseen','unseen_mark','map_grid','map_axis','map_A','tau_end']
    .forEach(function(k){ COL[k] = U.css(k); });
  COL.state = [COL.fuel, COL.burning, COL.burnt];
  COL.gridl = COL.state.map(function(c){ return mix(c, COL.map_gridline, 0.16); });
  COL.weakdot = [mix(COL.fuel, COL.map_ink, 0.5), mix(COL.burning, COL.map_ink, 0.5), mix(COL.burnt, COL.map_white, 0.5)];
  COL.void = [COL.map_ink, COL.map_ink, COL.map_white];
  COL.tau = function(tau){ return mix(COL.map_bg, COL.tau_end, 1 - tau); };
}

// ---------- cell painter (shared by map and the 9x9 panels) ----------
// Matches the restyled GIFs: flat hazard fill, faint cell
// gridline, smoke rho as light diagonal hatching (opacity proportional to rho,
// 16 steps), weak intact floor as a centre dot, collapsed floor as a boxed X
// keeping the hazard fill, food as an aqua square with a dark ring.
// cell: {h, rho(0..1), weak, coll, food}
function paintCell(ctx, x, y, s, c, opt){
  var h = opt.fire ? c.h : 0;
  ctx.fillStyle = opt.fire ? COL.state[h] : COL.map_bg; ctx.fillRect(x, y, s, s);
  if(s >= 5){ ctx.fillStyle = opt.fire ? COL.gridl[h] : COL.map_grid; ctx.fillRect(x + s - Math.max(1, s/8), y, Math.max(1, s/8), s); ctx.fillRect(x, y + s - Math.max(1, s/8), s, Math.max(1, s/8)); }
  if(opt.smoke && c.rho > 0){
    var lv = Math.round(c.rho * 15) / 15;
    if(lv > 0){ ctx.save(); ctx.beginPath(); ctx.rect(x, y, s - Math.max(1, s/8), s - Math.max(1, s/8)); ctx.clip();
      ctx.globalAlpha = lv * 0.9; ctx.strokeStyle = COL.smoke_hatch; ctx.lineWidth = Math.max(1, s/8);
      var stp = s/2; for(var k = -s; k <= 2*s; k += stp){ ctx.beginPath(); ctx.moveTo(x + k, y); ctx.lineTo(x + k - s, y + s); ctx.stroke(); }
      ctx.restore(); ctx.globalAlpha = 1; }
  }
  if(opt.weak && c.weak && !c.coll){ var w = Math.max(1, s/4); ctx.fillStyle = COL.weakdot[h]; ctx.fillRect(x + s*3/8, y + s*3/8, w, w); }
  if(opt.coll && c.coll){
    var q = s*7/8, lw = Math.max(1, s/8); ctx.strokeStyle = COL.void[h]; ctx.lineWidth = lw;
    ctx.strokeRect(x + lw/2, y + lw/2, q - lw, q - lw);
    ctx.beginPath(); ctx.moveTo(x + lw/2, y + lw/2); ctx.lineTo(x + q - lw/2, y + q - lw/2); ctx.moveTo(x + q - lw/2, y + lw/2); ctx.lineTo(x + lw/2, y + q - lw/2); ctx.stroke();
  }
  if(opt.food && c.food){ var e = s/8; ctx.fillStyle = COL.map_ink; ctx.fillRect(x, y, s*7/8, s*7/8); ctx.fillStyle = COL.food; ctx.fillRect(x + e, y + e, s*5/8, s*5/8); }
}
// agent sprites as in the GIFs: alive = blue disc in white and dark rings;
// dead = a hollow dark ring with white either side (radii in cells: .82/.70/.56; .82/.70/.45/.325)
function ring(ctx, cx, cy, r0, r1, col){ ctx.fillStyle = col; ctx.beginPath(); ctx.arc(cx, cy, r1, 0, 6.2832); ctx.arc(cx, cy, r0, 0, 6.2832, true); ctx.fill(); }
function drawAgentMark(ctx, cx, cy, s, alive, selected){
  if(alive){
    ctx.fillStyle = COL.map_ink; ctx.beginPath(); ctx.arc(cx, cy, 0.82*s, 0, 6.2832); ctx.fill();
    ctx.fillStyle = COL.map_white; ctx.beginPath(); ctx.arc(cx, cy, 0.70*s, 0, 6.2832); ctx.fill();
    ctx.fillStyle = COL.agent; ctx.beginPath(); ctx.arc(cx, cy, 0.56*s, 0, 6.2832); ctx.fill();
  } else {
    ring(ctx, cx, cy, 0.70*s, 0.82*s, COL.map_white); ring(ctx, cx, cy, 0.45*s, 0.70*s, COL.map_ink); ring(ctx, cx, cy, 0.325*s, 0.45*s, COL.map_white);
  }
  if(selected){ ctx.strokeStyle = COL.map_white; ctx.lineWidth = Math.max(3, s*0.4); ctx.beginPath(); ctx.arc(cx, cy, 1.25*s, 0, 6.2832); ctx.stroke();
    ctx.strokeStyle = COL.map_ink; ctx.lineWidth = Math.max(1.5, s*0.2); ctx.stroke(); }
}
function cellAt(t, i){
  return {h: HZ[t*NN+i], rho: SM[t*NN+i]/255, weak: WEAK[i], coll: COLL[t*NN+i], food: FOOD[t*NN+i]};
}
function agentPos(t, a){ var o = (t*NA + a)*2; return [POS[o], POS[o+1]]; }
function isAlive(t, a){ return ALIVE[t*NA + a] === 1; }

// ---------- map ----------
var map = document.getElementById('map'), mctx = map.getContext('2d'), MS = 8, DPR = 1;
function sizeMap(){
  DPR = window.devicePixelRatio || 1;
  var w = map.clientWidth || 480; MS = Math.max(2, Math.floor(w*DPR/L));
  map.width = MS*L; map.height = MS*L;
}
function drawMap(){
  var t = S.t, s = MS, ly = S.layers;
  mctx.fillStyle = COL.map_bg; mctx.fillRect(0,0,map.width,map.height);
  var opt = {fire: ly.fire, smoke: ly.smoke, weak: ly.weak, coll: ly.coll, food: ly.food};
  for(var i=0;i<NN;i++){ paintCell(mctx, (i%L)*s, ((i/L)|0)*s, s, cellAt(t,i), opt); }
  if(ly.seed){
    for(var c=0;c<NN;c++){ var f = SEEDT[c]; if(f>=0 && f<t){
      var cx=(c%L+0.5)*s, cy=(((c/L)|0)+0.5)*s; mctx.strokeStyle = COL.map_white; mctx.lineWidth = Math.max(2.5, s*0.32);
      mctx.beginPath(); mctx.arc(cx, cy, s*0.42, 0, 6.2832); mctx.stroke(); mctx.strokeStyle = COL.map_A; mctx.lineWidth = Math.max(1.2, s*0.16); mctx.stroke(); } }
    SEEDL[t].forEach(function(c){ var cx=(c%L+0.5)*s, cy=(((c/L)|0)+0.5)*s;
      mctx.strokeStyle = COL.map_white; mctx.lineWidth = Math.max(4, s*0.6); mctx.beginPath(); mctx.arc(cx, cy, s*1.35, 0, 6.2832); mctx.stroke();
      mctx.strokeStyle = COL.map_A; mctx.lineWidth = Math.max(2, s*0.32); mctx.stroke(); });
  }
  if(S.agent >= 0){
    var p = agentPos(t, S.agent);
    var x0 = (p[1]-R)*s, y0 = (p[0]-R)*s, w = K*s;
    mctx.strokeStyle = COL.map_white; mctx.lineWidth = Math.max(3, s*0.5); mctx.strokeRect(x0, y0, w, w);
    mctx.strokeStyle = COL.map_ink; mctx.lineWidth = Math.max(1.5, s*0.22); mctx.strokeRect(x0, y0, w, w);
  }
  if(ly.agents){
    for(var a=0;a<NA;a++){ var q = agentPos(t,a); drawAgentMark(mctx, (q[1]+0.5)*s, (q[0]+0.5)*s, s, isAlive(t,a), a===S.agent); }
  }
  mctx.strokeStyle = U.css('muted'); mctx.lineWidth = 1; mctx.strokeRect(0.5,0.5,map.width-1,map.height-1);
  map.setAttribute('aria-label', 'Episode map at t = ' + t + ' of ' + M.H + ': ' +
    LAYERS.filter(function(l){return ly[l.k];}).map(function(l){return l.name;}).join(', ') + '.');
}

// ---------- the three 9x9 panels ----------
var pobs = document.getElementById('obs'), ptru = document.getElementById('tru'), ptau = document.getElementById('tau');
function sizePanel(cv){ var w = cv.clientWidth || 160; var s = Math.max(4, Math.floor(w*DPR/K)); cv.width = s*K; cv.height = s*K; return s; }
var PS = 16;
function unseen(ctx, x, y, s){
  ctx.fillStyle = COL.unseen; ctx.fillRect(x, y, s, s);
  ctx.fillStyle = COL.unseen_mark; ctx.font = 'bold ' + Math.round(s*0.62) + 'px system-ui, sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('?', x + s/2, y + s/2 + s*0.03);
}
function drawPanels(){
  [pobs, ptru, ptau].forEach(function(cv){ PS = sizePanel(cv); });
  var octx = pobs.getContext('2d'), tctx = ptru.getContext('2d'), uctx = ptau.getContext('2d'), s = PS;
  var sel = document.getElementById('sel');
  [octx, tctx, uctx].forEach(function(c){ c.fillStyle = COL.map_bg; c.fillRect(0,0,K*s,K*s); });
  if(S.agent < 0){ sel.textContent = 'no agent selected'; return; }
  var t = S.t, a = S.agent, p = agentPos(t, a), base = (t*NA + a)*KK;
  sel.textContent = 'agent ' + (a+1) + (isAlive(t,a) ? '' : ', dead') + ' · t = ' + t;
  var occ = {}, dead = {}; for(var b=0;b<NA;b++){ var q = agentPos(t,b); if(isAlive(t,b)) occ[q[0]*L+q[1]] = 1; else dead[q[0]*L+q[1]] = 1; }
  var full = {fire:true, smoke:true, weak:true, coll:true, food:true};
  for(var dr=0; dr<K; dr++) for(var dc=0; dc<K; dc++){
    var gr = p[0]-R+dr, gc = p[1]-R+dc, inside = gr>=0 && gr<L && gc>=0 && gc<L, j = dr*K+dc, x = dc*s, y = dr*s;
    var seen = REV[base + j] === 1, tau = 1 - TAUQ[base + j]/255;
    var c = inside ? cellAt(t, gr*L+gc) : null;
    // state panel
    if(inside){ paintCell(tctx, x, y, s, c, full); if(occ[gr*L+gc]) drawAgentMark(tctx, x+s/2, y+s/2, s*0.55, true, false);
      else if(dead[gr*L+gc]) drawAgentMark(tctx, x+s/2, y+s/2, s*0.55, false, false); }
    else { tctx.fillStyle = COL.outside; tctx.fillRect(x, y, s, s); }
    // observation panel: content planes x reveal; out-of-arena cells are zero planes
    if(!seen){ unseen(octx, x, y, s); }
    else if(inside){ paintCell(octx, x, y, s, c, full); if(occ[gr*L+gc]) drawAgentMark(octx, x+s/2, y+s/2, s*0.55, true, false); }
    else { paintCell(octx, x, y, s, {h:0, rho:0, weak:0, coll:0, food:0}, full); }
    // transmittance panel
    uctx.fillStyle = COL.tau(tau); uctx.fillRect(x, y, s, s);
  }
  [octx, tctx, uctx].forEach(function(c){
    c.strokeStyle = COL.map_grid; c.lineWidth = 1;
    for(var k=1;k<K;k++){ c.beginPath(); c.moveTo(k*s+0.5,0); c.lineTo(k*s+0.5,K*s); c.moveTo(0,k*s+0.5); c.lineTo(K*s,k*s+0.5); c.stroke(); }
    c.strokeStyle = COL.map_ink; c.lineWidth = Math.max(1.5, s*0.08); c.strokeRect(R*s+1, R*s+1, s-2, s-2);
    c.strokeStyle = COL.map_axis; c.lineWidth = 1; c.strokeRect(0.5,0.5,K*s-1,K*s-1);
  });
}
function obsLegend(){
  var lg = document.getElementById('olegend'); U.clear(lg);
  function item(draw, text){ var sp = U.el('span'); var cv = U.el('canvas', {width: 28, height: 28, style:'width:14px;height:14px'}); draw(cv.getContext('2d'), 28); sp.appendChild(cv); sp.appendChild(document.createTextNode(text)); lg.appendChild(sp); }
  item(function(c,s){ unseen(c,0,0,s); }, 'unseen (masked)');
  item(function(c,s){ c.fillStyle = COL.outside; c.fillRect(0,0,s,s); c.strokeStyle=COL.map_axis; c.strokeRect(0.5,0.5,s-1,s-1); }, 'outside the arena');
  item(function(c,s){ c.fillStyle = COL.map_bg; c.fillRect(0,0,s,s); c.strokeStyle = COL.map_ink; c.lineWidth = 3; c.strokeRect(2,2,s-4,s-4); }, 'own cell');
  var sp = U.el('span'); var cv = U.el('canvas', {width: 120, height: 14, style:'width:60px;height:7px'}); var cx = cv.getContext('2d');
  for(var i=0;i<120;i++){ cx.fillStyle = COL.tau(1 - i/119); cx.fillRect(i,0,1,14); }
  sp.appendChild(document.createTextNode('τ 1')); sp.appendChild(cv); sp.appendChild(document.createTextNode('0')); lg.appendChild(sp);
}

// ---------- layer toggles (each pill carries its legend swatch) ----------
function swatch(k){
  var cv = U.el('canvas', {width: 28, height: 28, style:'width:14px;height:14px'}), c = cv.getContext('2d'), s = 28, z = {h:0,rho:0,weak:0,coll:0,food:0};
  if(k==='fire'){ c.fillStyle = COL.fuel; c.fillRect(0,0,s/3,s); c.fillStyle = COL.burning; c.fillRect(s/3,0,s/3,s); c.fillStyle = COL.burnt; c.fillRect(2*s/3,0,s/3,s); }
  if(k==='smoke'){ paintCell(c,0,0,s,{h:2,rho:1,weak:0,coll:0,food:0},{fire:true,smoke:true}); }
  if(k==='weak'){ paintCell(c,0,0,s,{h:0,rho:0,weak:1,coll:0,food:0},{fire:true,weak:true}); }
  if(k==='coll'){ paintCell(c,0,0,s,{h:0,rho:0,weak:1,coll:1,food:0},{fire:true,coll:true}); }
  if(k==='seed'){ c.fillStyle = COL.fuel; c.fillRect(0,0,s,s); c.strokeStyle = COL.map_A; c.lineWidth = 4; c.beginPath(); c.arc(s/2,s/2,s*0.34,0,6.3); c.stroke(); }
  if(k==='food'){ paintCell(c,0,0,s,{h:0,rho:0,weak:0,coll:0,food:1},{fire:true,food:true}); }
  if(k==='agents'){ c.fillStyle = COL.fuel; c.fillRect(0,0,s,s); drawAgentMark(c, s*0.28, s/2, s*0.3, true, false); drawAgentMark(c, s*0.74, s/2, s*0.3, false, false); }
  return cv;
}
var layerBox = document.getElementById('layers');
function buildLayers(){
  U.clear(layerBox);
  LAYERS.forEach(function(l){
    var b = U.el('button', {'class':'pill', 'aria-pressed': S.layers[l.k] ? 'true':'false'});
    b.appendChild(swatch(l.k)); b.appendChild(document.createTextNode(l.name));
    b.addEventListener('click', function(){ S.layers[l.k] = !S.layers[l.k]; b.setAttribute('aria-pressed', S.layers[l.k]?'true':'false'); writeHash(); drawMap(); });
    layerBox.appendChild(b);
  });
}
var agentBox = document.getElementById('agents');
for(var a=0;a<NA;a++){ (function(a){
  var b = U.el('button', {'class':'pill', 'aria-pressed':'false', 'aria-label':'agent ' + (a+1)}, String(a+1));
  b.addEventListener('click', function(){ S.agent = (S.agent===a ? -1 : a); render(); writeHash(); });
  agentBox.appendChild(b); })(a); }

// ---------- time track ----------
var track = document.getElementById('track');
function drawTrack(){
  U.clear(track); var w = track.clientWidth || 600, h = 22; track.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
  var pad = 8, X = function(t){ return pad + (w-2*pad)*t/(T-1); };
  track.appendChild(U.svg('line', {x1: pad, x2: w-pad, y1: 11, y2: 11, 'class':'ax'}));
  for(var f=0; f<T; f++){
    if(COLLL[f].length) track.appendChild(U.svg('rect', {x: X(f)-3, y: 14, width: 6, height: 6, fill: 'var(--ink)'}));
    if(SEEDL[f].length) track.appendChild(U.svg('circle', {cx: X(f), cy: 6, r: 3.6, fill:'none', stroke:'var(--A)', 'stroke-width': 2}));
  }
  track.appendChild(U.svg('line', {x1: X(S.t), x2: X(S.t), y1: 0, y2: h, stroke: 'var(--ink)', 'stroke-width': 2}));
  track.onclick = function(e){ var r = track.getBoundingClientRect(); var t = Math.round((e.clientX - r.left - pad)/(r.width-2*pad)*(T-1)); seek(Math.max(0, Math.min(T-1, t))); };
}

// ---------- playback ----------
var playBtn = document.getElementById('play'), scrub = document.getElementById('scrub'), tlab = document.getElementById('tlab');
scrub.max = T-1;
var SPEEDS = [0.5, 1, 2, 4], BASE = 16, last = null, acc = 0;
var speedBox = document.getElementById('speeds');
SPEEDS.forEach(function(v){ var b = U.el('button', {'class':'pill', 'aria-pressed': v===S.speed?'true':'false'}, v + '×');
  b.addEventListener('click', function(){ S.speed = v; Array.prototype.forEach.call(speedBox.children, function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); }); });
  speedBox.appendChild(b); });
function setPlaying(p){ S.playing = p; playBtn.setAttribute('aria-pressed', p?'true':'false'); playBtn.innerHTML = p ? '&#10074;&#10074; pause' : '&#9654; play'; last = null; acc = 0; if(p) requestAnimationFrame(loop); }
function loop(ts){
  if(!S.playing) return;
  if(last === null) last = ts; var dt = ts - last; last = ts; acc += dt * BASE * S.speed / 1000;
  var adv = Math.floor(acc); if(adv > 0){ acc -= adv; var t = S.t + adv; if(t >= T-1){ t = T-1; S.t = t; render(); setPlaying(false); return; } S.t = t; render(); }
  requestAnimationFrame(loop);
}
function seek(t){ S.t = Math.max(0, Math.min(T-1, t)); render(); writeHash(); }
playBtn.addEventListener('click', function(){ if(!S.playing && S.t >= T-1) S.t = 0; setPlaying(!S.playing); });
document.getElementById('back').addEventListener('click', function(){ setPlaying(false); seek(S.t-1); });
document.getElementById('fwd').addEventListener('click', function(){ setPlaying(false); seek(S.t+1); });
scrub.addEventListener('input', function(){ setPlaying(false); seek(parseInt(scrub.value,10)); });
function jumpEvent(dir){ setPlaying(false); var cand = EVENTS.filter(function(f){ return dir>0 ? f > S.t : f < S.t; }); if(cand.length) seek(dir>0 ? cand[0] : cand[cand.length-1]); }
document.getElementById('evprev').addEventListener('click', function(){ jumpEvent(-1); });
document.getElementById('evnext').addEventListener('click', function(){ jumpEvent(1); });
document.addEventListener('keydown', function(e){
  var tag = (e.target && e.target.tagName) || '';
  if(e.key === ' ' && tag !== 'BUTTON' && tag !== 'INPUT'){ e.preventDefault(); if(!S.playing && S.t >= T-1) S.t = 0; setPlaying(!S.playing); return; }
  if(tag === 'INPUT') return;
  if(e.key === 'ArrowRight'){ e.preventDefault(); setPlaying(false); seek(S.t + (e.shiftKey?10:1)); }
  else if(e.key === 'ArrowLeft'){ e.preventDefault(); setPlaying(false); seek(S.t - (e.shiftKey?10:1)); }
  else if(e.key === 'Home'){ e.preventDefault(); seek(0); }
  else if(e.key === 'End'){ e.preventDefault(); seek(T-1); }
  else if(e.key === ']'){ jumpEvent(1); } else if(e.key === '['){ jumpEvent(-1); }
  else if(/^[1-9]$/.test(e.key)){ var a = parseInt(e.key,10)-1; if(a < NA){ S.agent = a; render(); writeHash(); } }
});

// ---------- map hover / click ----------
function cellFromEvent(e){ var r = map.getBoundingClientRect(); var c = Math.floor((e.clientX - r.left)/r.width*L), rr = Math.floor((e.clientY - r.top)/r.height*L); return [rr, c]; }
var HSTATE = ['fuel', 'burning', 'burnt'];
map.addEventListener('mousemove', function(e){
  var rc = cellFromEvent(e); if(rc[0]<0||rc[0]>=L||rc[1]<0||rc[1]>=L){ U.tip.hide(); return; }
  var i = rc[0]*L+rc[1], c = cellAt(S.t, i), lines = [['cell', '(' + rc[0] + ', ' + rc[1] + ') · t = ' + S.t]];
  lines.push('fire state: ' + HSTATE[c.h]);
  if(c.rho > 0) lines.push('smoke density ρ ≈ ' + c.rho.toFixed(2) + ' (environment field)');
  if(c.coll) lines.push('collapsed floor'); else if(c.weak) lines.push('weak floor, intact');
  if(c.food) lines.push('food');
  if(SEEDT[i] >= 0 && SEEDT[i] <= S.t) lines.push('collapse-seeded ignition at t = ' + SEEDT[i]);
  for(var a=0;a<NA;a++){ var p = agentPos(S.t,a); if(p[0]===rc[0] && p[1]===rc[1]) lines.push('agent ' + (a+1) + (isAlive(S.t,a)?'':', dead')); }
  U.tip.show(lines, e.clientX, e.clientY);
});
map.addEventListener('mouseleave', function(){ U.tip.hide(); });
map.addEventListener('click', function(e){
  var rc = cellFromEvent(e), best = -1, bd = 2.3;
  for(var a=0;a<NA;a++){ var p = agentPos(S.t,a), d = Math.hypot(p[0]-rc[0], p[1]-rc[1]); if(d < bd){ bd = d; best = a; } }
  if(best >= 0){ S.agent = best; render(); writeHash(); }
});
function panelHover(cv, which){
  cv.addEventListener('mousemove', function(e){
    if(S.agent < 0) return; var r = cv.getBoundingClientRect(); var dc = Math.floor((e.clientX-r.left)/r.width*K), dr = Math.floor((e.clientY-r.top)/r.height*K);
    if(dr<0||dr>=K||dc<0||dc>=K){ U.tip.hide(); return; }
    var p = agentPos(S.t, S.agent), j = (S.t*NA+S.agent)*KK + dr*K+dc, gr = p[0]-R+dr, gc = p[1]-R+dc;
    var inside = gr>=0&&gr<L&&gc>=0&&gc<L, seen = REV[j]===1, tau = 1-TAUQ[j]/255;
    var lines = [['offset', '(' + (dr-R) + ', ' + (dc-R) + ')' + (inside ? ' · cell (' + gr + ', ' + gc + ')' : ' · outside the arena')]];
    lines.push('P(seen) = τ ≈ ' + tau.toFixed(2) + ' · ' + (seen ? 'seen' : 'unseen (masked)'));
    if(inside){ var c = cellAt(S.t, gr*L+gc); lines.push('state: ' + HSTATE[c.h] + (c.rho>0 ? ', ρ ≈ ' + c.rho.toFixed(2) : '')); }
    U.tip.show(lines, e.clientX, e.clientY);
  });
  cv.addEventListener('mouseleave', function(){ U.tip.hide(); });
}
[pobs, ptru, ptau].forEach(panelHover);

// ---------- render ----------
function render(){
  scrub.value = S.t; tlab.textContent = 't = ' + S.t + ' / ' + M.H;
  drawMap(); drawPanels(); drawTrack();
  Array.prototype.forEach.call(agentBox.children, function(b, i){ b.setAttribute('aria-pressed', i===S.agent?'true':'false'); });
}
function full(){ readColors(); sizeMap(); buildLayers(); obsLegend(); render(); if(window.__fit) window.__fit(); }
window.__redraw = full;
var rt = null; window.addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(full, 80); });
window.addEventListener('beforeprint', full);
full();
