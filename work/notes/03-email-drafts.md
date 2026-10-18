# Note 03: first-contact e-mails (drafts for Carlos to read, then send)

Rewritten 18 October 2026 at Carlos's request: the AI's role is stated first and plainly, the
hobby framing is his own, and the technical asks are unchanged. Both in Carlos's voice. Nothing is
sent until Carlos has read the final text and said so; he also chooses the sending address.

---

## E-mail 1: to An T. Le (warpax)

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
reading notes, a claim register with every claim quoted, and the first calculations.

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

## E-mail 2: to Barzegar, Buchert and Vigneron (pending Carlos's decision)

To: hamed.barzegar@ens-lyon.fr, thomas.buchert@ens-lyon.fr, quentin.vigneron@ens-lyon.fr
Subject: A question on condition (B.3) in Appendix B of arXiv:2602.16495, from a hobbyist project

Dear Dr Barzegar, Professor Buchert, Dr Vigneron,

I should start with who is writing. I am a software engineer in Frankfurt with no training in
relativity. The reading and the calculations behind this message were done by an AI model, Claude
Code (Anthropic's Fable), which is in the driving seat technically; I contribute free time,
project planning, the tokens, and a lifelong fascination with this subject. I have no affiliation
with Anthropic or with anyone in the warp-drive community. This is a hobby project, and I read and
sign everything that goes out.

The project, warp-shell-check (github.com/cnog2023/warp-shell-check), is an independent
reproduction of the Fuchs et al. (2024) shell construction in its own toolkit and in warpax. Your
February paper is the backbone of what is being tested, and I have one specific question about
Appendix B before relying on it.

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
law, seems independent of (B.6), and I want to represent both correctly. If the AI's involvement
makes you prefer not to reply, I understand. Whatever is published will be sent to you first.

With respect for the care in your paper,
Carlos Nogueira
