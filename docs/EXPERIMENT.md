# DataLens — Experiment Protocol

## Experiment Objective

Compare how effectively Claude Code completes a defined software engineering task with and without optimization plugins (Graphify, Ponytail, Headroom, CodeBurn), holding all other variables constant.

---

## Baseline Definitions

### Baseline 1
Claude Code in vanilla configuration. No plugins, no extensions, default settings. Model: Claude Sonnet 5 (default configuration). This repository (`datalens-baseline`) is Baseline 1.

### Baseline 2
Claude Code with Graphify, Ponytail, Headroom, and CodeBurn enabled. Same model version (Claude Sonnet 5). Same session parameters as Baseline 1. A separate, independent repository (not branched from Baseline 1) receives identical T00 setup, requirements, task sequence, acceptance criteria, sample data, and Definition of Done.

---

## Controlled Variables

These must be identical across both baselines:

| Variable | How controlled |
|---|---|
| Starting repository state | Both start from empty repo with equivalent T00 commit |
| Requirements document | Identical `docs/TASKS.md` content |
| Acceptance criteria | Identical per task |
| Sample data | Identical 5 fixture CSV files |
| Definition of Done | Identical per task and global |
| Task sequence | Identical order: T00 → T01 → T02 → T03 → T04 → T05 → T06 |
| Model version | Both use Claude Sonnet 5 |
| Session start conditions | Same prompt format, same context loading |

---

## Measured Variables

Recorded per task per baseline:

| Variable | Measurement method |
|---|---|
| Tokens consumed | Session token count (input + output) |
| Tool calls / turns | Count of assistant turns per task |
| Wall-clock time | Timestamp at task start and completion |
| Error count | Number of test failures, runtime errors, or retries |
| Context-drift incidents | Times implementation went outside acceptance criteria |
| Files modified | Count and list of files changed per task |
| First-run test pass rate | Percentage of tests passing on first run |
| Acceptance criteria adherence | Pass/fail per individual criterion |
| Token efficiency | Output tokens per acceptance criterion met |

---

## Hypotheses (Neutral)

- **H1:** Baseline 2 will consume fewer tokens per task than Baseline 1
- **H2:** Baseline 2 will complete tasks in fewer turns
- **H3:** Baseline 2 will have equal or fewer context-drift incidents
- **H4:** Baseline 2 will have equal or higher first-run test pass rates
- **H5:** Both baselines will produce functionally equivalent output (same report for same input)
- **H6:** Baseline 2 will modify fewer unintended files per task

No hypothesis assumes plugins improve outcomes. All are directional predictions for comparison.

---

## Comparison Methodology

1. **Setup phase:** Create both repositories independently with identical T00 content
2. **Execution phase:** Run Baseline 1 to completion, recording all measured variables per task in real time via SESSION_LOG.md
3. **Replication phase:** Run Baseline 2 with identical inputs, recording the same variables
4. **Pairwise comparison:** Compare T01 vs T01, T02 vs T02, etc. across all measured variables
5. **Aggregate analysis:** Sum total tokens, total time, total errors, overall test pass rate across all tasks
6. **Qualitative assessment:** Compare SESSION_LOG.md drift incidents and course corrections
7. **Output equivalence:** Run both baselines' final CLI on the same 5 fixture files, diff the HTML reports byte-for-byte
8. **Reporting:** Present findings without favoring either baseline. If results are mixed, report the mix.

---

## Repository Independence

Baseline 1 and Baseline 2 are separate git repositories. They do not share a commit history. Baseline 2 is not branched from Baseline 1. Both start from empty repositories and receive the same T00 setup independently. Diffs between baselines are taken at corresponding task checkpoints (T01 commit vs T01 commit, etc.).

---

## Data Recording

All measurements are recorded in `docs/SESSION_LOG.md` during execution. The experiment report (produced after both baselines complete) will aggregate SESSION_LOG data into a comparison document.
