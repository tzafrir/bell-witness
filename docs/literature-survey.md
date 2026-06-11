# Literature survey — the discriminator's standing (2026-06-10)
## VERDICT (decision tree outcome)
NO DIRECT BOUND EXISTS on L_exp — the dependence of the JOINT
(system-outcome, environment/ancilla-readout) statistics on a remote
party's setting. Every located experimental test is one of:
(a) MARGINAL no-signaling checks; (b) Bell-violation persistence under
frame scanning (speed-of-influence bounds); (c) inequality tests of
specific nonlocal-HV classes (Leggett). The observable in
translation-protocol.md is unmeasured. => The protocol note upgrades to
a PROPOSAL DRAFT.
## Map of adjacent constraints
1. MARGINAL NO-SIGNALING CHECKS ON BELL DATA.
   - Dedicated test on Hensen loophole-free data: arXiv:1606.00784 —
     checks p_A(x|a) independence of b; marginal conditions only.
   - Standard practice: two-proportion Z-tests on marginals (e.g.
     arXiv:2401.03505 Hardy loophole-free; arXiv:1807.09611 DIQRNG);
     p-value-level statements, no joint-with-ancilla quantity.
   - Apparent-signaling systematics: arXiv:1801.05739 (fair-sampling
     experiments show artifacts; loophole-free data clean at marginal
     level).
   - Frameworks for analyzing data WITH bounded signaling:
     arXiv:2602.05507 (Feb 2026); NS-projection-invariant inequalities
     arXiv:2511.06624. Marginal-level; useful for our statistics section.
2. HIDDEN-INFLUENCE (v-CAUSAL) MODELS — theoretical kin of T4 theorem.
   - Bancal, Pironio, Acin, Liang, Scarani, Gisin, Nat. Phys. 8:867
     (2012), arXiv:1110.3795: any finite-speed hidden-influence model
     reproducing quantum correlations enables superluminal SIGNALING in
     multipartite scenarios — "hidden mechanism becomes operational
     signaling," same logical shape as our T4 impossibility.
     DIFFERENTIATION: their axis is propagation speed in spacetime; ours
     is configuration-disturbance with accessible records, quantitative
     leak floors/scaling surfaces, environment-probe operationalization.
   - Multipartite NS stronger than relativistic causality:
     Nat. Commun. 10:1701 (2019).
   - Colbeck & Renner, PRL 101:050403 (2008): HV models for QM cannot
     have any local part — adjacent impossibility family.
3. SPEED-OF-INFLUENCE EXPERIMENTS (bound v-causal models, not L_exp).
   - Salart et al., Nature 454:861 (2008): 18 km east-west Bell test,
     >24 h; v > 1e4 c for privileged frames with Earth speed < 1e-3 c.
   - Yin et al., PRL 110:260407 (2013): loophole-improved version.
   - Tabletop variant: Sci. Rep. 13:8201 (2023).
   These bound propagation-style mechanisms; the shortcut is not a
   propagating influence, so these do NOT constrain the substrate class
   — but Bancal-type arguments may, via the T4 route (theory item).
4. LEGGETT-MODEL FALSIFICATIONS (different nonlocal-HV class).
   - Groblacher et al., Nature 446:871 (2007); Paterek PRL 99:210406;
     Branciard PRL 99:210407; Branciard Nat. Phys. 4:681 (2008).
   Exclude nonlocal models with specific marginal structure; no
   environment joints. Useful precedent for model-class-exclusion papers.
5. ENVIRONMENT-RECORD MEASUREMENT CAPABILITY (feasibility, not bound).
   - Quantum Darwinism experiments: photonic cluster states
     (arXiv:1803.01913), photonic simulator (arXiv:1808.07388) —
     fragment-resolved environment readout is demonstrated capability.
     None condition on a remote setting in a Bell configuration.
     The proposal = QD-style fragment readout x loophole-free Bell
     geometry.
## Why the substrate class survives all existing tests BY CONSTRUCTION
Z2-equivariance pins single-party marginals flat (phase 1), so marginal
NS checks pass; the shortcut is not finite-speed propagation, so
frame-scanning bounds do not apply; gadgets are not Leggett-structured.
The ONLY exposed surface is the joint-with-records observable — exactly
what the T4 theorem says cannot be hidden.
## Implications for the paper
- Position the T4 theorem as the records/environment analogue of Bancal
  et al.'s v-causal result (closest prior art; cite and differentiate).
- Novelty claim safe: b-conditioned joint (A,C) tables in a monitored-
  decoherence Bell configuration appear unpublished.
- Statistics section: adopt bounded-signaling frameworks (2602.05507,
  2511.06624).
- Residual risk: unindexed thesis/appendix with a passing joint
  analysis; mitigation = define the observable precisely and invite
  retrospective analyses of public loophole-free datasets.
## Next concrete step
Proposal v0: observable definition; QD-fragment x Bell-geometry
apparatus sketch; statistics plan (delta = 1e-2 at 1e4 trials/cell);
exclusion-surface translation (bridging surface); retrospective-analysis
appendix for existing public datasets.
[Status note added at mirroring time: the retrospective branch was
executed by this repository — clean pre-registered null, L_exp <~ 0.105
(95%), Delft pooled heralding channel. See results/RETRO_REPORT.md.]
