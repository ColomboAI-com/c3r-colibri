# c3r-colibri

Evidence-gated C3R shadow integration for the [Colibri](https://github.com/JustVugg/colibri)
local inference runtime. Colibri remains the execution authority: this adapter parses
route/usage telemetry and records C3R recommendations, but never rewrites native routing.

## Compatibility pin

- upstream: `JustVugg/colibri`
- commit: `9d5d05de7f4ccf39840224ed295f292ab8aeb598`
- validated build target: `c/olmoe`

The pinned OLMoE engine compiles successfully under Ubuntu/WSL. Upstream currently
initializes route telemetry but does not emit OLMoE route records, so a real checkpoint
shadow qualification remains gated on an upstream-compatible instrumentation patch.
This repository does not mislabel a build check as a live deployment.

## Trace format

`<call> <row> <layer> <expert_id>:<gate> ...`

Run `python -m unittest discover -s tests` to validate strict parsing and shadow-only
authority behavior.

