var D = JSON.parse(document.getElementById('data').textContent);
function marker(svg, shape, x, y){
  if(shape==='dot') svg.appendChild(U.svg('circle', {cx:x, cy:y, r:4.6, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':2}));
  if(shape==='tri') svg.appendChild(U.svg('path', {d:'M'+x+','+(y-5.6)+'L'+(x+5.2)+','+(y+3.6)+'L'+(x-5.2)+','+(y+3.6)+'Z', fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
}
function whisker(mt, d, shape){
  var W = 240, H = 22, X = function(v){ return 8 + (v - mt.dom[0])/(mt.dom[1]-mt.dom[0])*(W-16); };
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'estimate and Šidák 95 % interval'});
  svg.appendChild(U.svg('line', {x1:X(0), x2:X(0), y1:0, y2:H, 'class':'zero'}));
  svg.appendChild(U.svg('line', {x1:X(d.lo), x2:X(d.hi), y1:H/2, y2:H/2, stroke:'var(--ink)', 'stroke-width':2}));
  [d.lo, d.hi].forEach(function(v){ svg.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:H/2-5, y2:H/2+5, stroke:'var(--ink)', 'stroke-width':2})); });
  marker(svg, shape, X(d.gamma), H/2);
  return svg;
}
function axis(mt){
  var W = 240, H = 26, X = function(v){ return 8 + (v - mt.dom[0])/(mt.dom[1]-mt.dom[0])*(W-16); };
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, 'aria-hidden':'true'});
  svg.appendChild(U.svg('line', {x1:8, x2:W-8, y1:2, y2:2, 'class':'ax'}));
  mt.ticks.forEach(function(v){ svg.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:2, y2:6, 'class':'ax'}));
    svg.appendChild(U.svg('text', {x:X(v), y:17, 'text-anchor':'middle', 'class':'tick'}, Math.abs(v)<1e-12 ? '0' : (v>0?'+':'−') + Math.abs(v).toFixed(mt.dp))); });
  return svg;
}
function chip(text, kind){ return U.el('span', {'class':'chip ' + kind}, text); }
function render(){
  var host = document.getElementById('blocks'); U.clear(host);
  D.metrics.forEach(function(mt){
    var blk = U.el('section', {'class':'blk'}); blk.appendChild(U.el('h3', null, mt.name));
    D.rows.forEach(function(r){
      var d = r.m[mt.k], row = U.el('div', {'class':'r'});
      var id = U.el('div', {'class':'id'}); var b = U.el('b', null, r.sym); id.appendChild(b); id.appendChild(document.createTextNode('  ' + r.contrast));
      id.appendChild(U.el('span', {'class':'m'}, r.meta)); row.appendChild(id);
      var vt = U.el('div', {'class':'vt'});
      vt.appendChild(chip(d.reject ? 'REJECT' : 'null', d.reject ? 'fill' : 'line'));
      vt.appendChild(U.el('span', {'class':'num'}, d.est + (d.ci ? ' ' + d.ci : '')));
      if(r.id==='G4'){ var c = D.consequence[mt.k]; vt.appendChild(chip(c.text, c.kind)); }
      row.appendChild(vt);
      var wk = U.el('div', {'class':'wk'}); wk.appendChild(whisker(mt, d, r.shape)); row.appendChild(wk);
      blk.appendChild(row);
    });
    var ax = U.el('div', {'class':'r ax'}); ax.appendChild(U.el('div', {'class':'id'})); ax.appendChild(U.el('div', {'class':'vt'}));
    var wk = U.el('div', {'class':'wk'}); wk.appendChild(axis(mt)); wk.appendChild(U.el('div', {'class':'m', style:'text-align:center'}, mt.axis)); ax.appendChild(wk); blk.appendChild(ax);
    host.appendChild(blk);
  });
  document.getElementById('foot').textContent = D.foot;
  if(window.__fit) window.__fit();
}
window.__redraw = render; render();
