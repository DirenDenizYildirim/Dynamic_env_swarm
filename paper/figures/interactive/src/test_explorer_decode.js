// Node check: the page's own JS decoder, run on the page's own embedded data,
// must reproduce the arrays whose sha256 the Python builder recorded.
// Usage: node test_explorer_decode.js <explorer.html> <codec_check.json>
const fs = require('fs');
const crypto = require('crypto');
const html = fs.readFileSync(process.argv[2], 'utf8');
const check = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const data = JSON.parse(html.match(/<script type="application\/json" id="data">([\s\S]*?)<\/script>/)[1]);
const decSrc = html.match(/(var DEC = \(function\(\)\{[\s\S]*?\}\)\(\);)/)[1];
const DEC = new Function(decSrc + '; return DEC;')();
const b64 = (s) => Uint8Array.from(Buffer.from(s, 'base64'));
const M = data.meta, L = M.L, NN = L * L, T = M.T, NA = M.N, KK = M.K * M.K;
const sha = (u8) => crypto.createHash('sha256').update(Buffer.from(u8.buffer, u8.byteOffset, u8.byteLength)).digest('hex');
const HZ = DEC.hazard(DEC.unzrle(b64(data.haz0), NN), b64(data.hazd), T, NN);
const SM = DEC.unzrle(b64(data.smoke), T * NN);
const COLLL = DEC.cells(b64(data.coll), T), FOODL = DEC.cells(b64(data.foodd), T), SEEDL = DEC.cells(b64(data.seed), T);
const COLL = new Uint8Array(T * NN), FOOD = new Uint8Array(T * NN);
FOOD.set(DEC.unbits(b64(data.food0), NN), 0);
for (let f = 0; f < T; f++) {
  if (f > 0) { COLL.copyWithin(f * NN, (f - 1) * NN, f * NN); FOOD.copyWithin(f * NN, (f - 1) * NN, f * NN); }
  COLLL[f].forEach((c) => { COLL[f * NN + c] = 1; });
  FOODL[f].forEach((c) => { FOOD[f * NN + c] = 0; });
}
const res = {
  hazard: sha(HZ) === check.hazard,
  smoke_q: sha(SM) === check.smoke_q,
  collapsed: sha(COLL) === check.collapsed,
  food: sha(FOOD) === check.food,
  alive: sha(DEC.unbits(b64(data.alive), T * NA)) === check.alive,
  reveal: sha(DEC.unbits(b64(data.reveal), T * NA * KK)) === check.reveal,
  tau_q: sha(DEC.unzrle(b64(data.tau), T * NA * KK)) === check.tau_q,
  pos: sha(b64(data.pos)) === check.pos,
  seeded: JSON.stringify(SEEDL.map((a) => a.length)) === JSON.stringify(check.seeded_cells_per_frame),
  default_agent: M.agent0 === check.default_agent_index,
};
console.log(check.stem, JSON.stringify(res));
if (!Object.values(res).every(Boolean)) { process.exit(1); }
