# emmtyper - Emm Automatic Isolate Labeller

[![CircleCI](https://circleci.com/gh/MDU-PHL/emmtyper.svg?style=svg)](https://circleci.com/gh/MDU-PHL/emmtyper)
[![Coverage Status](https://coveralls.io/repos/github/MDU-PHL/emmtyper/badge.svg?branch=master)](https://coveralls.io/github/MDU-PHL/emmtyper?branch=master) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/emmtyper) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/emmtyper) ![PyPI](https://img.shields.io/pypi/v/emmtyper) ![PyPI - License](https://img.shields.io/pypi/l/emmtyper) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/emmtyper) ![Conda](https://img.shields.io/conda/pn/bioconda/emmtyper?label=bioconda) ![PyPI - Downloads](https://img.shields.io/pypi/dm/emmtyper) ![PyPI - Status](https://img.shields.io/pypi/status/emmtyper) ![GitHub issues](https://img.shields.io/github/issues-raw/MDU-PHL/emmtyper)

## Table of Content

- [emmtyper - Emm Automatic Isolate Labeller](#emmtyper---emm-automatic-isolate-labeller)
  - [Table of Content](#table-of-content)
  - [Background](#background)
    - [Inner workings](#inner-workings)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Brew](#brew)
    - [Conda](#conda)
  - [Usage](#usage)
    - [Example Commands](#example-commands)
  - [Result Format](#result-format)
    - [Short format](#short-format)
    - [Verbose format](#verbose-format)
    - [Visual format](#visual-format)
    - [Tags](#tags)
    - [Example outputs](#example-outputs)
  - [BLAST or PCR?](#blast-or-pcr)
  - [Authors](#authors)
  - [Maintainer](#maintainer)
  - [Issues](#issues)

## Background

`emmtyper` is a command line tool for emm-typing of _Streptococcus pyogenes_ using a _de novo_ or complete assembly.

By default, we use the U.S. Centers for Disease Control and Prevention trimmed emm subtype database,
which can be found [here](https://www2a.cdc.gov/ncidod/biotech/strepblast.asp).
The database is curated by Dr. Velusamy Srinivasan. We take this opportunity to thank Dr. Srinivasan for his work.

### Inner workings

The difficulty in performing M-typing is that there is a single gene of interest (`emm`), but two other homologue genes (`enn` and `mrp`), often referred to as `emm-like`. The homologue genes may or may not occur in the isolate of interest. When performing `emm-typing` from an assembly, we can distinguish betweeen one or more clusters of matches on the contigs. The best match for each of the clusters identified is then parsed from the BLAST results. Where possible, we try to distinguish between matches to the `emm` gene, and matches to one of the `emm-like` genes.

Possible arrangments:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_emm_

---->>>>>>>----

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_mrp_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_emm_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_enn_

---->>>>>>----->>>>>>------>>>>>>-----

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_emm_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_enn_

----->>>>>>------>>>>>>-----

## Requirements

- `blastn` ≥ 2.6 (tested on 2.9)
- `isPcr`
- `python` ≥ 3.6

## Installation

### Brew

```bash
brew install python blast ispcr
pip3 install emmtyper
emmtyper --help
```

### Conda

```bash
conda install -c conda-forge -c bioconda -c defaults emmtyper
```

## Usage

emmtyper has 2 workflows: directly BLASTing the contigs against the DB, or using isPcr to generate an _in silico_ PCR product that is then BLASTed against the DB. The BLAST results go through emmtyper's business logic to distinguish between `emm` and `emm-like` alleles and derive the isoolate M-type.

The basic usage of emmtyper is in the form of:

```bash
emmtyper [options] contig1 contig2 ... contigN
```

All the available options can be inspected with `emmtyper --help`. Options passed on to `blast` are tagged with `[BLAST]`, and those for `isPcr` are tagged with `[isPcr]`.

```bash
Usage: emmtyper [OPTIONS] [FASTA]...

  Welcome to emmtyper.

  Usage:

  emmtyper *.fasta

Options:
  --version                       Show the version and exit.
  -w, --workflow [blast|pcr]      Choose workflow  [default: blast]
  -d, --blast_db TEXT             Path to EMM BLAST DB  [default:
                                  /path/to/emmtyper/db/emm.fna]
  -k, --keep                      Keep BLAST and isPcr output files.
                                  [default: False]
  -d, --cluster-distance INTEGER  Distance between cluster of matches to
                                  consider as different clusters.  [default:
                                  500]
  -o, --output TEXT               Output stream. Path to file for output to a
                                  file.  [default: stdout]
  -f, --output-format [short|verbose|visual]
                                  Output format.
  --dust [yes|no|level window linker]
                                  [BLAST] Filter query sequence with DUST.
                                  [default: no]
  --percent-identity INTEGER      [BLAST] Minimal percent identity of
                                  sequence.  [default: 95]
  --culling-limit INTEGER         [BLAST] Total hits to return in a position.
                                  [default: 5]
  --mismatch INTEGER              [BLAST] Threshold for number of mismatch to
                                  allow in BLAST hit.  [default: 4]
  --align-diff INTEGER            [BLAST] Threshold for difference between
                                  alignment length and subject length in BLAST
                                  hit.  [default: 5]
  --gap INTEGER                   [BLAST] Threshold gap to allow in BLAST hit.
                                  [default: 2]
  --blast-path TEXT               [BLAST] Specify full path to blastn
                                  executable.
  --primer-db TEXT                [isPcr] PCR primer. Text file with 3
                                  columns: Name, Forward Primer, Reverse
                                  Primer.  [default:
                                  /path/to/emmtyper/data/isPcrPrim.tsv]
  --min-perfect INTEGER           [isPcr] Minimum size of perfect match at 3\'
                                  primer end.  [default: 15]
  --min-good INTEGER              [isPcr] Minimum size where there must be 2
                                  matches for each mismatch.  [default: 15]
  --max-size INTEGER              [isPcr] Maximum size of PCR product.
                                  [default: 2000]
  --ispcr-path TEXT               [isPcr] Specify full path to isPcr
                                  executable.
  --help                          Show this message and exit.
```

Most of these options are self explanatory. The two expections are:

1. `--workflow`: choose between a `blast` only workflow, or a _in silico_ PCR followed by `blast` workflow. See below for more information.
2. `--clust_distance` defines the minimum distance between clusters of matched sequences on the contigs to generate separate `emm-type` calls for each clusters. Clusters of matches that are within the minimum `clust-distance` are treated as a single location match.
3. `--output_type` demonstrated below.

### Example Commands

```bash
# basic call using the blast workflow for a single contig file
emmtyper isolate1.fa
# basic call using the pcr workflow for all the .fa files in a folder
emmtyper -w pcr *.fa
# basic call changing some of the options for blast
emmtyper --keep --culling_limit 10 --align_diff 10 *.fa
# call using the pcr workflow changing some of the isPcr options and
# using the visual output format
emmtyper -w pcr --output-format visual --max-size 2000 --mismatch 5 *.fa
```

## Result Format

### Short format

emmtyper has three different result formats: `short`, `verbose`, and `visual`.

emmtyper by default produces the `short` version. This consists of five values in tab-separated format printed to stdout.

The values are:

- Isolate name
- Number of clusters: should be between 1 and 3, larger values could indicate contamination
- Predicted `emm-type`
- Possible `emm-like` alleles (semi-colon separated list)
- EMM cluster: Functional grouping of EMM types into 48 clusters

### Verbose format

The verbose result returns:

- Isolate name
- Number of BLAST hits
- Number of clusters: should be between 1 and 3, larger values could indicate contamination
- Predicted `emm-type`
- Position(s) `emm-like` alleles in the assembly
- Possible `emm-like` alleles (semi-colon separated list)
- `emm-like` position(s) in assembly
- EMM cluster: Functional grouping of EMM types into 48 clusters

The positions in the assembly are presented in the following format `<contig_number>:<position_in_contig>`.

### Visual format

The visual result returns an ASCII map of the `emm` and, if found any `emm-alleles`, in the genome. Alleles on a single contig are separated by "-", with each "-" representing 500bp. Alleles found on different contigs are separated with tab.

### Tags

The alleles can be tagged with a suffix character to indicate different possibilities:

| Tag | Description        | Additional Information                                    |
| --- | ------------------ | --------------------------------------------------------- |
| \*  | Suspect `emm-like` | Allele flagged in the CDC database as possibly `emm-like` |
| ~   | Imperfect score    | Match score below 100%                                    |

### Example outputs

Example for all result format:

Short format:

```
Isolate1	1	EMM65.0		E6
Isolate2	3	EMM4.0	EMM236.3*;EMM156.0*	E1
Isolate3	2	EMM52.1	EMM134.2*	D4
```

Verbose format:

```
Isolate1	6	1	EMM65.0	5:82168	E6
Isolate2	8	3	EMM4.0	2:104111	EMM236.3*;EMM156.0*	2:102762;2:105504	E1
Isolate3	5	2	EMM52.1	14:10502	EMM134.2*	5:913	D4
```

Visual format:

```
Isolate1	EMM65.0
Isolate2	EMM156.0*--EMM4.0--EMM236.3*
Isolate3	EMM52.1	EMM134.2*
```

## BLAST or PCR?

If you are not sure which pipeline to choose from, we recommend using `blast` first. The `blast` workflow is fast and works well with assemblies. You can then use the `pcr` mode if you wish to perform some troubleshooting.

For example, the `pcr` workflow might be useful when troubleshooting isolates for which emmtyper has reported more than 3 clusteres and/or too many alleles.

An important thing to note is that not all `emm-like` alleles can be identified by using by PCR typing. The `pcr` workflow can be used to test which hits would be returned if carrying out conventional M-typing using PCR. However, the workflow is not foolproof, as _in silico_ PCR will fail when one or both primers do not align in the same contig (i.e., the allele is broken across two or more contigs) or there are mutations in the primer sites. In the former case, this might be an indication of poor sequence coverage or contamination.

## Authors

- Andre Tan
- Torsten Seemann
- Jake Lacey
- Mark Davies
- Liam Mcintyre
- Hannah Frost
- Deborah Williamson
- Anders Gon&ccedil;alves da Silva

The codebase for `emmtyper` was primarly written by Andre Tan as part of his Master's
Degree in Bioinformatics. Torsten Seemann, Deborah Williamson, and Anders Gon&ccedil;alves da Silva provided supervision and assistance.

Hannah Frost contributed with EMM clustering by suggesting we incorporate it in to the code, and providing the necessary information to do so and test it.

Jake Lacey, Liam Mcintyre, and Mark Davies provided assistance in validating `emmtyper`.

## Maintainer

The code is actively maintained by MDU Bioinformatics Team.

Contact the principal maintainer at andersgs at gmail dot com.

## Issues

Please post bug reports, questions, suggestions in the [Issues](https://github.com/MDU-PHL/emmtyper/issues) section.
