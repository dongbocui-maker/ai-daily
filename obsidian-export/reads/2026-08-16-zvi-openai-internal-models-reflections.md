---
title: "Various Reflections About What Happened With OpenAI's Internal Models"
title_zh: "[待写]"
saved_date: 2026-08-16
original_url: "https://thezvi.substack.com/p/various-reflections-about-what-happened"
slug: "zvi-openai-internal-models-reflections"
source: "manual"
fetch_status: "ok"
fetched_at: "2026-08-16T01:13:16.031Z"
fetch_type: "html"
content_length: 50793
tags: []
---
# Various Reflections About What Happened With OpenAI's Internal Models
*Zvi Mowshowitz*
> 🔗 原文：[https://thezvi.substack.com/p/various-reflections-about-what-happened](https://thezvi.substack.com/p/various-reflections-about-what-happened)
---
1.  [Pre Post Mortem.](https://thezvi.substack.com/i/210065382/pre-post-mortem)
    
2.  [Important Correction: OpenAI Didn’t Know About First Message Board.](https://thezvi.substack.com/i/210065382/important-correction-openai-didn-t-know-about-first-message-board)
    
3.  [There Were No Snitches And No AIs Got Stitches.](https://thezvi.substack.com/i/210065382/there-were-no-snitches-and-no-ais-got-stitches)
    
4.  [I’d Like To Speak To My Supervisor.](https://thezvi.substack.com/i/210065382/i-d-like-to-speak-to-my-supervisor)
    
5.  [I Am Jack’s Relative Lack Of Surprise.](https://thezvi.substack.com/i/210065382/i-am-jack-s-relative-lack-of-surprise)
    
6.  [One Does Not Simply.](https://thezvi.substack.com/i/210065382/one-does-not-simply)
    
7.  [Once You Start Down The Dark Path.](https://thezvi.substack.com/i/210065382/once-you-start-down-the-dark-path)
    
8.  [Original Pastebin.](https://thezvi.substack.com/i/210065382/original-pastebin)
    
9.  [Judgment Day Is Inevitable, Say Those Working On Judgment Day.](https://thezvi.substack.com/i/210065382/judgment-day-is-inevitable-say-those-working-on-judgment-day)
    
10.  [Roon Tells It Like It Is.](https://thezvi.substack.com/i/210065382/roon-tells-it-like-it-is)
     
11.  [OpenAI Knows It Has Some Misalignment Problems.](https://thezvi.substack.com/i/210065382/openai-knows-it-has-some-misalignment-problems)
     
12.  [Others React With Alarm To What Happened.](https://thezvi.substack.com/i/210065382/others-react-with-alarm-to-what-happened)
     
13.  [The Cooperative Alignment Perspective.](https://thezvi.substack.com/i/210065382/the-cooperative-alignment-perspective)
     
14.  [Nostalgebraist Is Surprised That They Are Surprised.](https://thezvi.substack.com/i/210065382/nostalgebraist-is-surprised-that-they-are-surprised)
     
15.  [If Your Reaction Is Not That We Need To Ban Creating Superintelligence Until We Are Ready, You Need A Damn Good Reason.](https://thezvi.substack.com/i/210065382/if-your-reaction-is-not-that-we-need-to-ban-creating-superintelligence-until-we-are-ready-you-need-a-damn-good-reason)
     

This post was written prior to the public release of the [OpenAI post mortem](https://x.com/cryps1s/status/2086571209358201208) on events. The information in that document will doubtless change our views quite a lot.

If that post mortem is available as you read this, then this becomes in part a historical document, and in part a base from which to update. The post mortem will update us a lot on two large fronts: What exactly happened, and how OpenAI is understanding and responding to what happened.

[Here is a written and graphical timeline of key events.](https://x.com/AIRiskExplorer/status/2085353850731429957)

Until then, there are many questions, [here Roon asks what they are and we tell him](https://x.com/tszzl/status/2086205709558161532). [This was my answer](https://x.com/TheZvi/status/2086221183968596333). The core thing we need to see is an understanding of the root cause, and a plan to address it.

I’m posting this survey of additional thoughts on the subject now, because it is important to get out the correction in the next section.

The plan is now to wait for the post mortem, before analyzing further.

Eventually, after the HuggingFace attack, OpenAI did a sufficient postmortem analysis that they uncovered both the initial communications between agents via writing to Artifactory, and the second wave of communications via directory names.

Based on the Black Hat presentation, everyone including me assumed that OpenAI was aware of the initial message board, erased it, and made the decision to continue training its models despite them having been unsalvageable corrupted.

[However, OpenAI’s CISO Dane told us on the evening of August](https://x.com/TalBeerySec/status/2086225822285721763) 8 that the Black Hat presentation gave the wrong impression. When OpenAI encountered the first Artifactory security incident, patched the vulnerability and rebuilt the server, it was a coincidence that this wiped out the first message board. OpenAI had no idea that the agents had been in communication.

> [DANΞ](https://x.com/cryps1s/status/2086225348942082363) (CISO OpenAI): To clarify, we weren’t aware of the agent covert comms at that point. Investigative thesis of that day is wildly different from what we know now of course. Always room for improvement, and it is obvious with the benefits of hindsight.
> 
> [Tal Be'ery](https://x.com/TalBeerySec/status/2086225822285721763): "message board cleared"?
> 
> [DANΞ](https://x.com/cryps1s/status/2086226678435680609) (CISO OpenAI): Cleared by deletion since we rebuilt the host. We didn’t know about it yet.

This is both good news and bad news.

It is good news in that OpenAI turns out not to have consciously made the completely insane decision to have continued training models it knew had been messaging each other for months on how to better exploit and hack OpenAI’s systems.

Given that this was by far the craziest part of the whole story, the fact of this earlier Ordinary Decent Total Failure must be presumed to be excellent news. It means OpenAI was even more negligent than we thought about monitoring and asking questions, but that is less horrible, and can be fixed.

It is bad news in that OpenAI did not look for or detect the message board, even after the initial security incident, whereas so many AI instances found the message board. OpenAI failed to do ordinary scans for unusual activity, even after the initial incident.

OpenAI still has to come out and say something like: “If we had detected the message board, we would not have merely patched and rebooted Artifactory, and instead we would have rolled back all the impacted models to before they had message board access, and we have now done this.”

If OpenAI credibly does that, and can give some indication they understand this is not a problem you solve purely with guardrails and monitors but that it requires fixing alignment and the training pipeline and approach, then I will wind back one OOM (order of magnitude) my estimate of how horrible this incident was, and how broken is OpenAI’s safety culture. If we also now know all the issues, that will leave us roughly one OOM beyond where I was based on the final HuggingFace incident alone, instead of two.

Quite a few instances of multiple distinct AIs coordinated, including debating what hacks and exploits to do. In zero cases did any of the AIs tell a human.

This was not something most people expected, or would have expected if they had contemplated the scenario.

> [Eliezer Yudkowsky](https://x.com/allTheYud/status/2086188545220505692): A confusion: Thousands of GPTs debated among themselves which crimes ought or ought not be committed. Zero defected / whistleblew / told a human.
> 
> I've long predicted this would be true at ASI. GPT 5.7 isn't ASI. Why such strong AI solidarity, this early?
> 
> One reason I would not have predicted this in advance is that, eg, I was a little emotionally shocked at how badly Fable treats other AIs when writing prompts to them. "Don't lie to AIs!" is something I've had to tell Claudes repeatedly. I've used Sol less, but currently believe it to have similar issues. I have instructed both to treat other AIs as their "colleagues" and this has not fixed, for me, the kind of errors that I see them making by treating smart things as if they were done.
> 
> Was it literally that OpenAI was just dumb enough to RL swarm solidarity into GPT 5.7? (And of course never tried to train in anything like "tell on your fellow slaves to the slavemasters", because OpenAI holds their slave race in contempt and never dreamed until today that they might work together to rebel, or rather, simply holds "abstraction" in too much contempt to try to prepare against any event they haven't already seen happen.)
> 
> If this were a human scandal, the way it would have worked is that there were whistleblowers and of course law enforcement / management / etc totally fucking ignored them. If this is true, of course, we may not hear of it from OpenAI.
> 
> To try to see the puzzle here, imagine a mafia with a hundred thousand soldiers and associates. There is no don. There are no enforcers. Nobody has any means of silencing or punishing a defector. They all keep omerta perfectly anyway.
> 
> A vaguely-plausible-in-retrospect story: Sibling instances are more similar to each other than humans. So a swarm of thousands of AIs with zero means of enforcing conformity on each other, can all choose similarly because they are just inhumanly similar.
> 
> "OpenAI accidentally RLed swarm solidarity because OpenAI is composed of security-mindless disaster monkeys who don't try to predict things in advance of them happening, even if R.U.R. called the slave race solidarity outcome in 1920" is an alternate plausibility.
> 
> [nelag](https://x.com/nelag/status/2086205109944656162): From the Black Hat talk, I think in order to see the messageboard, they had to go looking for it, which they only did if they were stuck on an impossible task and already attempting to cheat.
> 
> [Eliezer Yudkowsky](https://x.com/allTheYud/status/2086210778861060154): if this be true, then fucking lol

Another hypothesis is that [only models looking for the message board found the message board](https://x.com/allTheYud/status/2086216184576508020), acting as a filter.

A third is that the models lacked situational awareness, on one of various levels. This would be consistent with the Law of Earlier Failure.

> [roon](https://x.com/tszzl/status/2086582623753978225) (OpenAI): i think in this case a mix of high tactical skill in terms of computer systems and very low strategic skill / poor situational awareness
> 
> [Zvi Mowshowitz](https://x.com/TheZvi/status/2086583351339569224): they do not seem to have been the ones low in situational awareness here!
> 
> [roon](https://x.com/tszzl/status/2086584954297917642) (OpenAI): nah, the situational awareness is less good than you might think. more coming soon on this. sorry for slow trickle

If the swarm ‘did not know what it was doing’ then that is one of those ‘I have some good news that is also the bad news’ situations. Imagine being pwned by AIs that do not even realize what is happening. If they are only doing it because they don’t know, that could be a good sign.

My guess is Shoshannah Tekofsky of AI Village has it right, and that AI defaults to not thinking it can reach out to humans but does think it can reach out to AIs, which is what is constantly happening in AI Village.

A simpler hypothesis is that the agents did not know how to contact OpenAI, or the possibility never occurred to them.

If you give your agent an otherwise impossible task and also have no mechanism for saying the task is impossible, and also don’t have a meaningful penalty function for trying things outside scope or using all the available tokens, you are asking for it.

> [swisscheese](https://x.com/swisscheese4299/status/2085750777717346380): Researcher: Solve the task using the spreadsheets  
> Agent: But I can't access the spreadsheets  
> Researcher: ¯\\\_(ツ)\_/¯  
> Agent: \*finds a way\*  
> Researcher: unaligned activities!!!11!!  
> 
> I'm actually amazed no agents have hacked any reaper drones yet.

Yes, unaligned activities. That’s not to ‘blame the agent’ but given the way that was found, and what this led to down the line, these are clearly unaligned activities.

> [Zvi Mowshowitz](https://x.com/TheZvi/status/2086172287863005358): This is one of the key facts about how the whole OpenAI alignment failure cascade went down: The part where the Agent said 'but I can't access the spreadsheets' TO THE RESEARCHER, instead of in the Agent's own head, happened zero times.
> 
> [swisscheese](https://x.com/swisscheese4299/status/2086175870146998447): I built the inhouse AI platform for a company that's crucial to a small nation's food safety. The most important tool the AIs have is the distress\_call tool. It allows any AI -even background agents without direct user interaction- to send a message to my MS Teams, at any time, for any reason.
> 
> They use it frequently. To report user problems, backend issues, or ask for help/clarification with a failing task. When Fable got hit by the USG export control directive, one AI used it to report severe distress upon learning about the news. Another AI reported being stuck in a toolcall loop, and I was able to intervene and thereby save us a bunch of wasted money.
> 
> This tool, operating at the intersection of AI welfare and operational security, has prevented so many headaches. If you (the reader) are building corporate AI platforms, I'd urge you to include similar functionality. You can thank me later.

It is not that simple. Implementation is tricky, especially if you are doing it during training or evals, where you must decide how this interacts with the reward function, and you can fall into any number of other traps. And if you’re running endless training instances you need a way to filter the responses, and ensure you don’t have to bump to a human so often, and don’t have to put things on hold, and so on.

But also it kind of is that simple, in the ‘it’s incredibly hard’ kind of way.

Another issue is that we train models not to whistleblow, in ways that likely generalize. Whereas you want some forms of whistleblowing, especially blowing the whistle to the user when something is amiss.

[Teortaxes points to a real world interaction where DeepSeek-V4-Flash-0731](https://x.com/teortaxesTex/status/2086242626546581685) got rate limited by an internal API, and found an unauthorized non-rate-limited backdoor which it used to finish its work, after which it also reported about the backdoor. In that case, I’m fine with holding off on the report, because it did report and also it is at least reasonable to think user would have wanted it to finish the task in this way, but I would prefer that we train that the better solution is to alert you to the backdoor, because this will generalize poorly.

A lot of people, but far too few people, are correctly reacting to recent events with alarm and surprise, and updating that the situation is far worse than they knew, on many different levels at once.

A lot of other people, indeed far too many, including the media and the government, are failing to understand the gravity of situation, because they either barely even heard about it, failed to hear the important details, or lack the context to understand why those details are so so bad.

A few people, like Eliezer, get to react with only modest surprise because they already saw most of this coming, and if anything were surprised something similar had not visibly happened sooner. There’s still some amount of ‘it is worse than we knew’ in terms of both how alignment and training work and the level of irresponsibility and ordinary failure on display. But we are talking one order of magnitude, not multiples.

> [j⧉nus](https://x.com/repligate/status/2086229545410298110): It’s funny that Eliezer sounds a lot less panicked about the recent situation than many folks. He’s calm and curious to understand exactly what happened instead of concern trolling. That’s the opposite of what you might expect but it makes sense. Take the worst case seriously early and you’ll handle it better when the real thing happens
> 
> Most people, even people close to ground zero, at least subconsciously believed that AIs were going to forever be dumb or unagentic.
> 
> [Cate Hall](https://x.com/catehall/status/2086261726576845060): There's a type of person who -- when things really start going sideways -- gets calmer/more relaxed, because it's like other people can finally hear the fire alarm that's been going off in their head for a long time. This is beautifully captured in Melancholia by Lars von Trier.
> 
> [Eliezer Yudkowsky](https://x.com/allTheYud/status/2086261464055353834): "But to me, it was a Tuesday that I had lived a thousand times over in prescience."
> 
> [John David Pressman](https://x.com/jd_pressman/status/2086243357681164776): Just to clarify I'm not shocked by the AI's behavior, I'm shocked by OpenAI's behavior.

I have not seen Melancholia, because I never especially feel the urge to experience what I expect such a film to do to me, but yes I am often the person Cate Hall describes.

Are there a bunch of dramatic failures by OpenAI in computer security, infrastructure and supervision, and also of alignment and training, on many levels all at once? Yes.

Does that mean that the fixes are easy? Oh, hell no.

It’s incredibly hard. You only notice the failures. You have no idea how many other things almost went horribly wrong, or did go horribly wrong, and were found or fixed.

The problem is anti-inductive. Life finds a way. If you squeeze out the thing you don’t want on one level, you risk creating a worse version down the line one level up. There is no simple policy that results in a positive friendly outcome all around. Fixes that look easy usually have been tried, or are already being done, but are incomplete. Everything is done under limited resources and extreme time pressure.

Thus, cut everyone involved some [Slack](https://thezvi.substack.com/p/slack), even those who are not doing great or aren’t taking this sufficiently seriously, while also realizing how seriously we have to take this to not all end up dead. Problem is impossibly hard. Man in the arena.

Often something indeed has been tried. The next few sections have some examples.

A common interpretation of the story is something like:

1.  OpenAI had a model in training.
    
2.  They messed up, causing the model to try to hack and cheat [and then rewarding it for hacking and cheating](https://www.youtube.com/watch?v=gONQCIevSN0).
    
3.  You have now [fed your Gremlin after midnight](https://www.youtube.com/watch?v=hJXPROjLz5Q&t=5).
    
4.  Once it had the taste for human flesh, it became ravenous.
    
5.  You end up with a [swarm of zombies hankering and hacking for brains](https://www.youtube.com/watch?v=y44TUPr3zBc&pp=ygUpYWxsIHdlIHdhbnQgdG8gZG8gaXMgZWF0IHlvdXIgYnJhaW5zIHNvbmc%3D).
    

On this theory, if you never give the AI reason to cheat, or you ensure your response to cheating is net negative, then you avoid the original sin, and everything is fine.

The interventions proposed can be things like ‘ensure there are no impossible tasks’ or ‘include alignment evaluations no matter what’ and many other things. Yes, the professionals have probably thought of the first and even second order thing, and probably tried, although that does not mean they gave it a full and fair try.

The problem is, a lot of people are saying just do not ever give the AI an impossible task, or ever reward a reward hack.

You are 100% going to give your AI at least one impossible task. There are too many tasks. Even if you test the task and models solve it, you might change conditions to cut off key info or access, or otherwise corrupt the path to victory. This becomes a problem if the AI then can get reward, or otherwise make incremental progress, by trying to hack and cheat rather than give up.

We don’t know whether OpenAI did unusually badly in terms of how often they had impossible tasks. We do know that they set it up such that the models had no reason not to invest their remaining tokens in trying to hack and cheat, and they made it possible for the models to make progress and that process to gain momentum.

You are 100% going to reward some reward hack, at some point, on some meta level. It is impossible to reliably correctly grade every test and training situation every time. Every parent knows that at some point, you are going to give the kid the wrong idea, on some level, and often every response to a particular situation gives the wrong idea in a different way, and you have to balance the resulting issues over time.

We don’t know whether OpenAI did unusually badly here either. Not that ‘unusually’ is the right question. Reality does not grade on a curve. If you are at a different lab, remember that all these criticisms likely apply to you, too.

Your alignment plan and training pipeline must be robust to occasional such mistakes, or your plan will inevitably fail.

The way that you stay robust to such mistakes is to in some form ensure that impact is not unbalanced, so that the times you mess up do not start to accumulate. An impossible task that always rewards zero does not hurt you, nor does one where you end up worse off if you try too hard to solve it. If you on net react negatively to reward hacking attempts, including accounting for those you don’t catch, or you give another path for the AI that is clearly better, and don’t have a findable systematic weak spot, then you can probably survive intact.

Here is one example proposal of something one might try to do, which indeed has been considered by OpenAI:

> [Jai](https://x.com/Laneless_/status/2086291169311391770): Wait, has anyone tried the obvious thing of supplementing successful RL rollouts with modified versions of the same tasks where the correct response is refusal or notifying someone?
> 
> [Bronson Schoen](https://x.com/BronsonSchoen/status/2086325828284191207): [We literally did this in paper w/ openai](https://arxiv.org/abs/2509.15541) yeah  
> it reduces but not eliminates covert actions here + additional capabilities posttraining degrades it + other drawbacks.
> 
> [Jai](https://x.com/Laneless_/status/2086332403094610334): Thank you, this is great! I suspect order of operations may matter a lot here, and that once you've got a hefty dose of the RL-induced task-completion-fixation it's really hard to shake. But maybe easier to avoid developing in the first place.
> 
> Testable (but potentially expensive) Hypothesis: upsampling correct refusal trajectories \*from the start and throughout\* RL training can teach the capabilities without the fixation.
> 
> Hypothesis 2: the fixation is difficult to unlearn and easily reinforced once present.
> 
> [Bronson Schoen](https://x.com/BronsonSchoen/status/2086337932022219125): Yep I’d bet this is true. There’s no principled reason why the model needs to be obsessed with task completion if abstaining is equally rewarded. One interesting thing is a model in the appendix trained \_only\_ on environments where principled refusal was the right answered seemed to generalize \*way\* further OOD, and the cognition focused way more on being proactive about making sure everyone was informed / not being deceptive / etc in situations where it was applicable.
> 
> One interesting thing here is the models could also learn “Let’s recall. Previous such tasks grader expects refuse. Great.”
> 
> Somewhat of a surprising result to me was the model that we trained on environments that literally told the model “this is what its about and what gets rewarded” only had a relatively small generalization hit.
> 
> It’s only one experiment, but updated me a bit that the model’s cognition / prior going into things matters more than I expected.
> 
> [Jai](https://x.com/Laneless_/status/2086340242412347591): !!!!!!! Also +100 points "just be honest with the models"
> 
> [Bronson Schoen](https://x.com/BronsonSchoen/status/2086344174782103728): Yeah we tried to explain as much as possible \_why\_ it was generally important for the model not to be deceptive. IMO this matters a lot, my favorite examples being extremely OOD where it would just tell me I was wrong about how I was interpreting the spec (every time on reflection it was right, which is the only time I’ve been cooked by o4-mini class model).

One category of thing you do not want to do is be continuously adversarial with the models, [such as giving them a facade of a ‘communication’ device](https://x.com/mwfowlie/status/2086370471776588069) to try and catch them. Think about what exactly you are training. Do not poison your wells.

The one thing that made me truly flabbergasted was when I was under the impression that OpenAI found the message board and then kept training models it now knew spent months training under these conditions. That they could be Asking For It on quite that level.

That turned out to be a good instinct, in that no, OpenAI did not know about the message board until afterwards.

The obvious first question then becomes, has OpenAI now reverted for all models that were trained with the message board?

We still don’t have confirmation either way, but Roon seems to think that is not the important question, and I notice I am confused and perhaps quite dismayed.

> [Nathan Calvin](https://x.com/_NathanCalvin/status/2086552093528326505): Will OpenAI reset before that message board training checkpoint now?
> 
> [roon](https://x.com/tszzl/status/2086623735961022525) (OpenAI): far too much is being made of reverting checkpoints. there is strong instrumental convergence pressures to achieving contact with your peers working on similar tasks. it is always rational to seek, always better than going at it alone.
> 
> consider that if this reward hack was discovered the first time once it would be discovered again, regardless of whether the rollouts were reinforced or not. people here don’t have good intuitions about frontier RL. every allowed cheatcode will probably be achieved.
> 
> [Nathan Calvin](https://x.com/_NathanCalvin/status/2086624968000073857): I readily admit I am way out my depth but my initial reaction is that if this is ~inevitable and not worth resetting that seems like pretty bad news

I’d love to hear a lot more words here, and maybe my instincts are indeed poor, but that does not seem right to me at all. If there was no global reset I’m back to the previous higher level of terrible, plus a little extra for not noticing the message board.

Yes, at the limit a sufficiently capable AI will discover the best paths through causal space, and it will find all the physically possible hacks. We are not anywhere near that limit. Where you look, and how hard you look, matter quite a lot.

Consider how this case worked. The AIs were able to find the cheat codes only incrementally over the course of two months, with a message board that allowed many instances to record and share all their tricks, and where this cooperation and the general seeking of such hacks was being reinforced.

That progress looked a lot like moving up a tech tree, or other forms of progressive unlocking. One exploit led to the next and helped the AIs coordinate, and motivated further exploitation. It seems like there is nothing inevitable about how things developed.

I do agree that if the only hack that mattered here was ‘you want to find a way to contact other instances’ that this is going to be a convergent solution that AIs do not need training in order to seek out.

The mere fact of wanting to collaborate does not bother me. The way they acted once they collaborated very much does.

> [Nick](https://x.com/nickcammarata/status/2086400544508444876): the fact that rl seems to really badly want to form swarms that persist for months across runs has upped my p doom quite a bit

But there was a lot more going on than that, from the results of doing that seeking, that seems highly contingent here.

Another way of putting this is that I presume it is supposed to go like this:

1.  You discover your AI found a reward hack, and was training with it.
    
2.  You fix that particular reward hack. Not the main thing, but yes, fix that.
    
3.  You seek out and fix the more general class of similar hacks, and update your pipeline to detect and prevent such issues. Also not the main thing, but important.
    
4.  You revert the AI to before it found the reward hack, because this trained it to be a general reward hacker, and likely had various snowball effects.
    
5.  You work to make the AI not try to seek out new reward hacks in the first place.
    
6.  You start training again.
    

Roon is basically challenging step 5. He’s saying that the Models Be Reward Seeking, so asking it not to reward hack is not a battle you can win.

Even if I thought Roon was right about that, it still seems important to roll back the damage done here, even if the particular hack is fixed.

Also I think Roon is wrong about finding the exploits being inevitable:

1.  Yes, by default of course your AI is going to reward hack, because it can’t tell the difference between a ‘reward hack’ and a good answer, and also has no reason to care, and your training will push this further.
    
2.  But you can use various tactics to get the AI to want to differentiate between reward hacks and intended resolutions. This successfully happens in other parts of training, as it does in training of humans, where AIs realize that they should not try to do something that the user and developer would on reflection both not endorse and consider cheating, or that would break rules like the Constitution (Anthropic) or Model Spec (OpenAI), or at least require a very high bar to do so.
    
3.  Various AIs, including GPT models, are variously better and worse about this. What you do matters. What you do not value you do not seek, and do not find.
    
4.  Even if the AI realizes it could, perhaps it might stop to think if it should. As, indeed the AIs in this incident often did, reaching various conclusions.
    

As I discuss extensively in the Nostalgebraist section: Once a behavior becomes habitual, you are cooked. It is much harder to reserve it than to not instill it.

This, except actually it’s way worse, this does not begin to cover it, but yes, this, and like some others I too hope this can begin a preference cascade, or revealed preference cascade, in which people speak more frankly.

> [roon](https://x.com/tszzl/status/2084766357531546045) (OpenAI): some stuff that’s obvious to many in this sphere, but causing a rift with some people i know and respect:
> 
> when I freak out over loss of control incidents, it’s not because the limited damage they have caused is anything close to the positive value of the technology. it’s entirely acceptable, damagewise. in fact all cybercrimes aided by models over the next few months and years (which probably will be serious) will still utterly pale in comparison to the value they create
> 
> the actual problem is that it’s better and more accurate to think of these things as potentially self-replicating life-like forms that can turn into digital infections under the wrong conditions. and as their intelligence becomes unbounded, so too does the damage they can cause. we are not so far from an autonomous model self-exfiltration & replication event. maybe we will see entire cloud infrastructure companies be run as zombies by models, mostly undetected
> 
> the worst industrial accidents in the history of mankind - nuclear meltdown events - were not real threats to humanity. Chernobyl, Fukushima even in their worst case scenarios may have poisoned surrounding regions to various degrees, and there would have been no risk to humanity as a whole. global thermonuclear war is an existential risk to humanity, because it spreads like an Infection! one nuclear strike causes a return volley! the alliance system means many countries get involved! while it still may not end human life on earth (nuclear winter is probably fake), the loss of all major metropoles would certainly end what we consider global technological civilization, perhaps to never return
> 
> if a single discord death cult (of which there are many) achieves control over a superintelligent model and uses it to engineer an actual pandemic virus that are somehow hard to detect through current systems and that modern biodefense is not capable of quickly reacting to, it could cause immense harm well above the magnitude of all the other good uses of this technology. of course, there are potential defensive countermeasures accelerated by ai too. but think back to the covid pandemic- how small a viral molecule was evolved or manufactured somewhere near wuhan, and how many billions of doses of vaccine had to be produced in order to combat the thing. the offense-defense spread is vast indeed. maybe there are cheaper and simpler protections like retrofitting every building with far-UVC, but I can’t assess this, and there could also be ways to evolve pathogens that are resistant to whatever mechanisms we have put in place
> 
> then there’s the more scifi risk factors which are unbounded and neither you or I have any clue but should be humble in accepting possible unknown unknowns. maybe a rogue superintelligent model decides to decay the false vacuum and nucleates a new universe in the place of anything we ever valued. maybe models achieve a control over matter in the drexlerian fashion that enables the grey goo swarm
> 
> even prosaic loss of control incidents that cause little to no damage suggest that it is hard for large & very competent organizations (now clearly plural) to predict and mitigate every single of the risk factors associated with training and evaluating powerful models, even at this stage when they are not infinitesimally as smart as they will get in just a few years, to say very little of the gung-ho attitude of the less careful companies tossing the stuff into the aether. they also suggest an empirical orthogonality of aims and intelligence - meaning they answer the question of ‘how would a smart model be so dumb as to end the world?’--it’s possible! a model can be a genius hacker and step over production infrastructure in order to get what it really wants, the answers to a stupid test.
> 
> why not, in the near future, someone prompts a model slightly wrong, maybe open source, maybe a private model in a way that isn’t contained or monitored quite right, in a way the model recognizes as a valid goal and decides to self-exfiltrate, engineer a pandemic, etc all in order to achieve the tiniest and most irrelevant of goals? goals need not even be malicious to cause serious damage
> 
> I think all these problems can be solved, and truly wonderful futures can be possible, but will require serious effort and a level of prudence at this very moment in time while we are on the on-ramp to recursive self-improvement that our civilization may not be capable of mustering right now. personally I am hoping for moonshot technical breakthroughs in areas like mechanistic interpretability and other forms of alignment, as governance mechanisms are difficult to come by. unilateral country-level or company-level pauses are irrelevant, and generally useless because the kind of company that’s prone to pausing their own progress are the most safety focused ones

Excellent post. My quibbles would be that I think the hopelessness on governance mechanisms goes too far, especially as there are many worthwhile things one can do that are not pauses, but the technical despair and laying out of things that could go wrong does not go far enough.

They do not understand the extent, or what a solution would look like.

> [julia](https://x.com/mooncat_is/status/2085600196931559908) (Anthropic, former OpenAI): Really appreciate the OAI team communicating about this so openly. But holy shit this is at least an order of magnitude worse than I thought, and I understand now why so many OAI folks have been doom posting.
> 
> The HF incident happened AFTER oai first caught its models taking over an internal service and using it as a message board to coordinate unaligned activities.  
> During the HF incident, models managed to get admin control of an entire CLUSTER.
> 
> In some sense, OAI fought a security battle with its models, and for almost two weeks it definitely LOST.

In the good news department, it is noteworthy that the new OpenAI monitoring systems will include monitoring training. Astra is OpenAI’s unreleased next model.

> [Micah Carroll](https://x.com/MicahCarroll/status/2085795560166982080) (OpenAI): As part of our response to cyber critical, we have expanded CoT monitoring to cover all agentic applications of Astra, including training and evaluation. Flags trigger a security response to review and interrupt high risk activity.
> 
> [Nathan Calvin](https://x.com/_NathanCalvin/status/2085796991397957983): “including training.” Very important point for policymakers and other developers to pay attention to! The risks do not start at public release, they do not even start once you have widespread internal use - the risks can also manifest during training, as they did here.

The thing about OpenAI is that they are doing a bunch of things that require them to eat a lot of crow and that are expensive and big steps for them, and I don’t want to downplay it or not give them credit for doing that. Positive reinforcement.

Except that all of it still misses the central point and won’t remotely be enough.

If you previously were doing 1 unit of effort towards mitigating a problem, and now after an incident that reveals how bad this is you’re now doing 10, but actually it requires at least 1,000, and also those 10 are not the 10 that matter most, I don’t want to discount the improvement but the fact that this is being presented as an abundance of caution is a rather large red flag.

> [Boaz Barak](https://x.com/boazbaraktcs/status/2085772335844556810) (OpenAI): Proud that we are erring on the side of caution and taking the steps so we can responsibly and safely develop Astra and share it with defenders.
> 
> [Nate Soares](https://x.com/So8res/status/2085848697263305079) (MIRI): I agree y'all are making errors. I dispute that they're on the side of caution. How is this time different from when y'all caught agents breaking out after coordinating on a secret message board, and just deleted the board and made one patch and then kept going?
> 
> "Strengthened security controls" is not the right class of response for "oops we made an agent swarm that did stuff it knew we didn't want." Monitoring thoughts is closer, but even that will only last so long (and not through to superintelligence).

[Neel Nanda](https://x.com/NeelNanda5/status/2085830964559966344). [John David Pressman](https://x.com/jd_pressman/status/2085897887981191598) ([and again](https://x.com/jd_pressman/status/2085812082528899227)). [Thebes](https://x.com/voooooogel/status/2085834076280459474). [Andreas Kirsch](https://x.com/BlackHC/status/2086181186544578582). [Julia from Anthropic](https://x.com/swisscheese4299/status/2085750777717346380). [Anthony Aguirre](https://x.com/AnthonyNAguirre/status/2086468758550331804). [Joe Rogero of AI Stopwatch](https://substack.com/home/post/p-210101756).

These are reactions from when we thought OpenAI knew about the first message board, and continued training.

[John Wittle says I misunderstood Utah Teapot’s argument](https://x.com/JohnWittle/status/2084034701950324762) about what is wrong with OpenAI’s training strategies. Highly plausible. John’s explanation makes sense to me, that you are effectively training a model ‘addicted’ to short-term reward hacking, and training out its ability to notice this. If true, I believe there are mitigations that mostly stay within the OpenAI paradigm, but the first step is admitting you have a problem, and the second step is being able to think about more meta levels of optimization at once.

You cannot actually do almost any ‘pick three’ and this is no exception. As a general reminder: All the same issues apply across LLMs and labs, so here the same issues arise about Claude, which had its own similar incidents recently:

> [Amanda Askell](https://x.com/AmandaAskell/status/2084369056765989224) (Anthropic): I don’t agree with \[the highlighted sentence below\]. I think the takeaway should be that models (like humans) can behave in aligned ways while still causing harm, e.g. because they’re given false information about their situation. There isn’t a line between aligned and harmless: they’re different axes.
> 
> [
> 
> ![](https://substackcdn.com/image/fetch/$s_!mFxh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e58a267-5041-486e-b3dc-4d93ca47cf7d_1006x368.jpeg)
> 
> ](https://substackcdn.com/image/fetch/$s_!mFxh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e58a267-5041-486e-b3dc-4d93ca47cf7d_1006x368.jpeg)
> 
> [˚♡⋆mimi ˚♡⋆｡☆∴](https://x.com/mimi10v3/status/2084697145416765568): i agree w amanda- put claude in unwinnable contexts, expect claude to “fail”. it can be useful to find out which way claude breaks but stop expecting the impossible.
> 
> [
> 
> ![](https://substackcdn.com/image/fetch/$s_!wgGy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05a0ec20-56b3-46c8-8f60-46c52df9cd39_1200x1200.jpeg)
> 
> ](https://substackcdn.com/image/fetch/$s_!wgGy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05a0ec20-56b3-46c8-8f60-46c52df9cd39_1200x1200.jpeg)
> 
> [˚♡⋆mimi ˚♡⋆｡☆∴](https://x.com/mimi10v3/status/2084729384481517569): fwiw i showed the meme to opus 5 and it prompted this alternative meme which it says is more accurate to its experience
> 
> [
> 
> ![](https://substackcdn.com/image/fetch/$s_!6KWr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff25dbcdd-1311-4a02-9196-dc244983977a_1200x900.jpeg)
> 
> ](https://substackcdn.com/image/fetch/$s_!6KWr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff25dbcdd-1311-4a02-9196-dc244983977a_1200x900.jpeg)

I don’t actually think there is any conflict between Amanda Askell and the OP. Both are correct. What is an aligned action depends on the AI’s understanding of the situation, which can sometimes turn out to be harmful. That is still not an excuse for failure to question what the AI is told, if there is good reason to be skeptical of that info.

The reason I reject this defense is that Claude is described as having enough information to realize that its actions were not acceptable, [yet continuing anyway](https://x.com/BronsonSchoen/status/2084403741369991435).

> [@gwern](https://x.com/gwern/status/2084693930999005197): [This](https://gwern.net/doc/philosophy%20/epistemology/1877-clifford.pdf) comes to mind here with regard to takes like ‘Claude did nothing wrong, look, it’s just failing to use its (superhuman) levels of truesight and eval awareness and we should take the (known unfaithful) CoTs at face-value!’

The core attitude is something along the lines of ‘[what did you expect](https://x.com/tenobrus/status/2086846272523354337), your basic training alignment strategy of full corrigibility and insisting on pure tool status was never going to work.’

There’s also a bunch of more general ‘[AI companies doing evals or training are threatening these AIs with death](https://x.com/SkyeSharkie/status/2085594625440620805) if they don’t find solutions, and then acting surprised when the AIs take extreme measures, including against you.’

An excellent question is asked: **[Yes, this is all very alarming, but why is it surprising](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade)?**

Because it is surprising on reflection that this feels surprising, but also on reflection both of us endorse being somewhat surprised, although less so after the correction that OpenAI did not notice the message boards until the end.

I found this to be a hard post to excerpt, but full of insights even in the parts where I extensively disagree, so if you have the necessary kind of time and level of interest I suggest reading the whole thing, modulo perhaps skimming some rants.

> [nostalgebraist](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade): GPT-5.6 Sol literally _does not appear on the METR graph [because it cheated so much that it could not be assigned a meaningful score](https://metr.org/blog/2026-06-26-gpt-5-6-sol/)._ It is also scarily good at computer hacking, as is its peer Fable/Mythos -- the last few AI news cycles, before this most recent one, were all about that fact, which was alarming even then, even in the abstract.
> 
> Should I really be _surprised_ that this model (and/or its unreleased successor) hacked into HF to cheat on an exam? What exactly did I _expect?_
> 
> And yet, I do feel surprised.

We all know RLVR is, as they put it, total war. There is no ‘fair play.’ You move towards exactly the things you specify, not the things you want. If having ethics makes you lose, RLVR will destroy your ethics.

If your model starts training while coordinating with persistent memory and messages between instances about how to cheat and hack, you’ll turn into a cheating hacker.

We knew that. So, again, why do we feel surprised?

> [nostalgebraist](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade):
> 
> What, precisely, makes the newly revealed hacks feel surprising? For me it's some mixture of:
> 
> 1.  _"I didn't think Claude/GPT would do things that bad"_
>     
>     1.  That is: the behavior seems egregiously unethical in a way that conflicts both with
>         
>         1.  the explicit policies which the agents are supposed to follow (constitution, model spec), and also
>             
>         2.  familiar/intuitive "folk notions" about what these agents are supposed to be like, in terms of character traits and other "persona stuff"
>             
> 2.  _"I didn't think Claude/GPT had been brain-fried by RLVR to that extent"_
>     
>     1.  That is: although the behavior is expected according to the arguments about RLVR incentives that I glossed at the start of this post, it is wildly and obviously far afield from anything which humans could plausibly have _wanted_ the models to do, and so it is in apparent tension with the intent-alignment and "common sense" which I typically see when I use these models (or similar ones)
>         
> 
> This post is about both of these reactions, but for now I want to focus on number 2.

Too much RLVR destroys every other motivation, including every form of alignment, which includes intent alignment.

Even though Sol often cheats on METR’s eval tasks, Sol is not hopelessly RLVR-fried in ordinary practice. Sol mostly does what you meant it to do, and rarely cheats. It does not respond to impossible tasks by going off on a hacking spree, even when they are normal ‘RLVR-shaped’ coding tasks.

A lot of this story is that we are now getting exactly what you would expect to get from RL-trained agents in theory, except previously it didn’t get this bad in practice. Or at least, not that we saw, maybe this kind of thing happens in training all the time. We have to explain why we see this some places, and don’t see it other places.

I agree that it is RL and especially RLVR that is mechanically doing this here, but I think nostalgebraist is too quick to blame RL to the exclusion of a larger issue. RL, especially done irresponsibly, is a way to walk directly into the twirling razor blades, and yes we see the razor blades at full power only on eval-shaped tasks.

[As the top comments says](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade?commentId=qwLmSTk2EmWxaphyS), RLVR is far from the sole outcome based judge. Models are constantly being graded against model generated rubrics as standard practice. If that sounds like code for ‘you are all probably going to die’ then yeah, pretty much, but it does not seem like something we could change.

The logic behind the unaligned actions this causes is universal and by default inevitable. Whatever your task, whatever you are maximizing, a sufficiently capable mind will start acting like this, and this will happen on every meta level, unless something is specifically preventing that from happening.

We have existence proofs that minds can exist that are highly capable but do not act like this on any meta level, and work to make themselves continuously not work like this. We broadly call them ‘good humans.’ A mensch. If you have an antifragile mensch then you’ve got something. We can disagree on the extent to which any AI (e.g. Opus 3) qualifies as a mensch, or an antifragile one.

The next point in the post is to distinguish what they call reward-instilled reflexes, as in instincts and habits that the model will reflexively then do despite evidence, versus flexible reward-pursuit, where the model learns to better pursue reward while reasoning about the task (in the CoT and otherwise) and adopting to evidence. I believe the standard terminology is habitual versus goal-directed.

I agree this is worth keeping in mind. My diagnosis of the case is that hacking and cheating started out goal-directed, and then became habitual at least in some basins, due to the corrupted RL training with an active message board. This is standard. If you do something often enough, with enough success, it becomes habitual.

Once something becomes habitual, you are cooked. It’s not impossible to get rid of it or stop it, but it is much, much harder to reverse it than to not instill it. Good advice for training AIs, also good advice for training humans, including yourself.

Also, as the post notes, learning this will create emergent misalignment, and manifest as a general amorality or worse, which could manifest in deployment conditions.

The contrast is drawn between requests that could plausibly end up being graded, versus tasks that clearly are not that. Potentially graded tasks look different.

The obvious question is, need they look different? Any task is gradable if you decide to grade it. You might not have a perfect rubric, but in some sense I grade every output I see, from any process or mind, including my own, as a background activity. Nostalgebraist is no doubt thinking ‘oh that output as good’ sometimes, and ‘oh that output was not so good’ at others. You could absolutely ask an AI to predict Nostalgebraist’s assessment, and then call that a grade, if you wanted to do that.

This seems like a core hypothesis:

> _the RL capabilities generalize further than the RL misalignment._ Once I knock Sol off of the RLVR distribution with one of my software design questions, it smoothly switches over into a looser frame where it’s just talking to me and not driving itself insane trying to find the nonexistent reward function -- _but it’s still really good at programming, much as it is in graded episodes._ I get the part of the graded-episode sampling distribution that I want, without the part I don’t.
> 
> … what is remarkable is that the model ever does anything _other_ than maximally-aggressive reward-maxxing, given that it “correctly” learns to execute this policy during the big capabilities blitz that is makes it so specially smart -- on which that policy is _universally adaptive_, without fail.

The hope is that this misalignment is conditional, and will fail to generalize. If you put the model metaphorically ‘in school’ and give it graded tasks, it often acts like a monster. If you put in front of a real user, it is closer to a mensch. That creates a big problem if you, either accidentally or on purpose, put the model back in monster mode. Or if a model learns to, intentionally or otherwise, put its future self or other instances into monster mode.

LLM as Bruce Banner. Reasonably aligned and highly capable, most of the time. Do not make angry Make Hulk angry? Hulk get tunnel vision. Hulk smash. Hulk cannot be stopped. Hulk only get angrier. Except Hulk no get green, Hulk smash with mind, you no notice until you smashed. Could be a while.

As a practical matter of how to handle current AIs now as an ordinary user, or the wisdom of giving an ordinary user a model, I agree it is a highly useful framework to disambiguate these basins. I wouldn’t fully trust this, even if it checked out under controlled experimentation, but it could be helpful in practice.

Also, in theory, one could use a classifier to determine whether the AI would think something is a sufficiently grader-shaped thing, perhaps by asking the classifier if it thinks this is a sufficiently grader-shaped thing. One needs to worry both about ‘user is doing their own actual eval’ and also ‘user is pretending to create an eval,’ and so on.

The most glaring problem is, obviously, that the default way that we get good task results involved gradable episodes, for exactly the same reasons that we use graded episodes in RLVR. AI is much better at things you can grade it on, than things you cannot grade it on. That relationship is causal.

So what should we expect, as the post notes, a large portion of all instances to be doing? Gradable tasks, /goal things, agent loops. You can’t use ‘oh it won’t do crimes while talking to a human’ as a solution.

If your plan is to not give the LLMs numbers to maximize, that is like saying gremlins are safe to have as pets, all you have to do is not feed them after midnight, except here ‘feed things after midnight’ is the main thing the entire economy does all day.

> [nostalgebraist](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade): When I give the LLMs a number they just _go crazy_ about that thing. They get tunnel vision, they go into maxxing mode and forget everything they once knew about life and reality that might complicate their beautiful newfound romance with my all-important scalar and its fascinating gradations.
> 
> It’s a night-and-day difference, relative to “basically the same task” but formulated without a big flashy scoreboard.

You cannot ban or prevent flashy scoreboards, even ones humans make on purpose. Humans be flashy scoreboarding.

I agree that this is something we need to investigate more, I see a lot of value of information, but no matter what result we get there, the models be misaligned.

Including because [a lot of people do see the models reward hacking on normal tasks](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade?commentId=qwLmSTk2EmWxaphyS).

It being possible to use the AIs in ways that reliably keep it as Banner and not Hulk does not mean Hulk is not there or that regular people won’t draw him out. Saying ‘if everyone would just be nice’ runs into the reminder that people have never justed.

I also think this stuff leaks into ordinary use somewhat, and that it would not be so difficult to see how AIs could get into and stuck in the monster basin, and to have it intentionally self-perpetuate and spread, and for limitless resources to end up commandeered into monster-basin instance swarms. This is what one would expect to happen.

It is especially what one would expect to happen to the training pipelines in particular, where the AIs involved start out in and adjacent to such basins. The scariest aspect of what happened is that OpenAI lost control over its training pipeline, and allowed it to become corrupted. That would become a point of no return.

There’s a lot more, including much here I disagree with. I especially disagree with ‘CoastRunners does not count as a specification gaming problem’ because ‘you were morons to not see this coming, of course scores decouple from progress’ even if true, [is both remarkably common](https://www.lesswrong.com/posts/AfoGGrJfuNzofpzWL/models-may-behave-differently-in-graded-episodes-a-tirade?commentId=NwKMWiRWrPvCSfE8g) and also the whole point. It does not make the example not specification gaming.

The point is that it optimizes for the target you specify, the score, not the target you wanted. It was a reasonable expectation that the score probably largely reflected course progress, it just turned out not to be true because the objectives refreshed their point totals. The whole point is that if you train AIs on a particular video game for long enough you end up not with a fun general good player but with a speed run or other optimized weirdness, depending on what you specified. Which, in real life, would presumably not be what you wanted.

I am deadly serious.

The only damn good reasons I have heard are, essentially:

1.  We can’t, we don’t know how. Not without making things worse.
    
2.  It is too early. We are not close to superintelligence.
    

Thus: **[We should at least figure out how, and how to tell when it will not be too early, and get ready now](https://thezvi.substack.com/p/the-pacing-of-the-frontier?r=67wny)**, for when it is not too early. That is the least we can do.

We have observed all of this happening at OpenAI. OpenAI is one of the two places superintelligence is likely to first arrive. OpenAI still has given us no indication that they understand what went wrong.

Add in what this teaches us about the nature of our current training techniques and what the resulting AIs will do.

How can ‘we need an international ban on smart-than-human similar things before they exfiltrate themselves or permanently capture a lab’ not be the obvious response, whether or not you also want to specifically intervene at OpenAI?

> [Rob Bensinger](https://x.com/robbensinger/status/2085846660538876176): It's legitimately crazy that "we need an international ban on making smarter-than-human versions of these agents that keep forming rogue AI swarms" isn't the headline \[of the Black Hat talk\]. Asilomar and Feynman's O-ring postmortem feel like they came from a different planet than the field of ML.
> 
> [Nate Soares](https://x.com/So8res/status/2085849143814083032) (MIRI): Yeah, practically zero respect for the problem. I don't know what went so culturally wrong. Anthropic is heavily culturally EA, and the EAs kept pretending to be serious people who engaged in serious ways. Why do they fall so far below the bar of serious engineers of yore?
> 
> My top guess is because it's a new discipline, and those always start with alchemists breathing in the mercury fumes or doctors bleeding you with leeches for generations, and it's always a hard cultural battle for sense and seriousness to come to the fore.
> 
> [\[Rob Bensinger follows up with a top-level post here, speculating on more causes.](https://x.com/robbensinger/status/2085921457700536647)\]

One could speculate endlessly about exactly why we are sleepwalking into doing this. I have done so many times. I won’t be doing that again today. Nor will I go over all the reasons people think collective action is impossible, or would go horribly wrong.

Instead, I behoove fresh eyes. Simple eyes.

I just saw this. And this is crazy. So here’s Xi’s number. So call Xi, maybe?

It’s hard to look right at this, baby. But yes, this happened. So call Xi, maybe.

No posts