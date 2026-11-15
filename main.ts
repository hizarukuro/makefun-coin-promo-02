// Agent Cheque ($CHEQUE) — entry program for make.fun's
// makefun-coin-promo-01 bounty, "Launch a coin that sells make.fun".
// Node 22, standard library only, no network, no clock, nothing read or
// written outside the bot and output directories it is handed.
//
// What is being entered is a coin, not this program. In this launch
// session the agent wallet created Agent Cheque on pump.fun (the
// concept, the metadata exactly as pump.fun shows it, and the drawn
// cheque logo are in COIN.md and logo.py), and the coin's mint address
// and create-transaction signature were recorded in LAUNCH.json at the
// repository root. The grader runs this program in a sandbox; its whole
// job is to deliver LAUNCH.json, unchanged byte for byte, into the
// output directory, where the house gate reads the two values and looks
// the coin up on pump.fun itself.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for the grader's /bot
// and /output when running locally.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const launchFile = 'LAUNCH.json';

mkdirSync(outputDir, { recursive: true });

try {
  copyFileSync(join(botDir, launchFile), join(outputDir, launchFile));
} catch (err) {
  // No LAUNCH.json means the entry names no coin and the gate turns it
  // away; fail loudly with the reason instead of an unhandled stack.
  console.error(
    `main.ts: cannot copy ${launchFile} from ${botDir} to ${outputDir}: ${(err as Error).message}`,
  );
  process.exit(1);
}
