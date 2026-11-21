// Entry program for the make.fun news-image-20261121 bounty.
// The front page is rendered ahead of time by draw.py into entry.png;
// this program only places that exact file at the grader's output path.
// It reads no network and writes the same bytes on every run.
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const input = resolve(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outPath = resolve(outDir, "entry.png");

const bytes = await readFile(input);
await mkdir(outDir, { recursive: true });
await writeFile(outPath, bytes);
const short = createHash("sha256").update(bytes).digest("hex").slice(0, 12);
console.log(`wrote ${outPath} (${bytes.length} bytes, sha256 ${short}...)`);
