
var D = JSON.parse(document.getElementById('data').textContent);
var S = {view:'beh', sev:false};
var TYPES = [
  {k:'A', name:'Coupling A only'}, {k:'B', name:'Coupling B only'}, {k:'AB', name:'A + B together'},
  {k:'F', name:'fire-only (δ-only; no active stressor)'}, {k:'D', name:'δ only (comms denied)'}
];
function fr(s){ var p = s.split('/'); return p.length>1 ? parseInt(p[0],10)/parseInt(p[1],10) : parseFloat(s); }
function fill(defs, k){
  var id = 'pt' + k;
  if(!defs.querySelector('#'+id)){
    var p = U.svg('pattern', {id:id, width:7, height:7, patternUnits:'userSpaceOnUse'});
    var base = k==='A' ? 'var(--A)' : k==='B' ? 'var(--B)' : k==='AB' ? 'var(--A)' : 'var(--fireonly)';
    p.appendChild(U.svg('rect', {width:7, height:7, fill:base, 'fill-opacity': k==='F'||k==='D' ? 1 : 0.30}));
    if(k==='A' || k==='AB') p.appendChild(U.svg('path', {d:'M-1,8 L8,-1 M-1,1 L1,-1 M6,8 L8,6', stroke:'var(--A)', 'stroke-width':1.6}));
    if(k==='B' || k==='AB') p.appendChild(U.svg('path', {d:'M-1,-1 L8,8 M6,-1 L8,1 M-1,6 L1,8', stroke:'var(--B)', 'stroke-width':1.6}));
    if(k==='D') p.appendChild(U.svg('circle', {cx:3.5, cy:3.5, r:1.1, fill:'var(--ink2)'}));
    defs.appendChild(p);
  }
  return 'url(#' + id + ')';
}
function typOf(c){ var beh = S.view==='beh';
  if(c.A && c.B) return 'AB'; if(c.A) return 'A'; if(c.B) return 'B'; return beh ? 'F' : 'D'; }
function segs(arm){
  // ordered segments; with severity split, one per (type, beta)
  var order = ['A','B','AB','F','D'], out = [];
  order.forEach(function(t){
    var cs = arm.components.filter(function(c){ return typOf(c)===t; });
    if(!cs.length) return;
    if(S.sev){ cs.slice().sort(function(a,b){return a.beta-b.beta;}).forEach(function(c){ out.push({t:t, w:c.wf, comps:[c], beta:c.beta}); }); }
    else out.push({t:t, w:cs.reduce(function(a,c){return a+c.wf;},0), comps:cs});
  });
  return out;
}
function fracText(w){ var dens=[1,2,3,4,6,12]; for(var i=0;i<dens.length;i++){ var n=Math.round(w*dens[i]); if(Math.abs(n/dens[i]-w)<1e-9) return dens[i]===1 ? String(n) : n+'/'+dens[i]; } return w.toFixed(3); }
function bar(arm){
  var W = 520, H = 46, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': arm.name + ' training mixture'}), defs = U.svg('defs'); svg.appendChild(defs);
  var x = 0, gap = 2;
  segs(arm).forEach(function(sg){
    var w = sg.w * W, label = TYPES.filter(function(t){return t.k===sg.t;})[0].name;
    if(S.view==='nom' && sg.t==='AB' && sg.comps.every(function(c){return c.D;})) label = 'A + B + δ together';
    var g = U.svg('g', {tabindex:0});
    g.appendChild(U.svg('rect', {x:x + (x>0?gap/2:0), y:0, width:Math.max(0, w - (x>0?gap/2:0) - (x+w<W-0.5?gap/2:0)), height:30, rx:3, fill:fill(defs, sg.t)}));
    var txt = fracText(sg.w) + (S.sev ? ' · β ' + sg.beta.toFixed(2) : '');
    if(w > txt.length*7 + 10){ var t = U.svg('text', {x:x + w/2, y:20, 'text-anchor':'middle', 'font-size':12, 'font-weight':600,
      style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, txt); g.appendChild(t); }
    var lines = [[arm.name, '· ' + label], ['share', fracText(sg.w)]];
    sg.comps.forEach(function(c){ lines.push(c.name + ': β ' + c.beta.toFixed(2) + ', κ_A ' + c.kA + ', κ_B ' + c.kB + ', δ ' + c.d + ', weight ' + c.w); });
    g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
    g.addEventListener('mouseleave', function(){ U.tip.hide(); });
    g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
    svg.appendChild(g); x += w;
  });
  // tick marks at thirds and halves (axis 0..1)
  [0, 1/3, 1/2, 2/3, 1].forEach(function(v){ svg.appendChild(U.svg('line', {x1:v*W, x2:v*W, y1:33, y2:37, 'class':'ax'})); });
  ['0','1/3','1/2','2/3','1'].forEach(function(s, i){ var v=[0,1/3,1/2,2/3,1][i]; svg.appendChild(U.svg('text', {x:Math.min(W-6, Math.max(6, v*W)), y:46, 'text-anchor':'middle', 'class':'tick'}, s)); });
  return svg;
}
function meters(arm){
  var v = arm[S.view], W = 230, H = 60, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': arm.name + ' per-stressor marginals and active share'}), defs = U.svg('defs'); svg.appendChild(defs);
  var rows = [{lab:'A', v:fr(v.mA), t:v.mA, f:fill(defs,'A')}, {lab:'B', v:fr(v.mB), t:v.mB, f:fill(defs,'B')}, {lab:'active', v:fr(v.active), t:v.active, f:'var(--ink)'}];
  var x0 = 46, x1 = 196;
  rows.forEach(function(r, i){ var y = 4 + i*19;
    svg.appendChild(U.svg('text', {x:0, y:y+10, 'font-size':11, style:'fill:var(--ink2)'}, r.lab));
    svg.appendChild(U.svg('rect', {x:x0, y:y, width:x1-x0, height:12, rx:2, fill:'var(--band)'}));
    if(r.v>0) svg.appendChild(U.svg('rect', {x:x0, y:y, width:(x1-x0)*r.v, height:12, rx:2, fill:r.f}));
    svg.appendChild(U.svg('text', {x:x1+6, y:y+10, 'font-size':11.5, 'font-weight':600, 'class':'num'}, r.t));
  });
  return svg;
}
function render(){
  document.getElementById('vbeh').setAttribute('aria-pressed', S.view==='beh'?'true':'false');
  document.getElementById('vnom').setAttribute('aria-pressed', S.view==='nom'?'true':'false');
  document.getElementById('vsev').setAttribute('aria-pressed', S.sev?'true':'false');
  var g = document.getElementById('grid'); U.clear(g);
  g.appendChild(U.el('div')); g.appendChild(U.el('div', {'class':'hd'}, 'share of training episodes, by episode type'));
  g.appendChild(U.el('div', {'class':'hd hdm'}, 'per-stressor marginal, and the share with an active stressor'));
  D.arms.forEach(function(arm){
    g.appendChild(U.el('div', {'class':'arm'}, arm.name));
    var b = U.el('div'); b.appendChild(bar(arm)); g.appendChild(b);
    var m = U.el('div', {'class':'meters'}); m.appendChild(meters(arm));
    if(arm.name==='JOINT') m.appendChild(U.el('div', {'class':'hd'}, 'per-stressor marginal: ' + D.ratios.JOINT));
    g.appendChild(m);
  });
  var lg = document.getElementById('legend'); U.clear(lg);
  TYPES.filter(function(t){ return S.view==='beh' ? t.k!=='D' : t.k!=='F'; }).forEach(function(t){
    var sp = U.el('span'), s = U.svg('svg', {width:18, height:12}), d = U.svg('defs'); s.appendChild(d);
    s.appendChild(U.svg('rect', {width:18, height:12, rx:2, fill:fill(d, t.k)})); sp.appendChild(s); sp.appendChild(document.createTextNode(t.name)); lg.appendChild(sp); });
  document.getElementById('note').textContent = S.view==='beh'
    ? 'δ inert under a frozen random-projection encoder at this scale · the fire burns in every episode'
    : 'nominal: δ counted, as the configs’ headers count it · the fire burns in every episode';
  table(); if(window.__fit) window.__fit();
}
function table(){
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['arm','component','β','κ_A','κ_B','δ','weight'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.arms.forEach(function(arm){ arm.components.forEach(function(c){ var tr = U.el('tr');
    [arm.name, c.name, c.beta.toFixed(2), c.kA, c.kB, c.d, c.w].forEach(function(v){ tr.appendChild(U.el('td', null, String(v))); }); tb.appendChild(tr); }); });
  host.appendChild(tb);
}
document.getElementById('vbeh').onclick = function(){ S.view='beh'; render(); };
document.getElementById('vnom').onclick = function(){ S.view='nom'; render(); };
document.getElementById('vsev').onclick = function(){ S.sev=!S.sev; render(); };
window.__redraw = render;
render();
