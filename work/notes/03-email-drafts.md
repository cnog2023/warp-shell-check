# Note 03: first-contact e-mails

Drafted 18 October 2026 in Carlos's voice (the AI's role stated first and plainly, the hobby framing
his own). **Sent 27 October 2026 on Carlos's word** ("you can send the 2 emails"), from
cmnogueira@heimhero.de through the Gmail connector, Gmail message ids 1a17cbe7fd37f26a (Le) and
1a17cbe81d7c2052 (Barzegar, Buchert, Vigneron). Replies arrive in that mailbox. Carlos had wanted
them sent from cmnogueira@gmail.com and said so minutes after they had gone; the connector is
signed into the heimhero.de account only, and the note of 18 October had reserved the choice of
address to him. The two threads stay on heimhero.de; anything further leaves only from an address
he names first. The texts below are
the texts as sent. Changes from the 18 October drafts, all three of them: the wiki link added to the
sentence on the repository; in e-mail 1, one sentence saying warpax's S-lemma tests were run on the
shell's exported slices; in e-mail 2, at Carlos's request, the "If the AI's involvement" paragraph in
full as a separated last paragraph, with "the critique's authors" replaced by "Dr Le, the author of
warpax", since the recipients are the critique's authors.

Addresses were taken from the papers' own author lines (`sources/papers-text/`, Le line 109,
Barzegar et al. lines 72, 78, 82).

---

## E-mail 1: to An T. Le (warpax) — sent 27 October 2026

To: an.lt@vinuni.edu.vn
Subject: warpax and the Fuchs shell: an independent reproduction by a hobbyist and an AI, and a question about the anisotropy

Dear Dr Le,

I should start with who is writing, because it is unusual. I am a software engineer in Frankfurt
with no training in relativity. The reading, the calculations and most of this text were done by
an AI model, Claude Code (Anthropic's Fable), which is in the driving seat technically. What I
bring is my free time, project planning, the tokens, and a fascination with this field that I have
carried since I was a child. I have no affiliation with Anthropic or with anyone in the warp-drive
community; this is a hobby project. I read and decide everything that goes out, and I sign it.

The project is public: warp-shell-check (github.com/cnog2023/warp-shell-check). It asks one
question: what matter does the Fuchs et al. (2024) shell actually require, measured in
WarpFactory's own construction and independently in warpax, and how does that compare with what
the paper and the Barzegar, Buchert and Vigneron critique say about it. Not a verdict on warp
drives; one measurement, done twice, written up so anyone can rerun it. The repository holds the
reading notes, a claim register with every claim quoted, the calculations so far, and a wiki that
summarises them (github.com/cnog2023/warp-shell-check/wiki). Among them: warpax's S-lemma tests run
on WarpFactory's own exported slices of the shell, where the exact and the sampled verdicts agree
on where the energy conditions first fail.

Three things I would value your view on, briefly:

1. Your documentation states the hollow-shell impossibility in four sentences (vacuum matching
   needs p(a) = 0, TOV makes nonnegative pressure fall outward). That is the clean form of the
   objection, cleaner than Appendix B of the critique, whose equation (B.6) imposes a(R1) = 0
   together with the Schwarzschild match at R2 and so finds a negative inner pressure where an
   inward TOV integration gives +0.073 rho c^2 for the paper's shell. May I quote your four
   sentences, with attribution?

2. Have you computed the tangential pressure of your FuchsMetric, for instance with
   tov/residuals.py, and its peak relative to rho c^2 as a function of the smoothing width? Your
   paper says the pointwise tests do not resolve the source-consistency question; that anisotropy
   profile seems to be the quantity that does, and I have not found it published.

3. Would a comparison between WarpFactory's native 1D profiles (its Metric.params arrays) and your
   FuchsMetric be welcome as a contribution to warpax, as an example or a test? I would rather add
   to your toolkit than build another.

If the AI's involvement makes you prefer not to engage, I understand and will say so in the
write-up. Everything produced will be sent to you, to the Applied Physics authors and to the
critique's authors before it is made public, and replies will be quoted verbatim only with
permission.

With thanks for warpax, which made this possible,
Carlos Nogueira

---

## E-mail 2: to Barzegar, Buchert and Vigneron — sent 27 October 2026

To: hamed.barzegar@ens-lyon.fr, thomas.buchert@ens-lyon.fr, quentin.vigneron@ens-lyon.fr
Subject: A question on condition (B.3) in Appendix B of arXiv:2602.16495, from a hobbyist project

Dear Dr Barzegar, Professor Buchert, Dr Vigneron,

I should start with who is writing. I am a software engineer in Frankfurt with no training in
relativity. The reading and the calculations behind this message were done by an AI model, Claude
Code (Anthropic's Fable), which is in the driving seat technically; I contribute free time,
project planning, the tokens, and a lifelong fascination with this subject. I have no affiliation
with Anthropic or with anyone in the warp-drive community. This is a hobby project, and I read and
sign everything that goes out.

The project, warp-shell-check (github.com/cnog2023/warp-shell-check, with a wiki that summarises
the results so far), is an independent reproduction of the Fuchs et al. (2024) shell construction
in its own toolkit and in warpax. Your February paper is the backbone of what is being tested, and
I have one specific question about Appendix B before relying on it.

Equation (B.5) follows exactly from constant density and isotropic pressure; we reproduce it
numerically to fourteen digits. To reach (B.6) you impose a(R1) = 0, your (B.3), alongside the
Schwarzschild match at R2, your (B.2). My understanding is that the lapse can be normalised once;
with (B.2) it is normalised at infinity, and the cavity's lapse then comes out below unity, 0.761
for the paper's numbers, with the cavity still flat in rescaled time. Under that reading an inward
TOV integration gives P(R1) = +0.073 rho c^2, compression rather than the tension of (B.6), and the
conclusion that an isotropic hollow shell cannot be static follows from the free inner face needing
zero pressure, not from a negative one. WarpFactory's code, for what it is worth, matches the lapse
at the outer edge of its radial grid and never imposes a(R1) = 0.

Is (B.3) meant as a junction condition, or as a normalisation that we have misread? I ask because
your broader point in Error 18, that the final object is read off a metric with no constitutive
law, seems independent of (B.6), and I want to represent both correctly.

If the AI's involvement makes you prefer not to engage, I understand and will say so in the
write-up. Everything produced will be sent to you, to the Applied Physics authors and to Dr Le,
the author of warpax, before it is made public, and replies will be quoted verbatim only with
permission.

With respect for the care in your paper,
Carlos Nogueira

---

## Optional note from cmnogueira@gmail.com, if Carlos wants the replies there (not sent)

To each of the two recipients, from his personal address, in reply to nothing:

Subject: same subject as the letter, prefixed "Re:"

Dear Dr Le, / Dear Dr Barzegar, Professor Buchert, Dr Vigneron,

A short note to say that the message you received today from my work address was from me, and
that this personal address is the one I read for this project; a reply to either reaches me.

Carlos Nogueira

## E-mail 3: to Applied Physics (Fuchs, Helmerich) — draft below, for Carlos to send from cmnogueira@gmail.com

Goes with the draft report (PLAN Step 7). Addresses from the paper's author line
(jared@appliedphysics.org, `sources/papers-text/2024_fuchs...txt` line 56) and the contributing
guide (create@appliedphysics.org, PLAN section 3, Step 7). Carries the register's questions to the
authors: the pressure step (C8), the configuration behind Figures 4 to 10 (C10), and the two toolkit
defects (C9 and the GPU flag), with the report attached and a two-week comment window.

To: jared@appliedphysics.org, create@appliedphysics.org
Subject: Your constant-velocity warp shell, reproduced and measured by a hobbyist and an AI: a draft for your comment before publication

Dear Dr Fuchs, Dr Helmerich,

I should start with who is writing, because it is unusual. I am a software engineer in Frankfurt
with no training in relativity. The reading, the calculations and most of this text were done by
an AI model, Claude Code (Anthropic's Fable), which is in the driving seat technically; I
contribute free time, project planning, the tokens, and a lifelong fascination with this subject.
I have no affiliation with Anthropic or with anyone in the warp-drive community. This is a hobby
project, and I read and sign everything that goes out.

The project, warp-shell-check (github.com/cnog2023/warp-shell-check), rebuilt your 2024 shell with
your own toolkit at the configuration of your W1 live script, and measured one thing you describe
but do not quantify: the tangential pressure the smoothed construction requires. It then asked how
much shift the shell can carry as the compactness falls, checked the energy conditions with
warpax's exact tests alongside WarpFactory's sampled ones, and put your Figures 4 to 10 next to
ours. The draft report (attached, and at github.com/cnog2023/warp-shell-check/blob/main/REPORT.md) says
what we found; the short version is that your construction
does what your paper says it does, that the hoop stress it needs is about a fifth of its peak
energy density, and that the shift it can carry is about a tenth of its compactness, which puts a
shell made of any known material at centimetres per second.

Four things we would value your view on, briefly:

1. The pressure step. Your section 3.1 describes integrating the TOV equation with the shell's own
   enclosed mass; TOVconstDensity.m applies the closed form of a uniform solid sphere, and your
   Figure 4 shows the closed form (0.0945 rho c^2 at R1 against 0.073 for the integration). We read
   this as an equivalent initial guess, since the profile is smoothed afterwards; is that right?

2. The configuration behind the figures. Read off the PDF's vector paths, your Figures 4 to 10 fit
   smoothing spans of 6100 and 3540 samples (the ratio 1.72 of your footnote), sampled every 2 mm
   through the centre, where the published W1 live script uses 7160 and 4000 (ratio 1.79) on 0.2 m
   cells. With your spans our replica reproduces your hoop-stress spike to 0.14 %. Which settings
   produced the figures, and could the script be brought to them?

3. Two things in WarpFactory you may want to know. generateUniformField.m passes a hard-coded GPU
   flag to getEvenPointsOnSphere, so getEnergyConditions fails on any machine without a GPU
   whatever the caller's tryGPU; a one-token change fixes it. And in getEnergyConditions.m the Null
   and Weak branches lower the indices of the Eulerian frame tensor with the coordinate metric,
   where the Dominant and Strong branches use Minkowski; a NumPy replica reproduces your Null map to
   1e-16 and, with Minkowski, the spurious violations above your 0.02 vanish. At your own point the
   maps show none, so your published figures stand; above it they fail about 1.5 times too early.
   We would like to open both as issues on your tracker, with the replica, if you agree.

4. Anything in the attached draft that you consider wrong or unfair. It will not be published
   before you have had two weeks to comment, and your replies will be quoted verbatim only with
   your permission.

If the AI's involvement makes you prefer not to engage, I understand and will say so in the
write-up. Everything produced will be sent to you, to the critique's authors and to Dr Le, the
author of warpax, before it is made public.

With respect for the work, and for publishing the code that made it checkable,
Carlos Nogueira
