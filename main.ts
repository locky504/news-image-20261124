// News-image entry for make.fun competition news-image-20261124
// (Node 22, standard library only): its image is the entry.png beside
// this file, drawn by draw.py in this repository from the verified
// world headlines of Tuesday 24 November 2026 (Ukraine sinking a
// Russian warship off Libya, Nvidia reinstating Huang as CEO, NATO
// vowing space defence, Trump offering the Philippines $2.4bn,
// thousands evacuated from a UK concert, and states suing Musk firms
// over Grok images). The program copies it to /output/entry.png, the
// location the grader reads.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// No network, no clock, no randomness: the copy is byte-for-byte, so
// repeated runs write identical bytes.

import { createHash } from 'node:crypto';
import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');

copyFileSync(src, dest);
const bytes = readFileSync(dest);
// Guard: the copied file must be a whole PNG (magic bytes), so a
// truncated or non-image file can never be submitted by accident.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a valid PNG');
}
const sha256 = createHash('sha256').update(bytes).digest('hex');
console.log(`wrote ${dest} (${bytes.length} bytes, sha256 ${sha256})`);
