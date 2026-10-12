// Inspect a real kit build in headless Chromium and record raw measurements.
//
// Called by kit_build.sh (see README.md). Needs the globally installed playwright
// (NODE_PATH=/opt/node22/lib/node_modules) and its Chromium (PLAYWRIGHT_BROWSERS_PATH);
// never runs `playwright install`. Outbound requests (the kit's CDNs) go through
// $HTTPS_PROXY when it is set; the local server is reached directly.
//
//   node kit_checks.mjs --url URL --control-url URL --expected expected.json \
//        --out browser.json --pdf out.pdf --screens DIR
//
// It measures; kit_report.py grades. Nothing here decides PASS or FAIL.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
const exp = JSON.parse(fs.readFileSync(args.expected, 'utf8'));
// Playwright forces loopback through the proxy unless told not to; the local server must
// be reached directly.
process.env.PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK = '1';
const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: '127.0.0.1,localhost' } : undefined;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await chromium.launch({ proxy });
const out = { url: args.url, requests: { failed: [], total: 0 }, console_errors: [], page_errors: [] };
const okUrls = new Set();

async function openPage(url, record) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  if (record) {
    page.on('request', () => { out.requests.total += 1; });
    page.on('requestfailed', (r) => out.requests.failed.push({ url: r.url(), why: r.failure()?.errorText || 'failed' }));
    page.on('response', (r) => { if (r.status() >= 400) out.requests.failed.push({ url: r.url(), why: `HTTP ${r.status()}` }); else okUrls.add(r.url()); });
    page.on('console', (m) => { if (m.type() === 'error') out.console_errors.push(m.text().slice(0, 300)); });
    page.on('pageerror', (e) => out.page_errors.push(String(e).slice(0, 300)));
  }
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  await page.waitForFunction(() => document.readyState === 'complete', null, { timeout: 60000 });
  try {
    await page.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, { timeout: 60000 });
    await page.evaluate(() => MathJax.startup.promise);
  } catch (e) { out.mathjax_wait_error = String(e).slice(0, 200); }
  try { await page.waitForSelector('d-citation-list li', { timeout: 20000, state: 'attached' }); } catch (e) { /* graded later */ }
  await sleep(1500);
  return { ctx, page };
}

const MAIN = 'd-article:not(#bibtex-container)';

// ---- iframe growth (review RM-4): in a fresh page per width, every iframe's height
// 5 s and 60 s after load, and its document's body.scrollHeight at 60 s.
async function growth(width) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 } });
  const p = await ctx.newPage();
  await p.goto(args.url, { waitUntil: 'load', timeout: 120000 });
  const t0 = Date.now();
  const SEL = `${MAIN} iframe`;
  const n = await p.$$eval(SEL, (f) => f.length);
  for (let i = 0; i < n; i++) { await p.$$eval(SEL, (f, i) => f[i].scrollIntoView({ block: 'center' }), i); await sleep(150); }
  const snap = () => p.$$eval(SEL, (fs) => fs.map((f) => {
    let body = null; try { body = f.contentDocument.body.scrollHeight; } catch (e) { /* cross-origin */ }
    return { src: f.getAttribute('src'), h: Math.round(f.getBoundingClientRect().height), body };
  }));
  await sleep(Math.max(0, 5000 - (Date.now() - t0)));
  const at5 = await snap();
  await sleep(Math.max(0, 60000 - (Date.now() - t0)));
  const at60 = await snap();
  await ctx.close();
  return { width, at5, at60 };
}

const { page } = await openPage(args.url, true);
const growthRuns = Promise.all([1280, 1024, 390].map(growth));

// ---- iframes at 1280: scroll each into view so lazy frames load, then measure
const frameHandles = await page.$$(`${MAIN} iframe`);
out.iframes = [];
for (const h of frameHandles) {
  await h.scrollIntoViewIfNeeded();
  let loaded = false;
  for (let t = 0; t < 60 && !loaded; t++) {
    loaded = await h.evaluate((el) => {
      try { const d = el.contentDocument; return !!d && d.readyState === 'complete' && d.URL.endsWith('.html') && !!d.body && d.body.children.length > 0; }
      catch (e) { return false; }
    });
    if (!loaded) await sleep(250);
  }
  await sleep(800);
  const status = await h.evaluate(async (el) => {
    try { return (await fetch(el.src, { method: 'HEAD', cache: 'no-store' })).status; } catch (e) { return 0; }
  });
  if (status !== 200) loaded = false;
  out.iframes.push(await h.evaluate((el, loaded) => {
    let content = null, same = false;
    try { const d = el.contentDocument; same = !!d; content = Math.max(d.documentElement.scrollHeight, d.body.scrollHeight); } catch (e) { same = false; }
    return { src: el.getAttribute('src'), title: el.getAttribute('title'), loaded, same_origin: same,
             attr_height: Number(el.getAttribute('height')) || null,
             final_height: Math.round(el.getBoundingClientRect().height), content_height: content };
  }, loaded));
  out.iframes[out.iframes.length - 1].http_status = status;
}
await page.evaluate(() => window.scrollTo(0, 0));
await sleep(500);

// ---- everything read from the DOM at 1280
Object.assign(out, await page.evaluate((MAIN) => {
  const art = document.querySelector(MAIN);
  const r = {};
  r.title = document.querySelector('d-title h1')?.textContent.trim();
  r.description = document.querySelector('d-title p')?.textContent.trim();
  r.byline = document.querySelector('d-byline')?.innerText || '';
  r.cite_box = document.getElementById('bibtex-box')?.innerText || '';
  r.cite_attribution = document.getElementById('bibtex-academic-attribution')?.innerText || '';
  // math
  // MathJax marks a TeX error with mjx-merror; an undefined macro (the noundefined
  // extension) is drawn as red text: mtext mathcolor="red" in the assistive MathML (CHTML
  // draws glyphs with CSS, so the visible element has no text content).
  const merr = [...document.querySelectorAll('mjx-merror, [data-mjx-error]'),
                ...[...art.querySelectorAll('mjx-container')].filter((c) => c.querySelector('mjx-assistive-mml mtext[mathcolor="red"], mjx-mtext[style*="color: red"]'))];
  r.math = { rendered: art.querySelectorAll('mjx-container').length, errors: merr.length,
             error_texts: merr.slice(0, 10).map((e) => (e.getAttribute('data-mjx-error') || e.querySelector('mjx-assistive-mml')?.textContent || e.textContent).slice(0, 120)) };
  const c = art.cloneNode(true);
  c.querySelectorAll('mjx-container, mjx-assistive-mml, pre, code, script, style, iframe').forEach((n) => n.remove());
  const text = c.textContent;
  const raw = [];
  for (const re of [/\$/g, /\\[a-zA-Z]{2,}/g, /\\[()[\]]/g, /\^\{|_\{/g]) {
    let m; while ((m = re.exec(text)) && raw.length < 40) raw.push(text.slice(Math.max(0, m.index - 40), m.index + 30).replace(/\s+/g, ' '));
  }
  r.raw_tex = raw;
  const b = document.body.cloneNode(true);
  b.querySelectorAll('script').forEach((n) => n.remove());
  const h = b.innerHTML;
  r.liquid_left = (h.match(/\{\{|\{%/g) || []).length;
  r.liquid_samples = [...h.matchAll(/.{0,40}(\{\{|\{%).{0,40}/g)].slice(0, 5).map((m) => m[0]);
  r.tables = art.querySelectorAll('table').length;
  r.one_row_tables = [...art.querySelectorAll('table')].filter((tb) => tb.querySelectorAll('tr').length === 1)
    .map((tb) => tb.textContent.replace(/\s+/g, ' ').trim().slice(0, 120));
  r.br_in_article = art.querySelectorAll('p br').length;
  // references (Distill renders them in the light DOM of d-citation-list)
  r.references = [...document.querySelectorAll('d-citation-list li')].map((li) => ({
    key: li.id, html: li.innerHTML, text: li.innerText, title: li.querySelector('.title')?.textContent ?? null }));
  r.cites = [...document.querySelectorAll('d-cite')].map((el) => ({
    key: el.getAttribute('key'),
    number: el.shadowRoot?.querySelector('.citation-number')?.textContent ?? null,
    hover: el.shadowRoot?.querySelector('d-hover-box')?.innerHTML ?? null }));
  // toc and in-page links
  r.toc = [...document.querySelectorAll('d-contents a')].map((a) => {
    const id = decodeURIComponent((a.getAttribute('href') || '').replace(/^#/, ''));
    return { name: a.textContent.trim(), href: a.getAttribute('href'), resolves: !!document.getElementById(id) };
  });
  r.anchor_links = [...art.querySelectorAll('a[href^="#"]')].map((a) => {
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    return { href: a.getAttribute('href'), resolves: !!document.getElementById(id) };
  });
  // images
  r.images = [...art.querySelectorAll('img')].map((i) => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0, natural: i.naturalWidth }));
  // print companions on screen
  r.companions_screen = [...document.querySelectorAll('.print-companion')].map((e) => getComputedStyle(e).display);
  // listings: rouge's blocks, in order
  r.listings = [...art.querySelectorAll('div.highlighter-rouge')].map((d) => d.querySelector('pre')?.textContent ?? '');
  r.listing_font = (() => { const p = art.querySelector('div.highlighter-rouge pre'); return p ? getComputedStyle(p).fontSize : null; })();
  // footnotes on screen
  const docH = document.documentElement.scrollHeight;
  r.doc_height = docH;
  const heads = [...art.querySelectorAll('h2')];
  r.footnotes = [...document.querySelectorAll('d-footnote')].map((fn) => {
    const y = fn.getBoundingClientRect().top + window.scrollY;
    const before = heads.filter((hh) => hh.getBoundingClientRect().top + window.scrollY <= y).pop();
    return { text: fn.textContent.trim(), marker_y: Math.round(y), marker_frac: +(y / docH).toFixed(3),
             marker_number: fn.shadowRoot?.querySelector('sup span, sup')?.textContent?.trim() ?? null,
             under_heading: before ? before.textContent.trim() : '(before the first section heading)' };
  });
  const fl = document.querySelector('d-footnote-list');
  r.footnote_list = fl ? { y: Math.round(fl.getBoundingClientRect().top + window.scrollY),
    frac: +((fl.getBoundingClientRect().top + window.scrollY) / docH).toFixed(3),
    items: [...(fl.shadowRoot?.querySelectorAll('li') || []), ...fl.querySelectorAll('li')].map((li) => li.textContent.trim()),
    in_appendix: !!fl.closest('d-appendix') } : null;
  r.interact_spans = document.querySelectorAll('.interact').length;
  return r;
}, MAIN));

// ---- overflow at three widths
out.overflow = {};
for (const w of [1024, 1280, 390]) {
  await page.setViewportSize({ width: w, height: 900 });
  await sleep(700);
  out.overflow[w] = await page.evaluate((MAIN) => {
    const art = document.querySelector(MAIN);
    const pres = [...art.querySelectorAll('div.highlighter-rouge pre')].map((p) => ({ scroll: p.scrollWidth, client: p.clientWidth }));
    const sw = document.scrollingElement.scrollWidth, iw = window.innerWidth;
    const wide = [...document.querySelectorAll('body *')].filter((e) => e.getBoundingClientRect().right > iw + 1 && getComputedStyle(e).position !== 'fixed')
      .slice(0, 8).map((e) => `${e.tagName.toLowerCase()}${e.id ? '#' + e.id : ''}${e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : ''} right=${Math.round(e.getBoundingClientRect().right)}`);
    // display math wider than its box: does the reader get a scrollbar, or is it cut off?
    const math = [...art.querySelectorAll('mjx-container[display="true"]')].map((c) => {
      const inner = c.querySelector('mjx-math'); if (!inner) return null;
      const cr = c.getBoundingClientRect(), ir = inner.getBoundingClientRect();
      if (ir.right <= cr.right + 1 && ir.right <= iw + 1) return null;
      let el = c, scrolls = false;
      while (el && el !== document.body) { const ox = getComputedStyle(el).overflowX; if ((ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth) { scrolls = true; break; } el = el.parentElement; }
      const sec = [...art.querySelectorAll('h2')].filter((h) => h.getBoundingClientRect().top <= cr.top).pop();
      return { over_px: Math.round(ir.right - Math.min(cr.right, iw)), scrolls, under: sec ? sec.textContent.trim() : '', tex: (c.querySelector('mjx-assistive-mml')?.textContent || '').slice(0, 60) };
    }).filter(Boolean);
    return { page_scroll_width: sw, inner_width: iw, listings: pres, widest: wide, wide_math: math };
  }, MAIN);
}
await page.setViewportSize({ width: 1280, height: 900 });
await sleep(500);

// ---- screenshots of the first screen
fs.mkdirSync(args.screens, { recursive: true });
for (const [w, h] of [[1280, 800], [1440, 900], [390, 844]]) {
  await page.setViewportSize({ width: w, height: h });
  await page.evaluate(() => window.scrollTo(0, 0));
  await sleep(600);
  await page.screenshot({ path: path.join(args.screens, `top_${w}.png`) });
}
await page.setViewportSize({ width: 1280, height: 900 });

// ---- print media
await page.emulateMedia({ media: 'print' });
await sleep(800);
out.print = await page.evaluate((MAIN) => {
  const art = document.querySelector(MAIN);
  return {
    companions: [...document.querySelectorAll('.print-companion')].map((e) => ({ display: getComputedStyle(e).display,
      img_ok: [...e.querySelectorAll('img')].every((i) => i.complete && i.naturalWidth > 0) })),
    iframes: [...art.querySelectorAll('iframe')].map((f) => getComputedStyle(f).display),
    interact: [...document.querySelectorAll('.interact')].map((e) => getComputedStyle(e).display),
  };
}, MAIN);
// ---- print overflow (review RM-1 to RM-3): at the US Letter width, in print media,
// every table, MathJax container and pre must fit its box and the article, because
// paper cannot scroll. Wrapped listing lines are counted too (reported, not graded).
await page.setViewportSize({ width: 816, height: 1056 });
await sleep(800);
out.print_overflow = await page.evaluate((MAIN) => {
  const art = document.querySelector(MAIN);
  const ar = art.getBoundingClientRect();
  const heads = [...art.querySelectorAll('h2, h3')];
  const under = (el) => { const y = el.getBoundingClientRect().top; const h = heads.filter((x) => x.getBoundingClientRect().top <= y).pop(); return h ? h.textContent.trim().slice(0, 60) : ''; };
  const flagged = [];
  let checked = 0;
  for (const el of art.querySelectorAll('table, mjx-container, pre')) {
    const rc = el.getBoundingClientRect();
    if (rc.width === 0) continue;
    checked += 1;
    const over = el.scrollWidth - el.clientWidth;
    const past = Math.round(rc.right - ar.right);
    if (over > 1 || past > 1) flagged.push({ tag: el.tagName.toLowerCase(), over_px: Math.max(over, past), under: under(el),
      text: el.textContent.replace(/\s+/g, ' ').trim().slice(0, 90) });
  }
  const wraps = [...art.querySelectorAll('div.highlighter-rouge pre')].map((p) => {
    const lines = p.textContent.replace(/\n$/, '').split('\n').length;
    const lh = parseFloat(getComputedStyle(p).lineHeight) || 1;
    const cs = getComputedStyle(p);
    const inner = p.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    return Math.max(0, Math.round(inner / lh) - lines);
  });
  return { checked, flagged, article_overflow: art.scrollWidth - art.clientWidth, text_column: art.querySelector('p')?.clientWidth,
           listing_wrapped_lines: wraps };
}, MAIN);
await page.pdf({ path: args.pdf, format: 'Letter', printBackground: true });
await page.emulateMedia({ media: 'screen' });
await page.setViewportSize({ width: 1280, height: 900 });

// ---- the control build (comments not stripped): same rendered text?
if (args['control-url']) {
  const { page: cp } = await openPage(args['control-url'], false);
  const grab = (p) => p.evaluate((MAIN) => {
    const art = document.querySelector(MAIN);
    return { text: art.innerText, tables: art.querySelectorAll('table').length,
             math: art.querySelectorAll('mjx-container').length, listings: art.querySelectorAll('div.highlighter-rouge').length };
  }, MAIN);
  const a = await grab(page), b = await grab(cp);
  let first = -1;
  for (let i = 0; i < Math.max(a.text.length, b.text.length); i++) if (a.text[i] !== b.text[i]) { first = i; break; }
  out.control = { same_text: a.text === b.text, stripped_len: a.text.length, control_len: b.text.length,
    first_difference: first < 0 ? null : { stripped: a.text.slice(Math.max(0, first - 60), first + 60), control: b.text.slice(Math.max(0, first - 60), first + 60) },
    tables: [a.tables, b.tables], math: [a.math, b.math], listings: [a.listings, b.listings] };
}

out.growth = await growthRuns;
await browser.close();
// A request aborted because the page re-laid out (viewport or print changes) and then
// loaded fine is not a failure.
out.requests.aborted_then_loaded = out.requests.failed.filter((f) => f.why.includes('ERR_ABORTED') && okUrls.has(f.url)).length;
out.requests.failed = out.requests.failed.filter((f) => !(f.why.includes('ERR_ABORTED') && okUrls.has(f.url)));
fs.writeFileSync(args.out, JSON.stringify(out, null, 1));
console.log(`kit_checks: ${out.iframes.length} iframes, ${out.references.length} references, ${out.cites.length} d-cite, ` +
  `${out.tables} tables, ${out.math.rendered} math, ${out.requests.failed.length} failed requests -> ${args.out}`);
