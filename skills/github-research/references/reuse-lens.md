# Reuse lens

Use this lens when the user wants code, a component, an implementation pattern, or a repository to integrate or adapt.

## Component contract

For each serious candidate, determine:

- the exact capability needed and what is out of scope;
- source files, modules, symbols, or service endpoints that implement it;
- inputs, outputs, state, error behavior, and extension points;
- runtime, language, build system, and supported platforms;
- required models, datasets, credentials, external services, databases, or hardware;
- test coverage and examples that exercise the target path;
- license and any materially different license for bundled models, data, binaries, or dependencies;
- security, privacy, and data-flow constraints relevant to the user's use;
- likely integration seams, conflicts, and replacement cost.

State the assumed host stack and production scope before estimating integration effort. If they are unknown, provide a conditional estimate for the most plausible baseline and identify which assumption changes it most.

Do not call an entire repository reusable when only a narrow component fits.

## Validation levels

- **R0 — Mentioned**: a repository or component name was found; the implementation is not located.
- **R1 — Located**: the relevant source, example, or entry point is identified.
- **R2 — Traced**: one decision-relevant vertical slice is followed from public entry point through the target behavior, dependencies, error boundary, and relevant tests, with no unresolved high-impact gap in that slice.
- **R3 — Reproduced**: the relevant path was run or tested in a representative minimal environment.

Describe R0–R1 results as leads, not validated reusable components. R2 supports a conditional integration decision. R3 is required only when runtime certainty matters and the user authorized the work needed to reproduce it.

## Decision labels

- **Reuse**: the component fits with limited integration work and acceptable constraints.
- **Adapt**: the core is useful but needs bounded modification.
- **Reference**: the design or implementation is informative, but direct integration is unsuitable.
- **Reject**: a disqualifier such as incompatible license, missing capability, excessive dependency, unmaintained path, or unclear provenance outweighs the benefit.

Use explicit reasons rather than a universal numeric score.

## Search and inspection

Search implementation vocabulary, imports, symbols, examples, tests, configuration keys, and dependency manifests—not just repository descriptions. Inspect the exact revision used for the conclusion.

When a repository is large, trace one decision-relevant vertical slice from public entry point through implementation and tests. Do not claim whole-project understanding from a few files.

Clone only when code search or raw access is insufficient. Use a temporary directory, avoid changing remotes or upstream state, and remove disposable clones when the investigation ends.

## Output

For each finalist, report:

```text
Component and repository:
What it supplies:
Source location and revision:
Validation level:
Contract and dependencies:
License/provenance constraints:
Integration estimate and main unknown:
Decision: Reuse | Adapt | Reference | Reject
```

If the user asked for an implementation plan, map the selected component to the user's architecture. Do not implement or modify external repositories unless that action is separately requested.
