# Withdraw legacy decks — prepared 2026-10-04

This is a manifest-only hiding change, generated from the live course manifest. All nine modules keep their live reading and lab bundles. New Trees draft assets are not included. Upload the files under sicp-python/ to those same R2 keys; deploy the prepared viewer labId support to open labs directly. The nine small lab HTML pages also preserve access on the older viewer via an explicit link to /labs/<bundle-id>.

No production upload was performed: Cloudflare credentials are unavailable in this local checkout. Existing public slide/audio assets have not been deleted; a bookmarked direct deck or CDN URL can still open them. Hiding course-page links does not revoke access to public assets.

For subsequent course publication, reapply tools/hide_legacy_decks.py before uploading a newly generated manifest, until the original decks have been replaced. Standard generation currently infers decks from built bundles and would otherwise restore them.

Quality backlog: 16/31 legacy exercises pass untouched starters, including module 1's first two. Module 8's equality exercise accepts always-True methods. Slides include mangled identifiers, invalid generator formatting and clipped code; modules 4–9 have unrelated channel outros and 13 slides end on unanswered questions. The seven-hour estimate is removed rather than replaced with another unmeasured estimate. Legacy LabModeView has no hints or solution controls (source-confirmed; browser confirmation pending). Address these one module at a time; hiding does not fix legacy reading/lab correctness.
