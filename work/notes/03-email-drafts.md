# Note 03: first-contact e-mails (drafts for Carlos to send)

Both in Carlos's voice. Send the first now (approved 18 October 2026). The second waits for
Carlos's decision after reading `02-hollow-shell.md`. Replace nothing in square brackets without
checking it; there are none left on purpose.

---

## E-mail 1: to An T. Le (warpax)

To: an.lt@vinuni.edu.vn
Subject: warpax and the Fuchs shell: an independent reproduction, and a question about the anisotropy

Dear Dr Le,

I am a software engineer in Frankfurt and a curious outsider to relativity. Over the past weeks I
have been reading the warp-drive literature around WarpFactory, your February paper and warpax,
and the critique by Barzegar, Buchert and Vigneron. I should say up front that I do this together
with an AI assistant (Claude), which does the computing and the drafting; I read, decide and sign
everything, and I would rather you knew that than wondered.

I have started a small public project, warp-shell-check (github.com/cnog2023/warp-shell-check),
with one question: what matter does the Fuchs et al. (2024) shell actually require, measured in
WarpFactory's own construction and independently in warpax, and how does that compare with what
the paper and the critique say about it. Not a verdict on warp drives; one measurement, done
twice, written up so anyone can rerun it.

Three things I would value your view on, briefly:

1. Your documentation states the hollow-shell impossibility in four sentences (vacuum matching
   needs p(a) = 0, TOV makes nonnegative pressure fall outward). That is the clean form of the
   objection, cleaner than Appendix B of the critique, whose (B.6) imposes a(R1) = 0 together with
   the Schwarzschild match at R2 and so gets a negative inner pressure where an inward TOV
   integration gives +0.073 rho c^2 for the paper's shell. May I quote your sentences, with
   attribution?

2. Have you computed the tangential pressure of your FuchsMetric, for instance with
   tov/residuals.py, and its peak relative to rho c^2 as a function of the smoothing width? Your
   paper says the pointwise tests do not resolve the source-consistency question; the anisotropy
   profile seems to be the quantity that does, and I have not found it published.

3. Would a comparison between WarpFactory's native 1D profiles (its Metric.params arrays) and your
   FuchsMetric be welcome as a contribution to warpax, as an example or a test? I would rather add
   to your toolkit than build another.

Everything I produce will be sent to you, to the Applied Physics authors and to the critique's
authors before it is made public, and your replies, if you allow it, will be quoted verbatim.

With thanks for warpax, which made this possible,
Carlos Nogueira

---

## E-mail 2: to Barzegar, Buchert and Vigneron (pending Carlos's decision)

To: hamed.barzegar@ens-lyon.fr, thomas.buchert@ens-lyon.fr, quentin.vigneron@ens-lyon.fr
Subject: A question on Appendix B (condition B.3) of arXiv:2602.16495

Dear Dr Barzegar, Professor Buchert, Dr Vigneron,

I am a software engineer and an outsider to relativity, working with an AI assistant on an
independent reproduction of the Fuchs et al. (2024) warp-shell construction in its own toolkit and
in warpax (github.com/cnog2023/warp-shell-check). Your February paper is the backbone of what we
are testing, and I have one specific question about Appendix B before I rely on it.

Equation (B.5) follows exactly from constant density and isotropic pressure, and we reproduce it
numerically to fourteen digits. To reach (B.6) you impose a(R1) = 0, your (B.3), alongside the
Schwarzschild match at R2, your (B.2). My understanding is that the lapse can be normalised once;
with (B.2) it is normalised at infinity, and the cavity's lapse then comes out below unity (0.761
for the paper's numbers), with the cavity still flat in rescaled time. Under that reading an inward
TOV integration gives P(R1) = +0.073 rho c^2, compression rather than the tension of (B.6), and the
conclusion that an isotropic hollow shell cannot be static follows from the free inner face needing
zero pressure, not from a negative one.

WarpFactory's code, for what it is worth, matches the lapse at the outer edge of its radial grid and
never imposes a(R1) = 0.

Is (B.3) meant as a junction condition, or as a normalisation that I have misread? I ask because
your broader point in Error 18, that the final object is read off a metric with no constitutive
law, seems to me independent of (B.6), and I want to represent both correctly. Whatever we publish
will be sent to you first.

With respect for the care in your paper,
Carlos Nogueira
