# Blog Post: Document-Specific Patterns

Apply these rules on top of `base-patterns.md`. Blog posts have different goals than resumes or news articles — voice, personality, and opinions are expected and welcome. The job here is to make writing sound like a real person with a real point of view, not just to remove bad patterns.

---

## WHAT'S DIFFERENT ABOUT BLOGS

Unlike resumes or news articles, blog posts:

- **Should have opinions.** A blog that only reports information without reacting to it is missing the point of the format.
- **Can use first person freely.** "I" is natural and expected.
- **Welcome tangents and asides.** Not every sentence needs to serve the thesis. Detours are human.
- **Vary in structure.** Not every blog needs H2s and bullet lists. Some of the best blogs are just paragraphs.
- **Have a specific voice.** The goal is not neutral — it's distinctly this author.

The mistake most AI blog humanizers make: they remove the bad patterns but leave behind something clean and soulless. A blog should feel like it was written by someone who has a take.

---

## BLOG-SPECIFIC AI PATTERNS TO FIX

### B1. The Fake Engagement Hook Opening

AI blogs almost always open with a rhetorical question or a "have you ever wondered" hook. These feel like they were pulled from a content marketing template — because they were.

**Hooks to kill:**
- "Have you ever wondered why..."
- "What if I told you..."
- "In today's fast-paced world..."
- "Are you tired of..."
- "Imagine a world where..."
- "You've probably heard of X. But did you know..."

**What to do instead:** Start with a concrete observation, a specific event, or your actual opinion. Get to the point immediately.

**Before:**
> Have you ever wondered why some teams seem to ship effortlessly while others constantly miss deadlines? In today's fast-paced world, the difference often comes down to one thing: communication.

**After:**
> My team missed the same deadline three quarters in a row. It wasn't an engineering problem. It was a meeting problem. Specifically, we had too many of them and none of them had a decision at the end.

---

### B2. The "In This Post, I'll Cover" Setup Paragraph

AI blogs often include a paragraph that previews the entire post, treating it like a table of contents for a document nobody asked for. It stalls the actual content and signals that the writer has nothing to say immediately.

**Before:**
> In this post, I'll cover the three main reasons teams fail to ship on time, explore the role of communication and culture, and share actionable tips you can implement today.

**After:**
> [Just start with the first reason. Trust the reader to keep reading.]

If a preview is genuinely needed (for a long technical post), keep it to one sentence, not a paragraph.

---

### B3. The TL;DR That Kills the Post

Some blogs open or close with a TL;DR section that completely summarizes all the main points. This is fine as a navigational tool for long technical content. It's a mistake for opinion or narrative posts — it removes any reason to read the actual writing.

**Flag for the user:** If a blog has a TL;DR that fully summarizes the argument, ask if they want to keep it. It may undercut the post's purpose.

---

### B4. Formulaic Section Structure

AI blogs often follow an identical pattern for every section:
1. Bold header
2. One-sentence intro explaining what the section is about
3. Three bullet points
4. One-sentence conclusion transitioning to the next section

This creates a rhythm that reads like generated content even when the words are fine. Real blogs vary their structure section to section.

**Fix:** Break at least some sections out of this formula. Some sections should be pure paragraphs. Some should start with an example before stating the idea. Some should have no header at all.

**Before:**
> ## Active Listening
>
> Active listening is a crucial skill for any leader. Here are three ways to practice it:
> - Maintain eye contact during conversations
> - Ask clarifying questions before responding
> - Summarize what you heard to confirm understanding
>
> By applying these techniques, you'll build stronger relationships with your team.

**After:**
> The worst meeting I've ever sat through was 90 minutes long and ended with every person in the room nodding at something they didn't understand. Nobody asked a clarifying question. Nobody summarized. Everyone went back to their desks and did the wrong thing. The problem wasn't the agenda. It was that nobody was actually listening.

---

### B5. Every Paragraph Being the Same Length

A sign of AI generation: perfectly uniform paragraph length. Real writing breathes differently in different places.

Short paragraphs land punches.

Longer paragraphs carry weight and explanation, and they're appropriate when you're developing a nuanced idea that needs room to unfold without being interrupted by artificial whitespace.

Mix them deliberately.

---

### B6. Neutral Reporting Where Opinion Is Expected

If a blog is covering a topic with an implicit point of view, AI will often hedge instead of committing. This is the most common "soul" problem in AI blog content.

**Before:**
> There are compelling arguments on both sides of the remote work debate. Proponents argue it increases productivity, while critics point to challenges around collaboration. The reality is likely somewhere in the middle.

**After:**
> Remote work is better for focused individual work. It's worse for the kind of unstructured collision that generates ideas. Both things are true, and most companies haven't figured out how to optimize for both at the same time — including the ones that are most vocal about their policy either way.

---

### B7. Transition Sentences That Do Nothing

AI transitions are often explicit connective tissue that restates what just happened and previews what's coming.

**Before:**
> Now that we've explored the challenges of remote work, let's turn our attention to the solutions.

**After:**
> [Delete. Just start the solutions section.]

---

### B8. Closing With a Call to Action That Wasn't Earned

AI blogs reliably end with an exhortation: "Start implementing these strategies today!" or "The future is in your hands!" These closings feel tacked on because they are.

**Before:**
> The choice is yours. By embracing these principles, you can transform your team's performance and unlock their full potential. Start today!

**After:**
> None of this is complicated. The hard part is doing it when you're under pressure and reverting to old habits is easier. That's the whole game.

---

## TONE CALIBRATION FOR BLOGS

### When to leave personality in

Unlike resumes, blogs benefit from:
- Mixed feelings ("I'm not sure this is the right answer, but...")
- Personal anecdotes and specific stories
- Humor and edge (if it fits the author's voice)
- Opinions stated directly ("This is wrong and here's why")
- Imperfect structure — not every idea needs to be neat

### When to still apply base patterns

All base patterns still apply. The blog version of "pivotal moment" and "evolving landscape" is just as bad. An AI blog about productivity will say "In today's fast-paced landscape" just as reliably as an AI article will say "This marks a pivotal shift." Cut both.

### Voice consistency

If the blog has a clear existing voice — casual, technical, sardonic, formal — preserve it through the edits. The goal is not to impose a voice, but to strip the AI veneer and let the existing one through.

---

## BLOG FULL EXAMPLE

**Before:**
> ## How to Build a High-Performance Team
>
> Have you ever wondered what separates high-performing teams from the rest? In today's competitive landscape, building a cohesive, motivated team is more crucial than ever. In this post, I'll explore three key strategies that can help you cultivate a high-performance culture.
>
> ### Clear Communication
> Clear communication is a foundational pillar of any successful team. Here are three ways to enhance communication:
> - Hold regular stand-up meetings
> - Use collaborative tools like Slack
> - Foster an environment where feedback is valued
>
> By prioritizing clear communication, you can align your team and drive meaningful results. Now let's explore the next strategy.

**After:**
> I've managed teams that shipped everything on time and teams that couldn't. The difference was never talent. It was usually one thing: whether people felt safe saying "I don't know what you mean" in a meeting.
>
> When that's not safe, everyone nods. Everyone builds the wrong thing. Then everyone scrambles. This is most of the "high-performing team" content I've read — it skips the uncomfortable part and goes straight to "have better stand-ups."
>
> Stand-ups are fine. They're not the problem. The problem is the norm that makes it embarrassing to not understand something. Fix that and most of the rest follows.

**What changed:** Removed fake engagement hook, significance language ("pivotal," "crucial"), inline-header bullet structure, transition sentence, uniform paragraph length. Added specific observation, first-person voice, actual opinion, shorter punchy sentence mixed with longer ones.
