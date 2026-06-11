# The translation problem — from leak* to a laboratory protocol (working note v0.1)
## 1. The observable
For a Bell pair with wings A, B and an auxiliary system C that interacted
with the pair near the source (a "monitored decoherence ancilla"), define
    L_exp = max over a, over C-readouts of
            | E[A·C | a, b=0]  -  E[A·C | a, b=1] |
i.e. the dependence of the *joint* (A, C) statistics on Bob's setting, with C
measured spacelike-separated from Bob's choice.
## 2. The two predictions
**Quantum mechanics: L_exp = 0, exactly, always.** Bob's operation acts on his
tensor factor; it commutes with every observable of A⊗C. This is extended
no-signaling — a theorem, holding at every decoherence level.
**Substrate class (contractive, record⇒sever): L_exp > 0 whenever the pair
still violates Bell and C holds records of the shortcut micro-state.** In-model
magnitude for an optimal detector on records of half the shortcut: ~0.3 at
S ≈ 2.1 (leak law, 26σ confirmed). The leak hides in the joint: single
marginals P(A|a,b) and P(C|b) remain exactly flat (equivariance / Z2), so
standard marginal no-signaling checks see nothing. Only the joint analysis
detects it.
## 3. Why existing Bell tests likely don't bound this directly
Loophole-free Bell tests verify marginal no-signaling as a sanity check and
trace out the environment. The discriminator lives in a quantity they do not
report: b-conditioned (A, ancilla) joint distributions. Tripartite experiments
(GHZ, steering monogamy) come closest; whether any has published a precision
bound on c-invariance of two-party joints is the literature question (see §7).
## 4. Protocol sketch (photonic, near-term)
1. Polarization-entangled pair source; standard loophole-free geometry with
   fast random settings a, b.
2. On the source side, a *controlled* decoherence stage: a weak interaction
   entangling an ancilla photon (or atomic ancilla) with the pair before the
   wings separate — tunable strength φ, reducing S from ~2.8 toward 2 (this is
   the model's "partial severance" regime by construction: records exist AND
   violation persists).
3. Third detector measures the ancilla, spacelike from Bob's setting choice;
   several ancilla bases (the model's optimal detector is not known a priori —
   scan bases; the substrate effect is large enough that coarse scans suffice).
4. Report: S(φ) and L_exp(φ) with full b-conditioned (A, C) joint tables.
Statistics: bounding L_exp < δ needs ~δ⁻² trials per setting cell; δ = 10⁻²
is ~10⁴ trials per cell — trivial for modern sources. The model's in-family
effect (0.3 for an optimal detector; suppressed by record fidelity and
coverage for a realistic one) is detectable or excludable at modest cost.
## 5. The bridging function (in-model work required before proposing)
Map leak(η_cov, η_fid, S): leak as a function of the fraction of shortcut
recorded (η_cov), record fidelity (η_fid), and violation S. Then an
experimental null L_exp < δ at measured S translates into an exclusion region
in (η_cov, η_fid) for the substrate family — the exact analogue of coupling-
constant exclusion plots. This surface is a straightforward simulation
campaign on the existing harness.
## 6. The escape-hatch ladder (honesty section)
How the model retreats under a null result, and how far it can go:
- "The ancilla's records aren't the substrate's records" — partially valid:
  the map from graph spins to lab degrees of freedom is unspecified. BUT the
  record⇒sever rule makes severed records ordinary, dynamically accessible
  spins; if the ancilla causes the decoherence (it demonstrably reduces S),
  then *within the model* the ancilla holds severance records by definition.
  The retreat is limited to claiming lab decoherence is severance-without-
  accessible-records — which contradicts record⇒sever and reopens the axiom
  triad (no-cloning and severing split apart again). A null therefore forces
  a real cost somewhere in the axiom structure.
- "The optimal detector basis was missed" — quantifiable: the in-model leak
  is broadband across single-coordinate detectors (all 7 violators leaked in
  the first coordinate scanned); a moderate basis scan closes this.
## 7. Literature pass (to do, dedicated session)
Targets: precision bounds on setting-independence of two-party joints in
tripartite experiments; "event-ready"/heralded Bell tests with ancilla
analysis; monitored-decoherence entanglement experiments; collapse-model
tests (CSL bounds — different observable, possibly adjacent constraints).
Recommended as a deep-research run (20+ sources), not a single-search check.
## 8. Status
This note upgrades the discriminator from "in-principle" to
"protocol-shaped." Remaining before an actual proposal: §5 bridging surface,
§7 survey, and the leak envelope near S → 2⁺ (does the effect persist where
real partially-decohered pairs live, S ≈ 2.0–2.4 — current data says yes,
at full magnitude, but from one configuration).
[Status note added at mirroring time: §5, §7, and the envelope were
subsequently completed — see literature-survey.md and proposal-v0.html in
this directory; the archival arm (this repository) executed §7's
retrospective branch.]
