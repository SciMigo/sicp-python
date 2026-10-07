# Module 7 self-review — 2026-10-06

Ready for independent review as a draft; not published.

- Branch begins at reviewed main (716c688), one module in this PR.
- Lesson: about 2,223 prose words, nine executable Python blocks, two rendered comparisons, three predict blocks, proved invariant, six recap labels, three retrieval/defence questions, final Reference and licence section.
- Book examples retained: withdrawal, decrementer, independent closures versus aliases, shared/unshared mutable pairs. Exercises adapted from 3.1/3.2, 3.12, 3.3, 3.16/3.17 and 3.7. The Measure exercise observes supplied pair counters rather than requiring the learner to implement 3.17.
- Five runnable stub starters; all ten checks red untouched. All ten solution checks pass. Assert messages state expected versus observed data. Seeded histories, identities, saved operations, equal-valued credentials, repeated values, empties, exceptions and cyclic distinct counting covered.
- Five deliberately wrong implementations rejected: no count increment, unchanged append link, withdrawal from initial balance, invented measurement, incorrect forwarding operation. Not a security or anti-cheating boundary.
- Actual Google Chrome with CDN Pyodide: all five exercises Run, replay first/final frames, Check my work and question completion pass; mastery gating, embed and host-supplied loading pass; no page errors. All sixteen smoke screenshots inspected. Repeated affected browser flows after visual changes.
- Lesson at 1366 and 390 pixels, light and dark: no horizontal overflow. Body contrast 16.74/15.26; invariant contrast 15.20/11.76. Both figures inspected in both themes on phone; phone starter runs and editable functions appear first.
- Screenshot corrections: replaced misleading trace arrows with independent comparisons, labelled pair-identity count, identified measured strategies, added actual naive/distinct comparison frames, labelled mastery route-count/result cells. Added exception syntax before the lab requires handling rejected joins.

Estimate: lesson around 25 minutes (200 prose words/minute plus code and figure study); lab about 70 minutes; total 95 minutes. Unmeasured author estimate. Replay frames show real transitions; rejected requests deliberately preserve balance. Figure data and link text are checked independently of returned values.

Contract choices: monitor counts attempted calls even on exceptions; reserved query/reset strings are commands. Joint access adds a non-mutating boolean check request, explicitly identified as an adaptation. Sequential teaching account model; negative amounts, concurrent operations and production authentication are outside scope. Destructive append takes disjoint proper finite chains.

Publication work remains separate: publisher module list, reviewed asset publication and viewer registry entry. Course-wide tutor concepts/knowledge wiring is not claimed complete. Original book reading remains separate. No slides or narration added.

## 2026-10-07: fixes after review (Claude)

The conversion's content and checks were sound. Three things changed in substance.

- **Pictures of the structures.** Nothing drew a box-and-pointer structure: both lesson figures
  were text tables and the append exercise drew its links as text rows. The lesson now shows the
  two account frames, a chain after a destructive append, and the seven encounters of the naive
  pair counter as a tree. The append exercise draws real chains, with the visited pair
  highlighted and the `first` and `second` labels, before and after the link changes.
- **The pair counter is the learner's.** The Measure exercise asked only for a counting wrapper,
  for the fourth module running, while the supplied code held the answer to exercise 3.17. The
  learner now writes `count_pairs` by identity; the checks include two equal-content pairs, two
  cycles and a read budget. A recursive answer is accepted (the deep case is 150 pairs).
- **The mastery states behaviour, not design.** Its prompt said to forward operations to the
  parent service. It now says who must be able to do what; `run_access`, the event replay, is
  supplied, so the learner writes `connect`.

Smaller changes: the lesson recalls Module 2 for `make_withdraw` and `nonlocal` instead of
re-teaching them, shows `is` and `id()` before the traversal that needs them, fixes a
cross-reference to an example that does not exist, and claims SICP 3.1.1 and 3.1.3 (3.1.2 is
not covered). Prompts are split into paragraphs. A check now confirms that asking a monitor for
its count draws nothing. Exercise numbers are in the prompts, not the titles.

Verified: `lessons.py check 07` ok (10 blocks, 3 figures); `check_lab.py 07` ok (5 exercises,
10 solution checks); lab sources up to date; all 10 checks red on untouched starters; 14 wrong,
lazy and alternative submissions behave as expected; browser smoke with `--all` on Pyodide
0.27.4 from the CDN passes; lesson stays within 390 px. Looked at all three lesson figures and
the append exercise's first frame.

Estimate unchanged at 95 minutes, unmeasured.
