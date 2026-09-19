// Build a .pptx from a course's slides.yaml.  Usage: node scripts/build_slides.js <path/to/slides.yaml> [out.pptx]
// Slide types: title | section | bullets | two_col | table | demo | lab | quote | close.  Speaker notes from 'notes'.
const fs = require('fs'), path = require('path');
let yaml; try { yaml = require('js-yaml'); } catch { yaml = require(require('child_process').execSync('npm root -g').toString().trim() + '/js-yaml'); }
const pptxgen = require('pptxgenjs');
const [,, src, outArg] = process.argv;
if (!src) { console.error('usage: node scripts/build_slides.js <slides.yaml> [out.pptx]'); process.exit(1); }
const spec = yaml.load(fs.readFileSync(src, 'utf8'));
const out = outArg || path.join(path.dirname(src), (spec.deck.file || 'slides') + '.pptx');
const C = { navy: '1F2A44', teal: '0F766E', paper: 'FBFAF7', ink: '14213D', muted: '5B6170', gold: 'B7791F', line: 'D9D6CF', white: 'FFFFFF' };
const F = 'Georgia';
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.title = spec.deck.title;
const W = 10, H = 5.625;
function footer(s, n) { s.addText(`${spec.deck.footer || spec.deck.brand}   ·   ${n}`, { x: 0.4, y: H - 0.35, w: W - 0.8, h: 0.25, fontFace: F, fontSize: 9, color: C.muted, isTextBox: true, margin: 0 }); }
function bulletsBox(s, items, x, y, w, h, size = 16, color = C.ink) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6 } })), { x, y, w, h, fontFace: F, fontSize: size, color, isTextBox: true, valign: 'top', margin: 0 });
}
spec.slides.forEach((sl, idx) => {
  const n = idx + 1; const s = pres.addSlide(); s.background = { color: C.paper }; if (sl.notes) s.addNotes(sl.notes);
  if (sl.type === 'title') {
    s.background = { color: C.navy };
    s.addText(spec.deck.brand, { x: 0.6, y: 0.5, w: 4, h: 0.4, fontFace: F, fontSize: 14, color: C.gold, isTextBox: true, margin: 0 });
    s.addText(sl.title, { x: 0.6, y: 1.5, w: W - 1.2, h: 1.2, fontFace: F, fontSize: 38, bold: true, color: C.white, isTextBox: true, margin: 0 });
    s.addText(sl.subtitle || '', { x: 0.6, y: 2.9, w: W - 1.2, h: 1.4, fontFace: F, fontSize: 16, color: 'D9D6CF', isTextBox: true, margin: 0 });
    return;
  }
  if (sl.type === 'section') {
    s.background = { color: C.teal };
    s.addText(sl.title, { x: 0.6, y: 2.0, w: W - 1.2, h: 1.4, fontFace: F, fontSize: 34, bold: true, color: C.white, isTextBox: true, margin: 0 }); footer(s, n); return;
  }
  // header band for content slides
  const tag = { demo: 'DEMO', lab: 'LAB', close: 'CLOSE' }[sl.type];
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: W, h: 0.9, fill: { color: sl.type === 'demo' ? C.teal : sl.type === 'lab' ? C.gold : C.navy } });
  s.addText(sl.title, { x: 0.5, y: 0.15, w: W - 2.2, h: 0.6, fontFace: F, fontSize: 22, bold: true, color: C.white, isTextBox: true, margin: 0, valign: 'middle' });
  if (tag) s.addText(tag + (sl.duration ? ` · ${sl.duration}` : ''), { x: W - 2.0, y: 0.25, w: 1.6, h: 0.4, fontFace: F, fontSize: 11, bold: true, color: C.white, align: 'right', isTextBox: true, margin: 0 });
  if (sl.type === 'bullets' || sl.type === 'demo' || sl.type === 'lab' || sl.type === 'close') {
    bulletsBox(s, sl.bullets || [], 0.6, 1.2, W - 1.2, sl.command ? 2.8 : 3.8, sl.bullets && sl.bullets.length > 5 ? 14 : 17);
    if (sl.command) s.addText(sl.command, { x: 0.6, y: 4.2, w: W - 1.2, h: 0.5, fontFace: 'Courier New', fontSize: 13, color: C.white, fill: { color: C.ink }, isTextBox: true, margin: 6, valign: 'middle' });
  } else if (sl.type === 'two_col') {
    bulletsBox(s, sl.left, 0.6, 1.2, 4.3, 3.9, 15); bulletsBox(s, sl.right, 5.1, 1.2, 4.3, 3.9, 15);
    s.addShape(pres.ShapeType.line, { x: 4.95, y: 1.3, w: 0, h: 3.6, line: { color: C.line, width: 1 } });
  } else if (sl.type === 'table') {
    const rows = [sl.header.map(h => ({ text: h, options: { bold: true, color: C.white, fill: { color: C.navy }, fontFace: F, fontSize: 12 } }))]
      .concat(sl.rows.map(r => r.map(c => ({ text: String(c), options: { fontFace: F, fontSize: 12, color: C.ink } }))));
    s.addTable(rows, { x: 0.5, y: 1.15, w: W - 1.0, colW: sl.colW, border: { type: 'solid', color: C.line, pt: 0.5 }, autoPage: false, rowH: 0.35 });
  } else if (sl.type === 'quote') {
    s.addText(`“${sl.text}”`, { x: 0.8, y: 1.5, w: W - 1.6, h: 2.5, fontFace: F, fontSize: 24, italic: true, color: C.ink, isTextBox: true, margin: 0, valign: 'middle' });
  }
  footer(s, n);
});
pres.writeFile({ fileName: out }).then(() => console.log(`wrote ${out} (${spec.slides.length} slides)`));
