# Impact graph

**Summary**

The impact graph links goals to the code they call, so a review is a query over those links.

**Paragraph**

The impact graph records which goals call which parts of the system. It is the internal graph NLC uses to see what a change touches before it regenerates code. A review follows those links from a goal to the code that carries it. This is the map that makes code review and compliance review automatic: the question is a query over recorded links. The fuller trace, from a policy line through to the running check, comes later.
