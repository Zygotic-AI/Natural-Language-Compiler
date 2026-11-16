# Natural Language Compiler hub v0.8.0

## Highlights

Hub **v0.8.0** is a minor on **v0.7.0**. This file is the notes for the release line. The git tag is not cut yet.

- **Lazy-load skills at install.** On an interactive terminal the installer asks `Lazy-load skills (disable-model-invocation)? y/N`. Enter, `n`, or any other answer writes `disable-model-invocation: false` on the skills this install copies. `y` or `yes` writes `true`. Piped install and CI do not ask and write `false`. Skills already in the folder that this install did not copy stay as they are.
- **Product story pack.** Feature narratives, operator flows, and the concept graph for the released and upcoming story are in this line.

## Changes since v0.7.0

- **Lazy-load skills at install.** Interactive install can mark the skills it copies as slash-only. The default remains auto-invoke. Piped install and CI do not ask.
- **Product story pack.** Feature narratives, operator flows, and the concept graph are in this line. Upcoming items stay upcoming.
