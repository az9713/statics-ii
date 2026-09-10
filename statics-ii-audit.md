# Audit — `az9713/statics-ii` (Engineering Mechanics: Statics II)

## Auditor attribution and provenance

| Field | Recorded value |
|---|---|
| Auditor | **Devin**, an AI software engineering assistant built by **Cognition AI** |
| Role | Auditor of the repository, mathematical examples, teaching materials, and prose, within the scope and limitations recorded below |
| Devin version / build | Not exposed to this session or returned by the session metadata lookup; no version number can be verified |
| Model used | Devin, built by Cognition AI. The underlying model name, model version, and inference configuration are not exposed to this session or returned by the session metadata lookup |
| Audit date | 2026-09-10 (UTC) |
| Attribution added | 2026-09-10 (UTC) |
| Repository | [az9713/statics-ii](https://github.com/az9713/statics-ii) |
| Audited revision | [`846e5b1c291f9f972418da408d427d076cdf1580`](https://github.com/az9713/statics-ii/commit/846e5b1c291f9f972418da408d427d076cdf1580), on `main` at the time of the audit |
| Audit session | [Devin session dcea4a6e07534d49b51f7a0d3eb423b8](https://app.devin.ai/sessions/dcea4a6e07534d49b51f7a0d3eb423b8) |
| Requester | Simon (GitHub: `az9713`) |

### Prompt that triggered the audit

The request below is reproduced verbatim:

> audit the codebase not only for link/fragment/duplicate-ID checks, accessibility/HTML validity, spot-checking equations and worked solution, but also the quality of the teaching materials. this is supposed to be an advanced graduate class. assess the depth and scope of the materials, the writing prose ...

### Auditor signature

**Signed: Devin — built by Cognition AI — 2026-09-10 (UTC).**

This is a written attribution, not a cryptographic signature. The report below is preserved as originally delivered; adding this attribution and committing it does not constitute a new audit. Statements about an unchanged repository refer to the original audit, before this report was added.

---

Scope: 9 HTML pages (~42,000 words of prose, 376 rendered equations, 75 problems, 53 figures), `tools/package.py`, `verification.txt`, and the offline ZIP. Commit `846e5b1` on `main`.

**Headline:** the artifact is technically clean — zero broken links, zero duplicate IDs, zero HTML5 parse errors, and I found **no arithmetic or sign errors** in ~45 numerical results spot-checked across all five modules, including every worked value in Modules 4 and 5 and all five cumulative-final problems. The substantive finding is positioning: the content is a strong **upper-undergraduate / bridge-to-graduate** statics text, not an advanced graduate course. Accessibility issues are real but minor and confined to the aggregated and metadata pages.

---

## 1. Structure, links, HTML validity (verified)

| Check | Method | Result |
|---|---|---|
| Local links + fragments (all pages) | independent BeautifulSoup crawler | all resolve; no escapes from the package |
| Duplicate `id`s | independent scan | none |
| HTML5 parse errors | `html5lib` strict error list, all 9 files | **0 errors on every page** |
| External assets / scripts | scan | none; CSP `script-src 'none'`; MathJax pre-rendered to inline SVG |
| ZIP vs. repo bytes | entry-by-entry compare | identical, 11 entries |
| Published Pages bytes | SHA-256 vs. `verification.txt` | match |
| Repeatable packaging | re-ran `tools/package.py` | reproduces the archive |

Note: `html5lib` catches parse-level errors, not full Nu-validator conformance (e.g. ARIA misuse, obsolete attribute values). No network validator was run.

### Finding S1 — `tools/package.py` asserts hard-coded inventory counts (low, by design but brittle)
`expected = {'lecture':30,'reading':55,'problem':75,'figure':53,'mjx-container':376,'prop':15}` — any legitimate content edit fails with a bare `AssertionError` and no diff. It also validates only *self-consistency*, never correctness. Suggest printing the delta and treating counts as a warning plus a checked-in expected-counts file.

### Finding S2 — no CI (low)
The script is only ever run by hand. A 20-line GitHub Actions job running `python tools/package.py` on PRs would make the guarantees continuous.

---

## 2. Accessibility

Confirmed good: `lang="en"` everywhere; `<main>`, skip links, focus-visible styles on all module pages; **all 376 MathJax containers carry accessible labels** (0 unlabeled); every engineering figure has a `<figcaption>` and an `<svg role="img">` with `<title>`; `<details>`-based hints/solutions are native disclosure elements, so keyboard-operable.

| # | Finding | Severity | Evidence |
|---|---|---|---|
| A1 | `complete-course.html` has **6 `<h1>` elements** (one per module + page title), so the single-file textbook has no single document root in the outline | medium | full-page heading scan |
| A2 | **32 heading skips `h2 → h4`** in `complete-course.html`, all on "Problem N" and extension-problem headings | medium | heading scan |
| A3 | `about.html` and `audit-report.html` have **no `<main>` landmark and no skip link**, unlike the module pages | medium | landmark scan |
| A4 | **23 `<table>` elements without `<caption>`** (across index, complete-course, audit-report, modules) | low | table scan |
| A5 | 12 `<svg>` without title/label — **all are MathJax internals** inside labeled `mjx-container`s, i.e. not real failures | none | classified separately |

Not tested (requires a browser/AT): colour contrast, reflow at 320 px, print stylesheet, actual screen-reader announcement of the SVG math, `prefers-reduced-motion` behaviour of the animated figures (Fig. 4.10 etc.).

---

## 3. Mathematics and worked solutions (sampled, ~45 results)

I recomputed independently. **No errors found.** Representative checks:

- **M1** beam reactions, oblique load + couple, triangular distributed load, three-hinged portal, pliers mechanical advantage, toggle, lift-off condition, virtual-work check.
- **M2** \(m+r=2j\) determinacy vs. stability distinction; joints/sections results; zero-force members; tie force vs. truss height; sign convention (tension positive) held consistently.
- **M3** direction cosines, matrix equilibrium residuals, rank/conditioning discussion; SFD/BMD jumps at point loads and applied couples; overhang reactions and internal moments.
- **M4** slope-jump law \(H(s_R-s_L)=P\); \(H=Pab/(fL)\) (18 kN case, tensions 20.125 / 18.974 kN); tension-limited sag \(f\ge1.5435\) m; unequal supports \(H=90/7\) kN with reactions 45/7 and 60/7 kN; cable–beam correspondence \(Hd(x)=M_b(x)\) (36 kN·m both ways); prescribed-length \(f=\sqrt{2.04}\), \(H=21.004\) kN; parabola \(H=wL^2/8f=250\) kN, \(T_{\max}=269.258\) kN; catenary \(a=20\): sag 2.5525 m, \(T=22.5525\) kN, \(S=20.8438\) m; inverse catenary K4 root \(a=25.326487\) m with \(S=20.523737\) m, \(T=27.326487\) kN (and the naive-parabola 25 kN comparison is correctly signed).
- **M5** incline range \(-33.857\le P\le717.897\) N; optimal pull \(\tan\beta=\mu_s\), \(P_{\min}=185.70\) N, \(N=W/(1+\mu_s^2)>0\); tip-vs-slide thresholds and the \(b/2h<\mu_s\) criterion; ladder \(\mu\ge\frac12\cot\theta\), \(s_{\max}=3.705\) m; wedge \(P=W\tan(\alpha+\phi)=780.2\) N and self-locking extraction 45.7 N; capstan \(100e^{0.3\pi}=256.63\) N, \(\theta_{\min}=\ln10/0.25=9.2103\) rad (1.466 turns), fixed-sum torque \(\tau_{\max}=rS\tanh(\mu_s\theta/2)\); cumulative final P1–P5 all reproduce (7.5 kN cable, 12 kN·m peak, \(-\sqrt{13}/2\) kN diagonal with zero residuals, 19.2 kN cable thrust, 1038.20 N·m drum torque).

Conceptual correctness is likewise strong and unusually careful for this level:
- friction as an **inequality**, never auto-set to \(\mu N\);
- normal-resultant location bounded by nonnegative pressure without assuming a distribution;
- friction direction derived from *relative* velocity (the wedge kinematics proposition);
- the free-pulley counterexample to the capstan equation (Example 4, Lecture 29) — a genuinely good trap;
- explicit separation of determinacy / stability / admissibility / strength.

**Limitation:** this is sampling, not proof. Symbolic derivations were checked by reading, not by CAS; the remaining ~30 numerical results in Modules 1–3 were checked by inspection rather than recomputation.

---

## 4. Depth and scope vs. "advanced graduate class"

**Assessment: it does not reach advanced graduate level, and its own front matter doesn't claim to.** `index.html` states prerequisites as "introductory statics, vectors, algebra, trigonometry, and basic calculus" — a sophomore prerequisite set. Quantitatively:

- 60 of 75 problems are tagged **"Foundation problem · Apply the model, show the equations, then check feasibility."** Only 15 extension problems exist (5 conceptual, 5 derivational, 5 computational), one triple per module.
- ~42,000 words total ≈ 110 printed pages for a full course.
- Every problem ships with a hint and a full solution one click away; no unsolved problem set, no problem spanning multiple bodies and multiple pages, no open-ended modeling brief, no project.
- Assessments are self-scored on a 10-point rubric; the cumulative final is 5 problems, each solvable in 10–20 minutes.

**Topics a graduate structural-mechanics course would expect, absent here:** statically indeterminate analysis (force/flexibility and displacement/stiffness methods), compatibility and elasticity, energy and variational methods beyond one virtual-work exercise (Castigliano, complementary energy, principle of minimum potential energy), matrix structural analysis and FEM, limit analysis / plastic collapse mechanisms, buckling and stability of equilibrium, thrust-line and masonry/rigid-block statics, unilateral contact with friction as a complementarity problem (a natural, rigorous extension of the inequality framing the text already uses), cable elasticity and thermal effects, reliability/load-and-resistance factor reasoning, and any engagement with literature or design standards (there are **no scholarly references anywhere** — the 55 "readings" all point back into the text itself).

**Fair positioning:** an unusually rigorous *second* statics course — good for an advanced undergraduate cohort, a graduate bridge/qualifying-exam refresher, or a first module of a graduate program for students with non-structural backgrounds. Marketing it as an advanced graduate class would overstate it.

**What would actually raise the level** (in rough order of leverage):
1. Add an indeterminacy strand: flexibility method → matrix stiffness → conditioning/rank tied back to Module 3's spatial-truss discussion.
2. Recast the friction module's inequalities as an LCP/optimization problem (Coulomb cone, existence and non-uniqueness of solutions, Painlevé paradox) — this is where the current text is strongest and closest to graduate content already.
3. Add limit analysis: lower/upper-bound theorems, plastic hinge collapse of the frames from Module 1, thrust lines for arches.
4. Replace ~20 foundation problems with 6–8 multi-stage problems that require modeling choices, given no numbers, and are not solved in-page.
5. Add a reference apparatus (Coulomb, Heyman, Timoshenko, Bathe, Stewart on rigid-body contact) and at least one computational project with error/conditioning analysis.

---

## 5. Prose quality

Genuinely good: precise, plain, unhurried; every symbol is defined in a "Setup and symbols" block before use; assumptions are stated before results and re-stated when a result is used outside its derivation ("this conclusion is for the uniform vertical loading and equal supports specified here"). Voice is consistent across all 30 lectures. I found essentially no grammatical errors.

Weaknesses:

| # | Finding | Severity |
|---|---|---|
| P1 | Heavy boilerplate: the sentence "as the full companion chapter. Re-derive its displayed equations and reproduce each numerical check before moving on…" appears **30 times**; the "Foundation problem · Apply the model…" tag **60 times**; "Editorial continuation:" as a section heading **9 times** | low |
| P2 | 53 `figure-ref` paragraphs **repeat the entire figure caption verbatim** in the body text immediately before the figure that carries the same caption — doubles the text for sighted and AT readers alike; a short "see Fig. 4.7" would do | low |
| P3 | Five consecutive lectures titled "Coulomb Friction (cont.)" — the TOC carries no information about incline / tipping / ladder / wedge | low |
| P4 | Typo **"Pdf Vresion"** (Module 19 reading title), present in 6 places across `index.html`, `module-4.html`, `complete-course.html` | low |
| P5 | Greek letters spelled phonetically in running prose ("mu-s", "alpha", "theta") while the same symbols are typeset in the equations — inconsistent register, and unnecessary given MathJax is already inline | low |
| P6 | Frequent hedging boilerplate about idealization ("this is a teaching model, not a field-use rating") is correct but repeated past the point of usefulness | low |

---

## 6. Priority list

**Medium:** A1 (six `h1`s in the aggregated file), A2 (h2→h4 skips), A3 (missing `main`/skip link on `about.html` and `audit-report.html`), and the level claim (§4) — either retitle/reposition, or add the indeterminacy + limit-analysis + contact-complementarity strands.

**Low:** A4 table captions, S1 brittle count asserts, S2 no CI, P1–P6 prose.

**None found:** broken links, duplicate IDs, HTML parse errors, math errors, unlabeled equations or figures, remote asset leakage, secrets, local-path leakage.

## 7. Limitations of this audit

Mathematics was spot-checked (~45 of ~150+ numerical results) and read for conceptual soundness — this is not peer review. Accessibility was measured statically; no browser, screen reader, contrast, or print testing was done. No claim is made about the source syllabus this course is aligned to, nor about originality relative to it. No repository files were modified.
