#!/usr/bin/env node
/**
 * Filter NLC concept-graph React Flow edges by data.edgeClass (path | summary | both).
 * SSOT diagram: docs/diagrams/nlc-concept-graph-spine.json
 * Ontology: docs/nlc/concept-graph/
 *
 * Usage (from repo root):
 *   node docs/diagrams/filter-concept-graph-edges.mjs path
 *   node docs/diagrams/filter-concept-graph-edges.mjs summary
 *   node docs/diagrams/filter-concept-graph-edges.mjs both
 *
 * Prints JSON document to stdout (same nodes; filtered edges).
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const seedPath = join(__dir, "nlc-concept-graph-spine.json");

/**
 * @param {object} diagram
 * @param {'path' | 'summary' | 'both'} mode
 */
function filterConceptGraphEdges(diagram, mode = "both") {
  if (mode === "both") {
    return diagram;
  }
  const edges = (diagram.edges ?? []).filter((edge) => {
    const edgeClass = edge?.data?.edgeClass;
    if (edgeClass == null) {
      return true;
    }
    return edgeClass === mode;
  });
  return { ...diagram, edges, defaultEdgeFilter: mode };
}

const mode = process.argv[2] ?? "both";
if (!["path", "summary", "both"].includes(mode)) {
  console.error("usage: filter-concept-graph-edges.mjs <path|summary|both>");
  process.exit(1);
}

const diagram = JSON.parse(readFileSync(seedPath, "utf8"));
const filtered = filterConceptGraphEdges(diagram, mode);
process.stdout.write(`${JSON.stringify(filtered, null, 2)}\n`);
