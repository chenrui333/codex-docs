---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/target-prioritization'
source_last_modified: '2026-06-05T16:47:11Z'
source_etag: 'W/"ceadab0de96cfe774528f384de78cfba"'
codex_cli_versions: ["0.136.0", "0.137.0", "0.138.0"]
codex_cli_versions_raw: ["codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0"]
---

# Prioritize drug targets | Codex use cases

Source: https://developers.openai.com/codex/use-cases/target-prioritization

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Prioritize drug targets

Rank drug targets across multiple evidence lanes.

Difficulty **Advanced**

Time horizon **Long-running**

Use Codex with the Life Science Research plugin to normalize entities, retrieve genetics, cohort, clinical, literature, and expression evidence in parallel, score each lane, and produce a final ranking with reusable visuals.

## Best for

- Target prioritization questions that need more than one evidence family, such as genetics, cohort replication, disease context, clinical precedent, literature, and expression.
- Teams that want Codex to perform scientific research across multiple evidence lanes, then reconcile the results into one conclusion.
- Scientists who want saved raw payloads, an explicit scoring rubric, and visuals they can reuse in the next review or decision memo.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/target-prioritization/?export=pdf)

Use Codex with the Life Science Research plugin to normalize entities, retrieve genetics, cohort, clinical, literature, and expression evidence in parallel, score each lane, and produce a final ranking with reusable visuals.

Advanced

Long-running

Related links

[Request access to GPT-Rosalind](https://openai.com/form/life-sciences-access/)

## Best for

- Target prioritization questions that need more than one evidence family, such as genetics, cohort replication, disease context, clinical precedent, literature, and expression.
- Teams that want Codex to perform scientific research across multiple evidence lanes, then reconcile the results into one conclusion.
- Scientists who want saved raw payloads, an explicit scoring rubric, and visuals they can reuse in the next review or decision memo.

## Skills & Plugins

- [Life Science Research](codex://plugins/life-science-research@openai-curated)

  Search scientific databases and literature to ground pathway, translational, tractability, and competitive evidence.

| Skill | Why use it |
| --- | --- |
| [Life Science Research](codex://plugins/life-science-research@openai-curated) | Search scientific databases and literature to ground pathway, translational, tractability, and competitive evidence. |

## Starter prompt

Use the Life Science Research plugin to compare TSLP, IL33, and IL1RL1 for asthma target prioritization.
Run these independent lanes in parallel with subagents:
- Human genetics and GWAS: gwas-catalog-skill, opentargets-skill, gnomad-graphql-skill
- Cohort replication and PheWAS: finngen-phewas-skill, ukb-topmed-phewas-skill, biobankjapan-phewas-skill, tpmi-phewas-skill
- Target-disease evidence and disease context: opentargets-skill, efo-ontology-skill
- Clinical and regulatory precedent: clinicaltrials-skill, opentargets-skill, chembl-skill, pharmgkb-skill
- Literature and public-dataset context: ncbi-entrez-skill, ncbi-pmc-skill, biorxiv-skill, ncbi-datasets-skill, biostudies-arrayexpress-skill
- Expression and tissue/cell-type context: human-protein-atlas-skill, gtex-eqtl-skill, cellxgene-skill, bgee-skill
For each lane:
- score TSLP, IL33, IL1RL1 on a 1-5 scale
- keep direct asthma evidence separate from adjacent allergic/atopic phenotypes
- save raw payloads when helpful
Then synthesize:
- a lane-by-target score table
- a final rank of TSLP, IL33, IL1RL1
- a confidence assessment and the main caveats
- two visuals: a prioritization heatmap and a GWAS summary figure with the lead asthma-linked variants for each target

Open in the Codex app

Use the Life Science Research plugin to compare TSLP, IL33, and IL1RL1 for asthma target prioritization.
Run these independent lanes in parallel with subagents:
- Human genetics and GWAS: gwas-catalog-skill, opentargets-skill, gnomad-graphql-skill
- Cohort replication and PheWAS: finngen-phewas-skill, ukb-topmed-phewas-skill, biobankjapan-phewas-skill, tpmi-phewas-skill
- Target-disease evidence and disease context: opentargets-skill, efo-ontology-skill
- Clinical and regulatory precedent: clinicaltrials-skill, opentargets-skill, chembl-skill, pharmgkb-skill
- Literature and public-dataset context: ncbi-entrez-skill, ncbi-pmc-skill, biorxiv-skill, ncbi-datasets-skill, biostudies-arrayexpress-skill
- Expression and tissue/cell-type context: human-protein-atlas-skill, gtex-eqtl-skill, cellxgene-skill, bgee-skill
For each lane:
- score TSLP, IL33, IL1RL1 on a 1-5 scale
- keep direct asthma evidence separate from adjacent allergic/atopic phenotypes
- save raw payloads when helpful
Then synthesize:
- a lane-by-target score table
- a final rank of TSLP, IL33, IL1RL1
- a confidence assessment and the main caveats
- two visuals: a prioritization heatmap and a GWAS summary figure with the lead asthma-linked variants for each target

[
Your browser does not support the video tag.
](https://cdn.openai.com/devhub/codex-use-cases/Target%20Prioritization%20Demo_es8.mp4)

## Leverage skills

The [Life Science Research plugin](https://github.com/openai/plugins/tree/main/plugins/life-science-research)
includes skills for each evidence lane:

- Human genetics and GWAS: `gwas-catalog-skill`, `opentargets-skill`, `gnomad-graphql-skill`
- Cohort replication and PheWAS: `finngen-phewas-skill`, `ukb-topmed-phewas-skill`, `biobankjapan-phewas-skill`, `tpmi-phewas-skill`
- Target-disease evidence and disease context: `opentargets-skill`, `efo-ontology-skill`
- Clinical and regulatory precedent: `clinicaltrials-skill`, `opentargets-skill`, `chembl-skill`, `pharmgkb-skill`
- Literature and public-dataset context: `ncbi-entrez-skill`, `ncbi-pmc-skill`, `biorxiv-skill`, `ncbi-datasets-skill`, `biostudies-arrayexpress-skill`
- Expression and tissue/cell-type context: `human-protein-atlas-skill`, `gtex-eqtl-skill`, `cellxgene-skill`, `bgee-skill`

Use these skills by mentioning them specifically, or let Codex decide when to use them.

## Step-by-step guide

1. Start with a concrete comparison question and the exact targets, disease, and evidence lanes you want Codex to cover.
2. Invoke the `Life Science Research` plugin and tell Codex to run the lanes in parallel with subagents so each evidence family stays bounded.
3. Ask Codex to score each lane on a fixed 1-5 scale and to keep direct disease evidence separate from adjacent phenotypes.
4. Review the saved raw payloads, the lane-by-target score table, and the synthesized rank in the same thread.

## Related use cases

[![](/codex/use-cases/scrna-seq-post-count-qc.webp)

### Annotate scRNA-seq data

Use Codex with the NGS Analysis plugin to turn a 10x-style matrix bundle into QC-filtered...

Sciences  Data](/codex/use-cases/scrna-seq-post-count-qc)[![](/codex/use-cases/bulk-rna-seq-fastq-qc.webp)

### Validate bulk RNA-seq inputs

Use Codex with the NGS Analysis plugin to validate sample sheets, FASTQs, and references...

Sciences  Data](/codex/use-cases/bulk-rna-seq-fastq-qc)[![](/codex/use-cases/discover-protein-folding-architectures.webp)

### Discover protein folding architectures

Use Codex with Goal Mode to research and implement novel architectural modifications to...

Sciences  Engineering](/codex/use-cases/discover-protein-folding-architectures)

