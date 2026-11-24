# #143 pass 2 handoff - agreement

Source: Richard Pickett's decisions, 2026-11-24, on the #143 planit pass 1 GCA list (GCA 3). This file is binding input for planit pass 2.

## The agreement artifact is the echoed structured confirmation

- Before an amendment is applied, the agent echoes back in structured form exactly what it will change: the GCA item, the current text, the proposed text, and what the change triggers.
- The human confirms that echo. The echoed structure plus the human's confirmation is the agreement artifact. It is what the amendment commit points to.
- No signature is required. A plain yes from the human on the echoed structure is the agreement (Richard, 2026-11-22: plain chat yes counts; never ask him to sign).

## Session markers are metadata only

- Session markers (session ids, timestamps, chat or comment ids) are recorded as metadata next to the artifact.
- They are never the agreement on their own. A session marker with no echoed structure is not agreement.
- Known-bad: an amendment whose only evidence is a session marker or a bare "yes" with no echoed structure must fail.
