
var DEC = (function(){
  function R(b){ this.b=b; this.p=0; }
  R.prototype.v = function(){ var n=0, s=0, x; do { x=this.b[this.p++]; n += (x & 127) * Math.pow(2, s); s+=7; } while(x & 128); return n; };
  function unzrle(b, n){ var r=new R(b), out=new Uint8Array(n), i=0;
    while(i<n){ i += r.v(); var lit=r.v(); for(var k=0;k<lit;k++) out[i++]=b[r.p++]; } return out; }
  function unbits(b, n){ var out=new Uint8Array(n); for(var i=0;i<n;i++) out[i]=(b[i>>3]>>(7-(i&7)))&1; return out; }
  function cells(b, T){ var r=new R(b), out=[]; for(var f=0;f<T;f++){ var c=r.v(), a=new Array(c); for(var k=0;k<c;k++) a[k]=r.v(); out.push(a);} return out; }
  function hazard(h0, b, T, N){ var r=new R(b), out=new Uint8Array(T*N); out.set(h0,0);
    for(var f=1;f<T;f++){ out.copyWithin(f*N,(f-1)*N,f*N); var c=r.v(); for(var k=0;k<c;k++){ var i=r.v(); out[f*N+i]=b[r.p++]; } } return out; }
  return {R:R, unzrle:unzrle, unbits:unbits, cells:cells, hazard:hazard};
})();
