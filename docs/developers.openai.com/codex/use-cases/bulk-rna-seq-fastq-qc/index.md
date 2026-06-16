---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/bulk-rna-seq-fastq-qc'
source_last_modified: '2026-06-05T18:02:02Z'
source_etag: 'W/"154d23be483e720b8202509f754d0b06"'
codex_cli_versions: ["0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0"]
codex_cli_versions_raw: ["codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0"]
---

# Validate bulk RNA-seq inputs | Codex use cases

Source: https://developers.openai.com/codex/use-cases/bulk-rna-seq-fastq-qc

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Validate bulk RNA-seq inputs

Validate bulk RNA-seq inputs before differential expression.

Difficulty **Intermediate**

Time horizon **Long-running**

Use Codex with the NGS Analysis plugin to validate sample sheets, FASTQs, and references, then return MultiQC, Salmon matrices, provenance, and a short QC interpretation before differential expression.

## Best for

- Bioinformatics teams validating bulk RNA-seq inputs before differential expression.
- Researchers who want transcript and gene-level quantification plus QC in one thread.
- Teams that need mapping-rate, duplication, library-type, and resource-readiness review.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/bulk-rna-seq-fastq-qc/?export=pdf)

Use Codex with the NGS Analysis plugin to validate sample sheets, FASTQs, and references, then return MultiQC, Salmon matrices, provenance, and a short QC interpretation before differential expression.

Intermediate

Long-running

Related links

[Request access to GPT-Rosalind](https://openai.com/form/life-sciences-access/)

## Best for

- Bioinformatics teams validating bulk RNA-seq inputs before differential expression.
- Researchers who want transcript and gene-level quantification plus QC in one thread.
- Teams that need mapping-rate, duplication, library-type, and resource-readiness review.

## Skills & Plugins

- [NGS Analysis](codex://plugins/ngs-analysis@openai-curated)

  Validate sequencing inputs, run bulk RNA-seq counts and QC, and return auditable artifacts.

| Skill | Why use it |
| --- | --- |
| [NGS Analysis](codex://plugins/ngs-analysis@openai-curated) | Validate sequencing inputs, run bulk RNA-seq counts and QC, and return auditable artifacts. |

## Starter prompt

Use the NGS Analysis plugin.
Run bulk RNA-seq FASTQ-to-count QC on the provided sample sheet, FASTQ root, transcriptome FASTA, genome FASTA, and GTF.
Return:
- run\_manifest.json
- MultiQC plus browser-safe review links
- Salmon transcript- and gene-level matrices
- validation and resource-readiness artifacts
- a short QC interpretation that calls out mapping rate, duplication, library-type agreement, outlier samples, and anything that would block downstream differential expression

Open in the Codex app

Use the NGS Analysis plugin.
Run bulk RNA-seq FASTQ-to-count QC on the provided sample sheet, FASTQ root, transcriptome FASTA, genome FASTA, and GTF.
Return:
- run\_manifest.json
- MultiQC plus browser-safe review links
- Salmon transcript- and gene-level matrices
- validation and resource-readiness artifacts
- a short QC interpretation that calls out mapping rate, duplication, library-type agreement, outlier samples, and anything that would block downstream differential expression

## Leverage skills

The NGS Analysis plugin includes:

- `ngs-analysis-router`
- `ngs-bulk-rnaseq-counts-qc`
- `ngs-runtime-env`

When you use the plugin, Codex can use all these packaged skills.

## Step-by-step guide

1. Point Codex to a directory with the sample sheet, FASTQs, transcriptome FASTA, genome FASTA, and GTF, or provide exact file references.
2. Run the starter prompt so Codex can validate strandedness, reference consistency, and tool readiness before execution.
3. Open the generated MultiQC and matrix artifacts in Codex to review mapping rate, duplication, library-type agreement, and resource readiness.
4. Continue in the same thread to fix blockers, rerun with updated metadata, or hand the resulting gene-level matrices into downstream differential expression.

## Results

The run returns a QC-reviewed counts bundle rather than a bare quantification
output. Start with the MultiQC report to identify warnings that could affect
downstream interpretation. In this example, Codex surfaces FastQC
sequence-content warnings alongside the run summary so the team can decide
whether the observed pattern is expected for the library preparation.

![Review FastQC sequence-content warnings alongside the bulk RNA-seq run summary.](/codex/use-cases/bulk-rna-seq-fastq-qc-screenshot-1.webp)

Next, review the Salmon statistics in the same report. Mapping rates,
library-type assignments, and duplication signals provide a compact readiness
check before differential expression.

![Inspect Salmon alignment and library-type statistics from the generated MultiQC report.](/codex/use-cases/bulk-rna-seq-fastq-qc-screenshot-2.webp)

The resulting gene-level count matrix is saved as a reusable artifact. Open it
in Codex to confirm the expected samples and features are present, then keep it
with the run provenance for downstream analysis.

![Open the generated gene-level count matrix for downstream review.](/codex/use-cases/bulk-rna-seq-fastq-qc-screenshot-3.webp)

## Related use cases

[![](/codex/use-cases/scrna-seq-post-count-qc.webp)

### Annotate scRNA-seq data

Use Codex with the NGS Analysis plugin to turn a 10x-style matrix bundle into QC-filtered...

Sciences  Data](/codex/use-cases/scrna-seq-post-count-qc)[![](/codex/use-cases/discover-protein-folding-architectures.webp)

### Discover protein folding architectures

Use Codex with Goal Mode to research and implement novel architectural modifications to...

Sciences  Engineering](/codex/use-cases/discover-protein-folding-architectures)[![](/codex/use-cases/target-prioritization.webp)

### Prioritize drug targets

Use Codex with the Life Science Research plugin to normalize entities, retrieve genetics...

Sciences  Data](/codex/use-cases/target-prioritization)

