
(function(){
  // Theme: follow the embedding page when same-origin (al-folio sets data-theme).
  function syncTheme(){
    try{
      var p = window.parent && window.parent !== window && window.parent.document;
      var t = p && p.documentElement.getAttribute('data-theme');
      if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);return;}
    }catch(e){}
  }
  syncTheme();
  try{
    var pd = window.parent && window.parent !== window && window.parent.document;
    if(pd && window.MutationObserver){
      new MutationObserver(function(){syncTheme(); if(window.__redraw) window.__redraw();})
        .observe(pd.documentElement,{attributes:true,attributeFilter:['data-theme']});
    }
  }catch(e){}
  // Self-size the iframe when same-origin (fixed iframe heights clip on phones).
  function fit(){
    try{
      var fe = window.frameElement;
      if(fe){ fe.style.height = (document.documentElement.scrollHeight + 4) + 'px'; }
    }catch(e){}
  }
  window.__fit = fit;
  window.addEventListener('load', fit);
  if(window.ResizeObserver){ new ResizeObserver(fit).observe(document.body); }
  window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)')
    .addEventListener && window.matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', function(){ if(window.__redraw) window.__redraw(); });
})();
var U = {
  css: function(name){ return getComputedStyle(document.documentElement).getPropertyValue('--'+name).trim(); },
  reduced: function(){ return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); },
  el: function(tag, attrs, text){
    var e = document.createElement(tag);
    if(attrs) for(var k in attrs){ if(attrs[k]!==null && attrs[k]!==undefined) e.setAttribute(k, attrs[k]); }
    if(text!==undefined && text!==null) e.textContent = text;
    return e;
  },
  svg: function(tag, attrs, text){
    var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    if(attrs) for(var k in attrs){ if(attrs[k]!==null && attrs[k]!==undefined) e.setAttribute(k, attrs[k]); }
    if(text!==undefined && text!==null) e.textContent = text;
    return e;
  },
  clear: function(n){ while(n.firstChild) n.removeChild(n.firstChild); },
  sgn: function(x, d){ var s = (x>0?'+':(x<0?'−':'')); return s + Math.abs(x).toFixed(d); },
  ci: function(a, d){ return '[' + U.sgn(a[0],d) + ', ' + U.sgn(a[1],d) + ']'; },
  tip: (function(){
    var t = null;
    function node(){ if(!t){ t = document.createElement('div'); t.className='tt'; t.setAttribute('role','tooltip'); document.body.appendChild(t);} return t; }
    return {
      show: function(lines, x, y){
        var n = node(); U.clear(n);
        lines.forEach(function(l, i){
          var d = document.createElement('div');
          if(Array.isArray(l)){ var b=document.createElement('b'); b.textContent=l[0]; d.appendChild(b);
            if(l[1]) d.appendChild(document.createTextNode(' ' + l[1])); }
          else d.textContent = l;
          n.appendChild(d);
        });
        n.style.display='block';
        var w = n.offsetWidth, h = n.offsetHeight;
        var vx = Math.min(x + 14, window.innerWidth - w - 6), vy = y + 14;
        if(vy + h > window.innerHeight - 4) vy = Math.max(4, y - h - 10);
        n.style.left = Math.max(4, vx) + 'px'; n.style.top = vy + 'px';
      },
      hide: function(){ if(t) t.style.display='none'; }
    };
  })(),
  b64: function(s){ var bin = atob(s), n = bin.length, out = new Uint8Array(n);
    for(var i=0;i<n;i++) out[i] = bin.charCodeAt(i); return out; },
  // Tooltip at a focused element's position (keyboard parity with hover).
  tipAt: function(el, lines){ var r = el.getBoundingClientRect(); U.tip.show(lines, r.left + r.width/2, r.top + r.height/2); }
};
