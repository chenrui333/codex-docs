---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/discover-protein-folding-architectures'
source_last_modified: '2026-06-03T19:26:41Z'
source_etag: 'W/"9d403542ed76b5a0f4830c402d661d4a"'
codex_cli_versions: ["0.136.0"]
codex_cli_versions_raw: ["codex-cli 0.136.0"]
---

# Discover protein folding architectures | Codex use cases

Source: https://developers.openai.com/codex/use-cases/discover-protein-folding-architectures

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Discover protein folding architectures

Turn protein-folding hypotheses into benchmarked experiment loops.

Difficulty **Advanced**

Time horizon **Long-running**

Use Codex with Goal Mode to research and implement novel architectural modifications to AlphaFold2 for improved protein folding performance.

## Best for

- Computational biologists exploring architecture, loss, or curriculum changes against an automatically scorable benchmark.
- Researchers who have a scientifically motivated hypothesis and want to compress the path from idea to working experimental fork.
- ML engineers running long-lived autoresearch loops that require persistent experiment tracking and iterative debugging.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/discover-protein-folding-architectures/?export=pdf)

Use Codex with Goal Mode to research and implement novel architectural modifications to AlphaFold2 for improved protein folding performance.

Advanced

Long-running

Related links

[Follow a goal](/codex/use-cases/follow-goals)  [SimplexFold repository](https://github.com/ChrisHayduk/SimplexFold)  [SimplexFold benchmark plan](https://github.com/ChrisHayduk/SimplexFold/blob/main/BENCHMARK_PLAN.md)  [NanoFold competition](https://github.com/ChrisHayduk/nanoFold-Competition)

## Best for

- Computational biologists exploring architecture, loss, or curriculum changes against an automatically scorable benchmark.
- Researchers who have a scientifically motivated hypothesis and want to compress the path from idea to working experimental fork.
- ML engineers running long-lived autoresearch loops that require persistent experiment tracking and iterative debugging.

## Starter prompt

Use Goal Mode to improve the validation lDDT-Cα score of this AlphaFold2-style protein-structure model on the NanoFold public benchmark.
The scientific hypothesis is that persistent higher-order geometric states may help the model learn protein geometry more efficiently from limited data:
- retain the standard MSA and pairwise representations;
- add sparse learned 2-simplex face states for selected residue triplets;
- add sparse learned 3-simplex tetrahedral states for selected residue quadruplets;
- construct topology only from official benchmark inputs and model-generated recycled geometry;
- keep the implementation computationally practical under NanoFold constraints.
Maintain durable tracking files for:
1. The current strategy, status, and proposed next steps in PLAN.md
2. A structured log of experiments and results in EXPERIMENTS.md
3. A running scratchpad of notes and thoughts in EXPERIMENT\_NOTES.md
For each iteration:
1. state the hypothesis being tested;
2. make the smallest coherent code or configuration change;
3. run the relevant tests and benchmark slice;
4. record metrics, latency, memory, and failure modes;
5. decide whether to keep, revert, or refine the change;
6. periodically reassess the architecture-level search direction rather than only tuning local hyperparameters.
Do not claim generalization gains from smoke tests or single-chain overfit diagnostics. Prefer matched comparisons and preserve the evidence boundary.

[Open in the Codex app](codex://threads/new?prompt=Use+Goal+Mode+to+improve+the+validation+lDDT-C%CE%B1+score+of+this+AlphaFold2-style+protein-structure+model+on+the+NanoFold+public+benchmark.%0A%0AThe+scientific+hypothesis+is+that+persistent+higher-order+geometric+states+may+help+the+model+learn+protein+geometry+more+efficiently+from+limited+data%3A%0A%0A-+retain+the+standard+MSA+and+pairwise+representations%3B%0A-+add+sparse+learned+2-simplex+face+states+for+selected+residue+triplets%3B%0A-+add+sparse+learned+3-simplex+tetrahedral+states+for+selected+residue+quadruplets%3B%0A-+construct+topology+only+from+official+benchmark+inputs+and+model-generated+recycled+geometry%3B%0A-+keep+the+implementation+computationally+practical+under+NanoFold+constraints.%0A%0AMaintain+durable+tracking+files+for%3A%0A1.+The+current+strategy%2C+status%2C+and+proposed+next+steps+in+PLAN.md%0A2.+A+structured+log+of+experiments+and+results+in+EXPERIMENTS.md%0A3.+A+running+scratchpad+of+notes+and+thoughts+in+EXPERIMENT_NOTES.md%0A%0AFor+each+iteration%3A%0A1.+state+the+hypothesis+being+tested%3B%0A2.+make+the+smallest+coherent+code+or+configuration+change%3B%0A3.+run+the+relevant+tests+and+benchmark+slice%3B%0A4.+record+metrics%2C+latency%2C+memory%2C+and+failure+modes%3B%0A5.+decide+whether+to+keep%2C+revert%2C+or+refine+the+change%3B%0A6.+periodically+reassess+the+architecture-level+search+direction+rather+than+only+tuning+local+hyperparameters.%0A%0ADo+not+claim+generalization+gains+from+smoke+tests+or+single-chain+overfit+diagnostics.+Prefer+matched+comparisons+and+preserve+the+evidence+boundary. "Open in the Codex app")

Use Goal Mode to improve the validation lDDT-Cα score of this AlphaFold2-style protein-structure model on the NanoFold public benchmark.
The scientific hypothesis is that persistent higher-order geometric states may help the model learn protein geometry more efficiently from limited data:
- retain the standard MSA and pairwise representations;
- add sparse learned 2-simplex face states for selected residue triplets;
- add sparse learned 3-simplex tetrahedral states for selected residue quadruplets;
- construct topology only from official benchmark inputs and model-generated recycled geometry;
- keep the implementation computationally practical under NanoFold constraints.
Maintain durable tracking files for:
1. The current strategy, status, and proposed next steps in PLAN.md
2. A structured log of experiments and results in EXPERIMENTS.md
3. A running scratchpad of notes and thoughts in EXPERIMENT\_NOTES.md
For each iteration:
1. state the hypothesis being tested;
2. make the smallest coherent code or configuration change;
3. run the relevant tests and benchmark slice;
4. record metrics, latency, memory, and failure modes;
5. decide whether to keep, revert, or refine the change;
6. periodically reassess the architecture-level search direction rather than only tuning local hyperparameters.
Do not claim generalization gains from smoke tests or single-chain overfit diagnostics. Prefer matched comparisons and preserve the evidence boundary.

## Explore a protein-folding architecture hypothesis

Use Codex Goal Mode when you have a protein-folding hypothesis that needs more
than one implementation pass. Give Codex a bounded scientific direction, a
working baseline, and an automatically scorable benchmark. Codex can implement
the architecture fork, track experiments, diagnose failures, and continue
iterating while you review the evidence.

This example started with a specific question: could an AlphaFold2-style model
learn useful protein geometry more efficiently if its trunk represented not
only residues and residue pairs, but also explicit higher-order topological
objects?

## Define a bounded experiment

AlphaFold2 already uses powerful pairwise and triangle-style reasoning inside
the Evoformer. Its triangle operations improve edge representations, but still
write back into a pair tensor. The scientist proposed testing whether persistent
learned representations for triangular faces and tetrahedral cells could
provide a useful inductive bias in a data-limited setting.

The resulting public repository, [SimplexFold](https://github.com/ChrisHayduk/SimplexFold),
adds sparse face states `F_ijk` and tetrahedral states `U_ijkl` alongside the
conventional pair representation `Z_ij`.

```
MSA representation M
        <-> pair / edge tensor Z_ij
        <-> sparse face tensor F_ijk
        <-> sparse tetra tensor U_ijkl
        -> structure module
        -> recycled geometry
        loops back into the next pass
```

Start with the starter prompt on this page, a minimal AlphaFold2-style baseline,
and the public NanoFold benchmark. The benchmark provides a small, curated
fixed-data and automatically scorable substrate for structural-biology
experimentation. Keep the first implementation small enough to test with
targeted unit tests and microbenchmarks before launching expensive training
runs.

## Run the search with Goal Mode

1. Supply a falsifiable, high-level scientific hypothesis instead of asking the model to invent an entire research agenda from scratch.
2. Use GPT-5.5 Pro in ChatGPT to convert that direction into an implementation plan with explicit constraints and ablations.
3. Ask Codex to implement the smallest runnable [SimplexFold](https://github.com/ChrisHayduk/SimplexFold) baseline, then verify it with targeted unit tests and microbenchmarks.
4. Give the resulting repository to Codex Goal Mode and instruct it to hill-climb validation `lDDT-Cα` on the NanoFold benchmark while preserving experiment logs, plans, and artifact references.
5. Run Goal Mode continuously while it uses benchmark feedback to iterate on the architecture, training recipe, and experimental harness. In this example, the loop ran for more than 150 hours.

Use `PLAN.md` for the current strategy and next steps, `EXPERIMENTS.md` for a
structured log of results, and `EXPERIMENT_NOTES.md` for the running scratchpad.
These artifacts make a long-running search auditable and give you a stable
place to steer the next iteration.

Goal Mode is useful here because the search requires repeated implementation,
testing, experiment tracking, failure diagnosis, and benchmark-driven
iteration. Unguided autoresearch often drifted toward familiar local changes
such as losses, optimizers, and hyperparameters. A compact scientist-supplied
architecture hypothesis gave Codex a more meaningful search space while still
leaving room to test, diagnose, and refine the implementation.

This workflow is also useful for teams evaluating how scientist-in-the-loop
steering changes the quality of agentic scientific search.

## Example result

The result of this workflow was [SimplexFold](https://github.com/ChrisHayduk/SimplexFold),
an experimental architecture with explicit higher-order simplex states. Review
the topology alongside the benchmark logs to confirm that each iteration still
tests the original scientific idea.

![A comparison of 1-, 2-, and 3-simplex protein geometry.](/codex/use-cases/discover-protein-folding-architectures-simplex.webp)

The useful lesson is not that Codex autonomously solved protein folding. The
workflow shows how Goal Mode can act as a persistent scientific engineering
loop: a scientist contributes the conceptual move, and Codex compresses the
implementation, experimentation, debugging, and follow-up search cycle.

Treat promising diagnostics as evidence that the implementation path works,
not as proof of generalization. Review the agent’s trajectory periodically,
steer it back toward scientifically meaningful architecture questions if it
collapses into local hyperparameter tuning, and promote claims only after
matched public-validation comparisons and appropriate replicates.

## Resources

- [SimplexFold repository](https://github.com/ChrisHayduk/SimplexFold)
- [SimplexFold benchmark plan](https://github.com/ChrisHayduk/SimplexFold/blob/main/BENCHMARK_PLAN.md)
- [NanoFold competition](https://github.com/ChrisHayduk/nanoFold-Competition)
- [NanoFold competition rules](https://github.com/ChrisHayduk/nanoFold-Competition/blob/main/docs/COMPETITION.md)
- [Goal Mode running for more than 150 hours](https://x.com/ChrisHayduk/status/2055757345506877759?s=20)
- [Goal Mode article](https://x.com/ChrisHayduk/status/2053807198870880743?s=20)

## Related use cases

[![](/codex/use-cases/scrna-seq-post-count-qc.webp)

### Annotate scRNA-seq data

Use Codex with the NGS Analysis plugin to turn a 10x-style matrix bundle into QC-filtered...

Sciences  Data](/codex/use-cases/scrna-seq-post-count-qc)[![](/codex/use-cases/bulk-rna-seq-fastq-qc.webp)

### Validate bulk RNA-seq inputs

Use Codex with the NGS Analysis plugin to validate sample sheets, FASTQs, and references...

Sciences  Data](/codex/use-cases/bulk-rna-seq-fastq-qc)[![](/codex/use-cases/target-prioritization.webp)

### Prioritize drug targets

Use Codex with the Life Science Research plugin to normalize entities, retrieve genetics...

Sciences  Data](/codex/use-cases/target-prioritization)

