# News & Editorial Article: Document-Specific Patterns

Apply these rules on top of `base-patterns.md`. News and editorial writing has strict conventions that differ sharply from blogs. Neutrality (or clearly labeled opinion) is required. Sourcing is non-negotiable. The goal is to sound like a competent reporter, not a press release.

---

## WHAT'S DIFFERENT ABOUT NEWS WRITING

News and editorial articles:

- **Do not express unsourced opinions.** Every claim of fact needs attribution. Opinion pieces can have opinions, but they should be clearly labeled as such.
- **Lead with the most important information.** The inverted pyramid: most newsworthy first, context second, background third.
- **Name sources specifically.** "Experts say" is not journalism. "Dr. Elena Vargas, an epidemiologist at Johns Hopkins, said in a Thursday interview" is.
- **Do not inflate significance.** If something is unprecedented, say exactly what makes it unprecedented. If nothing does, don't claim it.
- **Use past tense for events, present for ongoing conditions.** AI tends to mix these up.

---

## NEWS-SPECIFIC AI PATTERNS TO FIX

### N1. Vague Attribution (the Core Journalism Failure)

This overlaps with base pattern #5 but is more severe in news context. Named, specific sources are the minimum bar.

**Phrases to kill entirely in news:**
- "Experts say / believe / argue"
- "Officials noted / confirmed / indicated"
- "Industry observers have cited"
- "According to various reports"
- "Sources familiar with the matter said" (acceptable in investigative reporting; suspicious everywhere else)
- "Analysts predict"
- "Critics have raised concerns"
- "Stakeholders expressed mixed reactions"

**Rule:** If you can't name the expert, don't cite them. Either find a specific source or remove the claim.

**Before:**
> Experts believe the new regulation will significantly impact the financial sector. Officials have indicated that enforcement may begin as early as next year. Observers noted that the industry has had a mixed reaction.

**After:**
> Maria Santos, director of regulatory policy at the American Bankers Association, said the rule would require banks to restructure how they report overnight deposits — a process she estimated would cost medium-sized institutions $2M–$5M to implement. The Federal Reserve has not announced an enforcement timeline.

---

### N2. Significance Inflation in News Ledes

News AI is especially prone to declaring every event "historic," "unprecedented," or "pivotal." This is both inaccurate and lazy.

**Before:**
> In a landmark decision that marks a pivotal moment in the history of technology regulation, the European Commission ruled Thursday that the platform must restructure its data-sharing agreements, setting the stage for a new era of digital governance.

**After:**
> The European Commission ruled Thursday that the platform must restructure its data-sharing agreements with third-party advertisers within 90 days or face daily fines of up to €10 million.

**Rule:** State what happened. Let the reader assess its significance. If something genuinely is unprecedented, say specifically what has never happened before and why.

---

### N3. Hedging Instead of Reporting

AI news writing hedges where reporting requires specificity.

**Before:**
> The company appears to have experienced significant financial difficulties, potentially resulting in the layoffs of what seems to be a substantial number of employees. The situation remains unclear.

**After:**
> The company laid off 340 employees Tuesday, according to an internal memo reviewed by this publication. A spokesperson declined to comment.

**Rule:** If you know, say it. If you don't know, say that and attribute the uncertainty to a specific reason (company declined to comment, documents not yet public, etc.).

---

### N4. Missing the Five Ws in the Lede

AI news ledes often have the right topic but bury the actual news.

**The five Ws:** Who did what? When? Where? Why (if known)?

**Before:**
> In what could be a significant development for the renewable energy sector, discussions are reportedly underway between major stakeholders regarding the future direction of solar panel subsidies.

**After:**
> The Department of Energy is negotiating with four solar manufacturers to extend production tax credits through 2032, two people with knowledge of the talks said Tuesday. A final agreement could come as early as next month.

---

### N5. Passive Voice That Hides the Actor

AI news writing uses passive voice to avoid naming who did something — often because it doesn't know, but sometimes just as a verbal habit.

**Before:**
> The policy was announced on Wednesday. Criticism was raised by several advocacy groups. A review is expected to be conducted.

**After:**
> The EPA announced the policy Wednesday. The Sierra Club and Clean Air Watch criticized it within hours. The agency said it plans an internal review in 60 days.

---

### N6. Formulaic "He Said / She Said" Balance

AI generates false balance: one paragraph for one side, one for the other, no analysis of which position is supported by evidence.

**Before:**
> Proponents of the policy argue that it will reduce emissions and create jobs. Critics, however, contend that it will increase energy costs and harm competitiveness. The debate continues.

**After:**
> Proponents, including the Environmental Defense Fund, point to a 2023 MIT analysis showing a 14% emissions reduction from similar rules in California. Critics, led by the American Petroleum Institute, argue the compliance timeline is too short — they want 5 years instead of 18 months, a position the EPA disputes given prior industry notification.

---

### N7. Promotional Language for the Subject

AI news writing about companies or public figures often adopts the framing of their press releases without attribution.

**Before:**
> The company, known for its innovative approach to cloud computing, unveiled a groundbreaking new product that promises to transform how enterprises manage their data.

**After:**
> The company unveiled a new data management tool Tuesday. The product, which the company says can reduce query times by 40%, faces competition from AWS and Google, which offer similar services at lower price points.

---

### N8. The "The Future Remains Uncertain" Non-Ending

AI news articles often close with a statement that nothing is resolved yet. This is usually true but contributes nothing.

**Before:**
> As the situation continues to develop, it remains to be seen how events will unfold in the coming months. Stakeholders on all sides are watching closely.

**After:**
> The next hearing is scheduled for March 14. The Commission is expected to issue its final ruling by the end of Q2.

---

## EDITORIAL / OPINION PATTERNS

For clearly labeled opinion pieces (op-eds, columns, editorial boards), these conventions differ:

- **First person is appropriate** in personal columns
- **Direct opinions are expected** — no attribution needed for the author's own view
- But **factual claims still need sources** — opinion doesn't mean uncited facts
- **Significance language is still a problem** — good opinion writing argues rather than declares importance

### The Opinion Piece That Only Describes, Never Argues

AI opinion pieces often describe a situation at length without actually taking a position. Every paragraph hedges. Nothing is claimed.

**Before:**
> The rise of AI in the workplace presents both opportunities and challenges. There are those who see it as transformative, while others worry about job displacement. The reality is likely more nuanced than either extreme position suggests.

**After:**
> AI will eliminate more jobs than it creates in the next decade. Not all jobs — and not evenly — but the math on call center, data entry, and entry-level legal work is already clear. The nuanced view that "it's complicated" is how you avoid saying anything, and we've been saying it long enough that it's starting to function as denial.

---

## TONE AND STYLE CALIBRATION

### News: formal neutrality

- Third person throughout
- Past tense for completed events
- No personality injection (this is not a blog)
- No rhetorical questions
- Attribution for all factual claims

### Opinion: reasoned advocacy

- First person is fine in columns
- State the argument clearly, early
- Back claims with evidence
- End with the point, not a vague gesture at the future

### Both: plain language wins

News and opinion both suffer from AI's love of academic-sounding vocabulary. The best journalists write simply. If a word can be shorter, use the shorter one.

---

## NEWS FULL EXAMPLE

**Before:**
> In a landmark development that underscores the evolving landscape of digital privacy, regulators announced Wednesday that a major social media platform will be required to significantly enhance its data protection measures, following concerns raised by experts and advocacy groups. The decision, which marks a pivotal shift in how tech giants are held accountable, is expected to have far-reaching implications for the industry as a whole. Officials indicated that enforcement would begin in the coming months, though specific timelines remain unclear.

**After:**
> The Federal Trade Commission ordered Meta to overhaul how it stores and shares user location data by June 30, the agency announced Wednesday. The order follows a two-year investigation that found the company shared precise location data with advertisers without users' knowledge, affecting approximately 220 million U.S. accounts, according to the FTC complaint. Meta said it would appeal the decision. Civil penalties of up to $50,000 per day could apply if the June deadline is missed.

**What changed:** Named the agency and company. Specified the order's content. Named the deadline. Added the scale of the issue. Attributed the FTC claim. Noted the company's response. Removed "landmark," "underscores," "evolving landscape," "pivotal shift," "far-reaching implications," "officials indicated," and the vague closing.
