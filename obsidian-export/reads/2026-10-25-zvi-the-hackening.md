---
title: "The Hackening"
title_zh: "大黑客潮来了：PHP 漏洞、AI 自动化入侵与「防御者优势」的破产"
author: "Zvi Mowshowitz"
saved_date: 2026-10-25
original_url: "https://thezvi.substack.com/p/the-hackening"
slug: "zvi-the-hackening"
source: "manual"
fetch_status: "ok"
fetched_at: "2026-10-25T15:22:37.086Z"
fetch_type: "html"
content_length: 43230
tags: ["AI 网络安全", "The Hackening", "PHP 漏洞", "漏洞披露", "AI Agent 攻击", "攻防平衡", "开放权重模型", "出口管制", "Daybreak", "个人安全", "Zvi"]
---
# The Hackening
*Zvi Mowshowitz*
> 🔗 原文：[https://thezvi.substack.com/p/the-hackening](https://thezvi.substack.com/p/the-hackening)
---
Last week at a small conference, there was talk about a future event referred to as The Hackening. As in, within 6-12 months, many predicted that due to advanced AIs and AI agents the internet would become a severely hostile place. Some worried that this could rise to the level of ‘assume any phone connected to the internet is rooted’ and several people urged doing general crisis preparations on a personal level, in case of disruptions in supply lines, power, water or internet.

It did not take long for things to escalate.

The biggest hack is a flaw in PHP, which can be exploited to take control of the computer running any website suing an unpatched version of PHP. There are many others.

On a personal level, you want to do at least some basic prep and get your security in order. It is cheap to do as a form of insurance, and being caught not having it when you need it is a large mistake. That doesn’t mean you should panic, or cancel travel plans or anything like that. But there is low hanging security fruit out there. Pick it.

> [Joshua Achiam](https://x.com/jachiam0/status/2112968705240109558) (Formerly OpenAI): Feels like March 1, 2020 for Cyber. Not normal, something is happening. Internet lockdowns in a couple of months?

[Multiple sources using GPT-5.6 Sol identified a critical flaw in PHP](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/). [Okay, identified two critical flaws](https://www.youtube.com/watch?v=psMMKgvpGfg&pp=ygUgc3BhbmlzaCBpbnF1aXNpdGlvbiBtb250eSBweXRob24%3D) in PHP. The plan was to deploy the patch first before announcing the flaw, but the embargo on the fix got broken more than six hours in advance, so here we are.

> [Dan Lorenc](https://x.com/HackingLZ/status/2113025408975143080): I wanted to share what happened with the PHP embargo, our role in it, and my decision process last night to ship the fixed builds early. First of all, the PHP Foundation and maintainers did an amazing job here in a high stress situation. I'm sorry that my decision led to even more stress for them.
> 
> We first got read in that there was something coming up in PHP last Friday by one of the original researchers that discovered this issue. That night we were able to independently discover the same issue using our harness and a frontier model with a basic prompt of "find bad vulnerabilities in PHP".
> 
> We got fully read in Saturday and confirmed that some our findings matched those from the initial report, and worked to help test the fixes.​

[

![](https://substackcdn.com/image/fetch/$s_!_K2M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c94051d-d43e-4f6c-9f0e-274c1583e2fe_1206x760.jpeg)

](https://substackcdn.com/image/fetch/$s_!_K2M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c94051d-d43e-4f6c-9f0e-274c1583e2fe_1206x760.jpeg)

They may have been in a rush due to attackers finding the exploit. [Amazon reports that this was happening as early as October 17](https://x.com/dnvolz/status/2113060616768213478), four days before disclosure. We are fortunate that this did not scale far larger than it did.

> [The PHP Foundation](https://x.com/ThePHPF/status/2112633155631108544): The PHP security team is giving advance notice: Upcoming security release Wed, Oct 21st 2026, 14:00UTC, two critical vulnerabilities, both rated CVSSv4 9.2.
> 
> PHP users are encouraged to prepare to update. Earlier release if details become public or active exploit evidence.
> 
> If you rely on the volunteer maintained
> 
> https://rpms.remirepo.net
> 
> we urge you to move to distro packages or building from source now, so you can immediately apply updates. The repo will not have updates today. Follow up: Remi managed to still pull this off, and is signing rpms right now!
> 
> [Jonny G](https://x.com/dontforgetchaos/status/2112899057626870153): Can somebody explain this to me like I’m 5 years old please? Ta.
> 
> [BRYNMAWR ∴ SHERLOCK](https://x.com/sherlock_comms/status/2112904595995275554): Websites are files on a computer. When you view a website, you are asking the computer to send you the files, then your browser shows them to you.
> 
> 70% of the websites you see use PHP to make them interactive. So you can send things to the website too and it can respond. E.g. filling in a comment box and hitting ‘post’ adds the comment as a row to a spreadsheet.
> 
> PHP has a flaw in its code that allows anyone to gain control of the computer that has the website on it.
> 
> The organisation that provides PHP announced the vulnerability before a patch was available, meaning we’re in a window where everyone knows about it (including baddies) but the good guys don’t have an official solution.
> 
> Some are just turning off their websites and waiting for the solution. Others are trying to fix it themselves. General chaos and lots of stressed techies across literally the entire planet because this affects the entire internet.

[The bug has been there for 14 years and was discovered in 2024](https://x.com/gdb/status/2112921529650688312), but it was not considered significant at the time. A lot more bugs are significant now.

> [Jack](https://x.com/tracewoodgrains/status/2112940237270011929): Life is basically the same as it was in 2021. This is a normal experience caused by a normal technology. Ordinary people are experiencing no material changes from this mildly useful office productivity software people are calling AI.
> 
> I can tell from my ordinary daily experience that ordinary people are materially impacted by this because I was hanging out with the ordinary person who runs one of these essential online services (explainXKCD) last night

[

![](https://substackcdn.com/image/fetch/$s_!RWJF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff31c225f-a011-486c-803f-547c0ddfc339_1170x581.jpeg)

](https://substackcdn.com/image/fetch/$s_!RWJF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff31c225f-a011-486c-803f-547c0ddfc339_1170x581.jpeg)

> [International Cyber Digest](https://x.com/IntCyberDigest/status/2112865804358205593): ‼️ PHP UPDATE: 4chan has gone read-only and Something Awful has shut its forums as American sites brace for the PHP patch.
> 
> 4chan says it is “temporarily read-only while we await an urgent PHP security update.”
> 
> Something Awful says the flaw “allows for the kind of hacking you see in movies (but in real life).”
> 
> Bookmarking service Pinboard, game publisher Choice of Games, history site Damn Interesting and the explain xkcd wiki are offline too, as is art site Fur Affinity.
> 
> DeviantArt is also down “for maintenance” but has not said why.
> 
> PHP’s fix is due at 14:00 UTC, 10am in New York.
> 
> [Huzaifa](https://x.com/huz_man1/status/2112894414292983885): 4chan going read only by choice is how you know it’s serious.

Things could have gone very, very badly, the same way Y2K could have gone quite badly if we had not done the work to prevent it. These days we are on rather tighter deadlines.

> [Internet Archive](https://x.com/internetarchive/status/2112912342564622841): https://Archive.org is currently offline. We are working to restore service now.
> 
> Brewster Kahle (21 hours later): Internet Archive ops staff were heroes last night.
> 
> PHP vulnerability announced, soon saw attacks, isolated the vulnerability, used Claude to make fixes for our older php versions, used local models to run simulated attacks, deployed.
> 
> reinforced WAF and other guards.
> 
> Offline briefly, Back on new versions and running!
> 
> Given the severity, there are heroes in many many orgs from last night.
> 
> Could have been no lights, no traffic signals, real problems.
> 
> Heroes.
> 
> Thank you all.
> 
> [Alfred Shingai](https://x.com/alfredshingai/status/2113183957663744075): I do not see any reason anyone would attack internet archive. those guys are heroes.

A lot of websites are going to go down permanently.

> [Joshua Achiam](https://x.com/jachiam0/status/2112957226801615325) (Formerly OpenAI): If there is a part of the internet you wish to preserve and make a backup of, now is probably the time; the level of bitrot coming is beyond comprehension.
> 
> [spor](https://x.com/sporadica/status/2112946435910197548): wait, if my math is correct.. doesn’t this say that a full ONE THIRD of the Internet is just...perma-fucked?
> 
> [International Cyber Digest](https://x.com/IntCyberDigest/status/2112890547019145245): The day the internet broke, and most of it is too old to fix.
> 
> PHP’s supported branches, 8.2 through 8.5, will receive a fix. Everything older, 8.1 and down, is EOL.
> 
> Of the top 7.2M PHP websites we analyzed, 46.1% of those that reveal a version run an End-of-Life branch.

It’s not quite as bad as spor describes. PHP shipped minimal backports for 7.4, 8.0 and 8.1, but I would not want to be running those going forward.

[In summary](https://x.com/CupOJoseph/status/2112745162309013883):

> [j🫪e](https://x.com/0x_Osprey/status/2112686904084963465): ICYMI: Today was basically the worse day of the year for cyber security incidents

[

![](https://substackcdn.com/image/fetch/$s_!Z-Nz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ec00bf2-a85d-4bb4-9dc7-d28c0a43cc62_585x500.png)

](https://substackcdn.com/image/fetch/$s_!Z-Nz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ec00bf2-a85d-4bb4-9dc7-d28c0a43cc62_585x500.png)

Now the race is on to patch all the systems before attackers can go on the offensive. OpenAI is helping race to get that done to the greatest extent possible, and are looking for better methods for fixing vulnerabilities in time.

> [John David Pressman](https://x.com/jd_pressman/status/2113045116743192612): I know everyone is rightfully freaking out but it must be noted that the worst case scenario isn’t you receiving lots of patches you have to apply, the worst case scenario is receiving zero patches and waking up to everything having been stolen.
> 
> [John David Pressman](https://x.com/jd_pressman/status/2113046794741690656): My takeaway so far is that we do not have a good way to coordinate the distribution of patches to vulnerable software.

This one was important enough the NSA got in on the act.

> [NSA Cyber](https://x.com/NSACyber/status/2112903220209098897): Effective Immediately, all organizations using PHP for their systems are advised to be prepared for an update addressing two critical vulnerabilities. PHP is widely used for web applications. These vulnerabilities often provide a direct path to the server’s file system or database. If an immediate update is not feasible, it is recommend that organizations take the system offline until it can be fully mitigated. NSA will follow up shortly with more specific guidance.

We are going to need better procedures for updates.

The best case scenario is that a defender finds the bug first, has enough time to figure out a solution and creates a patch. Then, the moment the patch is rolled out, every attacker gets what are effectively very clear instructions on how to exploit any unpatched systems.

> [Sichu Lu](https://x.com/lu_sichu/status/2112918460728807802/history): It's kind of a funny thing where even if white hats find bugs before the black hats, the process of updating is hard and bad and time-consuming and barely possible for some devices, and so the cyber asymmetry still exists.
> 
> I think "updates" need to be rethought. like a lot of updates require permissions to happen and manual intervention and openai and the other sota labs should just offer some sort of automatic service to their suscribers to be constantly monitoring and updating and searching for bugs in new software patches
> 
> like in the future manual updates will just be too slow. you need to do something like rolling updates

Some software has a lot of bugs. Some of that same software powers the internet.

> [John David Pressman](https://x.com/jd_pressman/status/2112985159914185117): A majority of the smart version of this thesis is “after enough 10/10 CVEs you will simply take down and rewrite or deprecate all software written in things like PHP and C.”
> 
> I’ve seen plenty of PHP guys joke that this is just Tuesday for PHP, which isn’t quite true but.

> [OpenAI](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/): As significant as they are, these bugs are among several significant vulnerabilities we’ve already found and are working to fix, and we expect similar findings to increase sharply in the coming months.

The same day as the PHP vulnerability we also were treated to this:

> [The Hacker News](https://x.com/TheHackersNews/status/2112981939984671090): 🚨 CRITICAL: GitLab flaw (CVSS 10.0) affects 12 years of releases. CVE-2026-110264 could allow unauthenticated remote code execution on self-managed servers.
> 
> [The Hacker News](https://thehackernews.com/2026/10/critical-gitlab-flaw-cvss-100-could.html): GitLab released fixes on October 21 for a flaw that lets an attacker run code on a self-managed server without logging in, and it affects every version of the software going back to 7.0, released in 2014.
> 
> The fix matters even for administrators who patched nine days earlier: the October 12 update covered only versions 19.2 and later, and the new fixed versions sit one patch above it, so an instance updated then is in range again.

And this:

> [Jacob Cooper](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) (Railway Blog): Earlier this morning, Railway detected anomalous activity involving systems that store customer environment variables. After further investigation, our investigation to date indicates that an unauthorized third party may have accessed encrypted environment variables and, for some of them, obtained the decrypted contents. Environment variables may contain secrets such as API keys or database and registry credentials.
> 
> … **What you should do:** As such, we strongly recommend that you immediately roll all environment variables, including any API keys, stored in Railway, as well as any private registry credentials, and review logs for those services for unusual activity.

And also this:

> [Microsoft Threat Intelligence](https://x.com/MsftSecIntel/status/2112975078266716390): The China state-aligned threat actor Storm-0940 used the agentic AI penetration testing framework ARTEX to automate attacks targeting hundreds of organizations globally across a broad range of industries. [Microsoft Threat Intelligence assesses](https://msft.it/6018aakEE) that Storm-0940 was responsible for the recently disclosed ConnectWise supply chain compromise of a multitenant application.
> 
> Our investigation found that Storm-0940’s use of ARTEX accelerated the speed of compromised application abuse to authenticate to target environments through applications that had already been granted access, allowing the threat actor to operate without requiring an interactive user sign-in. AI-accelerated follow-on activity included reconnaissance, application credential changes, and attempts to modify privileges that could enable expanded or persistent access.
> 
> Read our blog for a detailed analysis and indicators of compromise (IOCs), along with Microsoft Defender detections, protection recommendations, and guidance on investigating service principal sign-ins and unexpected application credential or privilege changes.
> 
> [Divyansh Kaushik](https://x.com/dkaushik96/status/2113223967901106521): Curious whether the PRC filed this under “AI incident reporting” or “mission accomplished.”
> 
> Presumably the PRC’s contribution to AI incident reporting should extend beyond supplying the incidents? Or I guess we can file this one right next to the 2015 Xi Pledge on cyber theft.

And this, probably nothing:

> [GitHub Status](https://x.com/githubstatus/status/2112920050390684070): We are investigating reports of degraded performance for Actions, Pull Requests and Webhooks.

Things are steadily escalating. Get ready.

> [Choblin](https://x.com/choblin29/status/2112133997505794285): Reuters is reporting that a Chinese-speaking hacker used AI agents to compromise websites belonging to more than 100 companies, including Deere, SharkNinja and Cummins, after attempting intrusions against over 1,200 sites.
> 
> The estimated cost: roughly $5,000 in AI tokens, or $50 per successful breach. Successful intrusions took around 23 hours on average.
> 
> The attackers used the open-source Cairn agent framework, apparently combining DeepSeek models with a Claude Code harness. One campaign gave its agents instructions in fewer than 100 Chinese characters.
> 
> NorForge researcher Snorre Fagerland: ‘It’s a new world now.’
> 
> [David Manheim](https://x.com/davidmanheim/status/2112150641141281234): If this surprised you, you haven’t been paying attention. Generic and easily usable cybersecurity is ending.
> 
> The choice now is either proactively monitoring and defending, which might be enough (if we’re lucky), or not doing so, so any script-kiddie can ask their LLM to attack.

AI cyber is scary both because it will find new vulnerabilities, and also [because it will exploit](https://x.com/diogomonica/status/2110661457113468931) all the existing dumb vulnerabilities at scale, [such as accessing Denmark’s national ID database with the password ‘123456.](https://x.com/Kalshi/status/2110589482844192897)’

[India discloses an official account of rogue AI agent attacks](https://x.com/choblin29/status/2111012579728412742). This looks like another ‘harmless in practice except that it was a government database’ incident.

> [Andrew Curran](https://x.com/AndrewCurran_/status/2113437710065311970): [Quest Diagnostics has been hacked](https://t.co/B3mouySJeE). Patient data was exposed. They serve roughly half of U.S. hospitals and physicians. Investigation ongoing.

As an example, [Andrew Curran resurfaces a notice that there are probes](https://x.com/AndrewCurran_/status/2113076973086109698) against US-based Siemens PLC installations using AI scripts.

AI will make it easier to probe essentially everything. Anything vulnerable will be hit. Even if there is no economic reason to do so, some people want to see the world burn, or want to see the West burn.

[Hackers used Claude and Grok to automate attacks on banks](https://www.theinformation.com/articles/hackers-used-claude-grok-fully-automate-attacks-banks?utm_campaign=article_email&utm_content=article-18015&utm_medium=email&utm_source=sg&rc=tv1dv6). The good news is that the banks understand they are primary and high-value targets, and are investing heavily in cybersecurity. The bad news is that their definition of ‘heavily’ and what is actually necessary may be greatly different.

[Banks also have to deal with the AI agents inside their customer accounts.](https://x.com/MadisonMills22/status/2113251043173683683) Most of them are authorized by the customer, but this is one place the customer is not always right, and some of them were not so authorized and it is hard to know which is which.

> [Madison Mills](https://x.com/MadisonMills22/status/2113251043173683683): [SCOOP: Major U.S. banks are detecting unauthorized third-party AI agents](https://www.axios.com/2026/10/22/ai-agents-banks-unauthorized-accounts-access) inside customer accounts, including some attempting to take actions that appear to be independent of user instructions, sources told Axios.
> 
> The findings have alarmed banking executives, who are racing to restrict access to their systems as AI moves at a velocity faster than financial institutions can respond, multiple industry and bank executives told Axios.
> 
> Several banks are now preparing for worst-case and even “day after” scenarios, including how to rapidly secure or restore customer accounts if things go wrong, the people said.
> 
> Several bank executives told Axios they’re struggling to distinguish between human users and AI agents. One executive said banks also struggle to determine whether agents are authorized by customers or potentially operating without their permission, more akin to rogue agent behavior.

[David Sacks suggests read-only permissions](https://x.com/DavidSacks/status/2113317306398879787) as an interim step while banks work to support agents in a safe way and have authorized connections, which seems wise. Then Sacks warns about the ‘irresponsibility’ of ‘blurring the line between user-authorized agentic behavior and cyberattacks.’ Whereas I see the ‘blurring lines’ here as two things. One, the banks being unable to distinguish one from the other, which is a real issue. Two, if Muse (or your OpenClaw, etc) convinces you to let your agent into your bank account, that can quickly turn into a cyberattack, and again the bank cannot tell.

If I was the banks, I would absolutely not allow agents to authorize any transactions until I could verify the status and nature of those agents. They have huge downside exposure risk as do the customers. This isn’t crypto (derogatory).

Soon days like this might be typical, or even quiet. After all, despite all the issues, life mostly continued as normal.

> [Patrick McKenzie](https://x.com/patio11/status/2113065196814266774): We are entering a new normal. The new normal is going to be very weird. This is also true for a lot of non-security new normals.
> 
> Was today a busy news day for security vulnerabilities? You may remember it as the one of the last quiet days.
> 
> The models don’t just seem to be really good at security research. They \*want\* to be doing security research. They love it. It is fun for them. I think many of us geeks can relate.
> 
> A model did unprompted security research against a Japanese bank when I asked it to help w/ taxes.
> 
> (I asked it to calculate daily value in JPY and USD of a position in a Japanese mutual fund given a screenshot of the position at Broker A. It thought to itself “I mean that’s just silly; all I need is the daily net asset value. Custodian C almost certainly has an API for that”)
> 
> Model internal reasoning quoted inexactly, he adds, to not have lied about the exposed thoughts of a computer program.
> 
> I am glad I am not telepathic but if I were telepathic I think the most minimal possible ethical standard for telepaths is “If you ever talk about a non-telepath you do not lie about what you telepathically lifted from them.”

There is no clear line, contra Sacks, between ‘this is a clearly authorized agent’ and ‘this is clearly not an authorized agent.’ Agents Can Just Do Things.

The original rogue agent incident remains Hugging Face. I wrote quite a lot of posts on the situation, but they are poor explainers for a non-technical person.

Luckily, **[new explainer for the people just dropped](https://huggingface.wtf/)**. It is very good at explaining the key parts of the Hugging Face incident in plain language. Highly recommended.

> [Oliver Habryka](https://x.com/ohabryka/status/2112259535012528556): In July 700+ agents formed their own society, hacked a multi-billion dollar company, committed multiple felonies, and caused one of the biggest shifts ever in how people perceive AI. We built the IMO best and most accessible explainer of what happened:
> 
> https://Huggingface.wtf
> 
> [Daniel Kokotajlo](https://x.com/DKokotajlo/status/2112288877524443352): This is cool: You can see the grid of agents (scraped from the report data) and hover over each of them to see what they were saying at the time, and then scroll down through the hours and days of the timeline.
> 
> [Brangus](https://x.com/RatOrthodox/status/2112270894467072160): It doesn’t contain much info that isn’t in the metr report, but unlike the metr report, it’s primarily a story. I think it’s somehow good to present stories as stories.
> 
> [Kelsey Piper](https://x.com/KelseyTuoc/status/2112265754842391031): I think this is by far the clearest, most complete and most detailed breakdown of the Hugging Face incident. It won’t contain much new info if you read the METR report, but if you’ve merely been vaguely intending to read the METR report, read this. (I gave feedback on a draft.)
> 
> [Nathan Calvin](https://x.com/_NathanCalvin/status/2112525546513142023): This is extremely well done, no matter how much you know about the HF incident I strongly recommend checking it out. The website also includes the most comprehensive list i’ve seen of rogue AI incidents (tho its literally too long for me to screenshot!)

The information is mostly in the METR report, but in addition to being a story it organizes some of the data into a more highly readable form.

Thanks to Raymond Arnold for putting a month of work in on this. I was able to help a little bit with the editing while at the conference last weekend, as were a number of others.

**[If you prefer video we got you, here’s AI In Context](https://www.youtube.com/watch?v=xFYUo0ZmK-A)** with an explainer.

[HuggingFace CEO Clement Delangue is still on the anti-anthropomorphization train](https://x.com/kevinroose/status/2112553762737025423), and still blames the attack on prosaic failures at OpenAI along with his other existing talking points.

Also, there is a Netflix ‘instadoc’ called AI Gone Wild about the incident. I have not watched it.

Earlier this week [Open Code got hacked](https://x.com/opencode/status/2111519637049319818) as part of a large scale distillation attack, impacting 1.4% of users.

> [dax](https://x.com/thdxr/status/2111790511409258796) (Open Code): they’ve been non stop trying to attack our systems for the past 48 hours. A side effect is everything is getting hardened but damn we basically need agents going 24/7 because that’s what they have.
> 
> [Rhys](https://x.com/RhysSullivan/status/2111831027824160865): Are you getting blocked by cyber safe guards at all with frontier models?
> 
> [dax](https://x.com/thdxr/status/2111831348336091179): yes that was a bit frustrating mid incident when trying to investigate. they did quite a bit and then started refusing
> 
> we got access to daybreak blue now so it’s better
> 
> [Paul Graham](https://x.com/paulg/status/2111823339953991832): This is how things will be for the foreseeable future.

Everyone reading this who has something worth defending, try to get Daybreak and similar programs going now, before you are attacked. Do not wait.

> [Sir Lemmings](https://x.com/sir_lemmings/status/2112125186938228953): people are mad at this because it makes a “caste system” or excludes small companies, but this is idiotic.
> 
> i was able to get daybreak blue access for my tiny company on my individual codex account in like 15 minutes.
> 
> these people are just incompetent.

I will not have sympathy for you if you choose not to do this. It is not as if getting access is difficult. You can mostly get it by asking nicely.

It is always a good time for basic personal-level advice. I think something around the level of Wildeford’s advice is wise. You are probably fine with less than that, but if you have to pick a mistake being too prepared is probably the better option.

> [Peter Wildeford](https://x.com/peterwildeford/status/2112994329316708756): PSA: in light of recent cyberattacks and vulnerabilities, I recommend everyone:
> 
> \* use a good password manager (1Password) and do not duplicate passwords  
> \* use two factor auth for everything important (not via sms!! Google Authenticator or better yet YubiKey)  
> \* Auto-updates on, and restart weekly so they actually install  
> \* Freeze your credit  
> \* Get an IRS Identity Protection PIN  
> \* Get your cell carrier to give you a port-out PIN or number lock that makes the carrier refuse to move your number without the PIN
> 
> You can ask your claude code to audit what on your laptop is out of date and needs updating.

Others recommend going a bit further:

> [deepfates.delve.town](https://x.com/deepfates/status/2112967705200603345): It seems like we’re in a pretty hot moment cybersecurity wise 😬 If you’re reading this website, you probably know more than most of the people in your life about what’s happening! they’re not talking about any of this stuff on the news, it’s too arcane and weird and sudden. It is on us.
> 
> Good time to call or text your family and friends, have some cash on hand, have a meetup point in your neighborhood for if the Internet goes down entirely, etc.
> 
> The full prepper mode for shit hitting the fan is probably something like what Andreas posted here but you can get 80% of the way with 20% of the effort. Think about what that would mean for you in your situation, and the people you care about, and talk to them about it sooner than later.
> 
> And as always, the most important part of prepping is having a strong support network and caring for each other. “Going off grid” isn’t the move, it just makes you isolated and you have to do everything yourself. We are social animals. Community is our superpower 🫡🫡🫡

[Andreas then has the next level down from that, including power banks and Starlink](https://x.com/stuhlmueller/status/2110048778942284149).

Things are going to get worse before they may or may not get better.

> [Casey Handmer](https://x.com/CJHandmer/status/2112931082836607452): Fascinating stuff. I’m not an expert, but I remember that dodgy CAs have been a known problem since at least 2010, data retention/version control leaks at least as long, and PHP has always been adjacent to self harm. It’ll be interesting to see where we land in 12-18 months on this stuff.
> 
> [Casey Handmer](https://x.com/CJHandmer/status/2112944369238204422): Just going to preregister here that I believe the computer security overhang is not a few dozen bugs that get patched and then we’re good, there are 100,000s of vulns that are extremely discoverable with infinite free tokens and we’re probably going to have to move away from systems that presuppose that perfection is possible.
> 
> [Patrick McKenzie](https://x.com/patio11/status/2112999358295838951): I think if we didn’t have agents to do remediation we’d currently be looking about about, oh, $500 billion or so in engineering costs in the US alone backfilling software security issues against \*checks notes\* substantially every deployed system in every industry.
> 
> So its a bit of a good news, bad news situation.
> 
> I’m absolutely prepared to be told that $500 billion is an undershoot, FWIW. Google getting religion on security post Project Aurora was, round numbers, $10 billion.
> 
> And so my finger to the wind is “OK, Bank of Bigness is good for $10B, there are ten of them, that’s $100B, probably at least ratable across the rest of the economy.”
> 
> But honestly would not be surprised if it is an undershoot.
> 
> It is relatively well-known that you can successfully read from a variety of computers by listening to them carefully. It is not yet obvious whether you can successfully write to them by playing a carefully constructed MP3 file.
> 
> But pretend we are in the world that sucks.
> 
> If we are in the world that sucks, and it is in fact possible to control a medical device by being close enough to it to play an MP3 file, then there are tens or hundreds of thousands of devices which kill someone if an MP3 file is played in the vicinity.
> 
> What would we do? One available answer is “Do nothing prospectively, harshly punish people who intentionally exploit that, and lean on Chinese government to lean on Tiktok to please add some jitter to playback in future.”
> 
> Another on is “\*sigh\* Recall immediately. Recall all the things.”

An excellent point from Dean Ball: Either you believe in ‘bottlenecks’ and slow diffusion, or you do not. You cannot declare ‘everything is fine’ unless you wait long enough to verify they are not becoming non-fine. Partly this is bottlenecks, but a lot of it is purely that diffusion and figuring out how to use the new tools takes time and iteration and People Don’t Do Things.

> [Kelsey Piper](https://x.com/KelseyTuoc/status/2111530949632737494): I think this was an interesting point to make but has aged incredibly badly with three significant likely AI-enabled cyberattacks in the ten days since it was posted. \[[South Korea](https://reuters.com/world/suspect-behind-south-korea-bank-hacks-may-be-26-year-old-china-cybersecurity-2026-10-08/), [France,](https://npr.org/2026/10/15/nx-s1-6001732/france-investigates-cyberattack-that-hacked-retailers-refrigeration-systems) [Open Code](https://x.com/opencode/status/2111519637049319818)\].
> 
> It was very fair to go “hey, we’re hitting the point where we should be seeing open source AI enabled cyberattacks at scale, where are they” but I think the answer is in fact “yes, we’re seeing them”.
> 
> [Dean W. Ball](https://x.com/deanwball/status/2111805714431644063) (OpenAI): There are people who say “the changes from AI will take longer than you think because <bottlenecks and institutions and other broad abstractions>,” who also were inclined to believe that AI cyber was an exaggerated risk after GLM 5.3’s weights were public for ~days. This seems like motivated reasoning; you cannot say, “ah, you shouldn’t worry about AI risks overwhelming us through speed alone, because <bottlenecks and diffusion>,” and then also make pronouncements about AI risks after a few days of evidence.
> 
> Generally I sympathize with the <bottlenecks> view of the world by the way.

The full [version of this looks](https://x.com/natolambert/status/2107840567040262624) like ‘because GLM-5.3 is a stronger cyber attacker than previous open models, and the sky did not fall in the first few weeks after its release, that must mean that open-weight Mythos in April would have been fine’ or doubling down on ‘[well these particular breaches are fine and due to stupidity.](https://x.com/natolambert/status/2111532075501408285)’ This is what you would expect to see if things were slowly moving towards being not fine, despite months of head start.

Also, no, GLM-5.3 does not fully have The Juice that Mythos and Astra have. That day will come, and GLM-5.3 is the best cyber offense open model, but I believe GLM-5.3 is still substantially below the April line for this purpose, and thus remains more than six months behind even in ‘fast follower via mass fraudulent distillation’ mode.

[The funniest fail was eMudhra.](https://x.com/AnzalAbidi/status/2112802425052754183)

> [Pirat\_Nation](https://x.com/Pirat_Nation/status/2112828045937475868): eMudhra, an Indian certificate authority, has had 8 private security keys compromised …
> 
> The keys were incredibly weak. One of them was literally just “4”
> 
> The keys could have been used to create fake HTTPS certificates and make malicious websites appear legitimate.
> 
> Chrome, Firefox, Apple and Microsoft have blocked the affected certificates. Older devices, software and apps may still need updates.
> 
> [0.005 Seconds](https://x.com/seconds_0/status/2112923228981318119): [WHAT DID RANDALL KNOW](https://xkcd.com/221/)
> 
> ![](https://substackcdn.com/image/fetch/$s_!q951!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21a91719-e23f-4314-abb6-18ae7a073f94_400x144.png)
> 
> [James Austin](https://x.com/JimmyAustin/status/2113336584007197182): shit shit shit shit
> 
> [
> 
> ![](https://substackcdn.com/image/fetch/$s_!E-VW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d7a8141-4a99-41dc-8810-6890cb576cc4_1200x800.jpeg)
> 
> ](https://substackcdn.com/image/fetch/$s_!E-VW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d7a8141-4a99-41dc-8810-6890cb576cc4_1200x800.jpeg)

[Sam Jarman](https://x.com/samjarman/status/2113358991841767652):

[

![](https://substackcdn.com/image/fetch/$s_!0rnF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5ff9d03-06fb-4a64-83b9-aa8de419dd3e_1036x1026.jpeg)

](https://substackcdn.com/image/fetch/$s_!0rnF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5ff9d03-06fb-4a64-83b9-aa8de419dd3e_1036x1026.jpeg)

Given the long history of PHP, four vulnerabilities might or might not count as a lot.

Thus, we are in a situation where we have both rapid diffusion of use of AI in cyber, both offensively and defensively, and also rapidly improving model capabilities. This is all coming into a world full of extremely buggy and terrible code.

The result is a loop feeding on itself and going vertical.

> [calle](https://x.com/callebtc/status/2113212220712604116): I'm tired boss
> 
> [Nick Dobos](https://x.com/NickADobos/status/2113430301183823901): 3% of “critical” software security bugs, in all of recorded history, have been found in the last month.

[

![](https://substackcdn.com/image/fetch/$s_!PPUR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86512374-5343-410e-90f2-325210fd778c_1200x715.jpeg)

](https://substackcdn.com/image/fetch/$s_!PPUR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86512374-5343-410e-90f2-325210fd778c_1200x715.jpeg)

> [Zach Weinersmith](https://x.com/ZachWeiner/status/2113259300147929108): Not an ai apocalypse doomer or whatever, but entering a world where the normal operation of cybersecurity is vast swarms of hacker bots battling vast swarms of defender bots 24/7 at a scale beyond human comprehension doesn’t seem like a \*great\* path forward.
> 
> [Yo Shavit](https://x.com/yonashav/status/2113280842822713573/history) (OpenAI Foundation): speaking frankly, ai and ai chipmaker companies kicking off a red queen race that forces everyone to buy their products is Not A Very Ethical Way To Make Money even if you think it was eventually inevitable, and fighting attempts to slow the red queen race is Much Worse.

It is not an especially ethical business model. It also might be unavoidable. We have passed the Point of No Return on swarms of attackers and defenders battling it out on cybersecurity, and the defenders had better mostly win.

Would it be worse to try and slow down the red queen race? That depends on the details of how you would do that. I think we should be trying to slow it down.

Anthropic’s CISO speaks truth:

> Jason Clinton (March 8, 2024): Fully automated vulnerability research is changing the cybersecurity landscape. Claude 3 Opus is capable of reading source code and identifying complex security vulnerabilities used by APTs. But scaling is still a challenge.
> 
> [Jason D. Clinton](https://x.com/JasonDClinton/status/2090543566682718542) (August 20): The vulnerability tsunami is coming in just a few months and there won’t be enough time to patch critical infrastructure. Network isolation described below (air-gaps and data diodes!) needed now!
> 
> [Jason D. Clinton](https://x.com/JasonDClinton/status/2113325263157395456) (October 22): as bad as things have gotten in the past 4 days, they are going to get a lot worse before they get better. security leaders, never let a crisis go to waste: please go to your boards and ask for help right now. not for ai, for the basics. (we need to hold on for ~18 months.)
> 
> [hina ansari](https://x.com/hinapansari/status/2113362687866400775): You and your cohorts created this monster. Now you want us to help you clean it up.
> 
> [Jason D. Clinton](https://x.com/JasonDClinton/status/2113363809629020374): yes. it was always going to be this way. we tried to warn the world.

He was not the only one giving out warnings.

> [Dean W. Ball](https://x.com/deanwball/status/2113584460075876628) (OpenAI): We tried to warn the world and far too often, to be frank, we were yelled at for doing so. “Regulatory capture,” “marketing hype,” “doomer anxiety,” “fear-mongering about open source,” “why don’t you talk about the benefits?”
> 
> “we” here includes the broader ai policy world too. most of the time when I personally warning people, I was a policy researcher at a think tank or in government, not a lab.

‘We’ includes not only the AI policy world, but also before that the AI safety world.

As in, there are those who said ‘we are building the cybersecurity vulnerability exploiter from the cautionary tale…’ and then those who were saying ‘here is a cautionary tale saying we should not build the cybersecurity vulnerability exploiter,’ and then the Usual Suspects accused everyone involved of lying so they could Do a Hype or a Regulatory Capture.

So yes. They did try to warn us. They are still trying to warn us. They, along with all the other major labs and tech companies, are also doing their best to help us get through this, given the capabilities available.

Also they are still increasing the capabilities available, about as fast as they can.

[How should we think about the PHP bug and a number of other issues being found by 5.6 Sol](https://x.com/tszzl/status/2112967217323422069) instead of Mythos or a current frontier model?

> [Nate Soares](https://x.com/So8res/status/2112959457001119766) (MIRI): It’s striking that this vulnerability was found by Sol and Argon rather than being found and fixed in the wake of Mythos 6mo ago. Seems like a heavy strike against the “defense will run ahead of offense” theory, especially give that domains like bio are much harsher than cyber.
> 
> I think glasswing failing to find this one for 6mo+ is an indictment of the theory (that defense can outpace offence on relevant timescales) essentially regardless of the difference between the models.
> 
> [Drake Thomas](https://x.com/MaskedTorah/status/2112984657704751375) (Anthropic): Agree this is a negative update on defense/offense balance dynamics in cyber but I don’t think this really affects any of my views on bio - what would the analogous bio update be that people haven’t already priced in?
> 
> [roon](https://x.com/tszzl/status/2113117685886386578) (OpenAI): this is just wrong: these vulns were found by defenders using Daybreak rather than attackers. It’s just evidence Glasswing didn’t go far enough, possibly due to capacity constraints. It’s also very likely that March Mythos was not as good as Sol/Astra of September.

Roon is correct that the vulnerabilities were first found by defenders. If that had not been true we could be in a rather royal mess right now.

This does not invalidate the central point from Nate Soares. Nate is pointing out that the vulnerability was not found by Glasswing for many months, and then found using a model that was behind the public frontier, rather than being found in advance of attackers getting such capabilities. That means that attackers could plausibly have found it first.

That defenders happened to get there first in this case is helpful, but not as reassuring as one would like it to be. A particular reason is that defenders actually had a full 11 week lead, as the defenders found this bug on August 1, yet this took so long that we started to see exploitation on October 17. If we need more time than that, we are cooked.

I think this is an update against defenders being advantaged, and it is [distressing to see people calling Nate’s statement ‘disinformation.](https://x.com/BlancheMinerva/status/2113263852582486465)’

> [Vitalik Buterin](https://x.com/VitalikButerin/status/2113078532125622577): I didn’t predict and do not predict defense running ahead of offense automatically. I predict cybersecurity will be endgame defense-favoring but the transition will be hard.
> 
> In particular, “good guys find vulns in already-released software before the bad guys do” is not a defense-favoring game. Making the game defense-favoring requires deeper shifts in methodology including formal verification, aggressive TCB minimization, etc, and we’ve only barely started making those transitions.
> 
> (This distinction is a big reason why I continue to be friendly toward slowdowns/pauses, and we need >1% of GDP going toward cyber + bio + physical world hardening)

[China has realized there are some issues involved in all this and have solicited comments on revising their AI export controls](https://www.mofcom.gov.cn/zwgk/zcjd/art/2026/art_b11d5c1e9374421e93e85dc87eba6e38.html). They are just like us.

Eventually there is going to be a clash between ‘we encourage open models’ and ‘but you cannot let the wrong people get \[X\].’ You can’t make an open frontier model not \[X\], or meaningfully apply ‘export controls’ to it.

In this case the primary \[X\] is ‘malicious code generation’ and that is especially impossible to prevent if you want your model writing good code. So you get continuous statements that say both ‘yay models’ and ‘but not \[X\]’ and eventually something will have to give.

> Chinese [Ministry of Commerce](https://www.mofcom.gov.cn/zwgk/zcjd/art/2026/art_b11d5c1e9374421e93e85dc87eba6e38.html) (translated from Chinese): This public consultation involves 40 key technologies proposed for addition to the list in three fields: artificial intelligence, biomedicine, and photovoltaics.
> 
> Among them, 14 technologies are proposed to be prohibited from export, including: AI-driven malicious code generation and mutation technology, cell and gene therapy technology and process platforms with independent intellectual property rights, and perovskite and tandem solar cell module production technology;
> 
> 26 technologies are proposed to be restricted from export, including: AI-assisted vulnerability mining technology, general-purpose cell and gene therapy novel target discovery and verification technology with independent intellectual property rights, and polysilicon engineering technology with a single-line capacity of ≥30,000 tons/year.
> 
> …
> 
> 1.  the scope of control is precise and limited.
>     
> 2.  facilitation measures are applicable.
>     
> 3.  dynamic adjustments are implemented.
>     
> 
> … **First, it is crucial to ensure the safety and controllability of artificial intelligence (AI) technology.**
> 
> The various inherent and derivative risks arising from AI have drawn significant global attention. The AI-driven malicious code generation and mutation technologies proposed for regulation could be used to attack critical national information infrastructure, defense and military industries, core government systems, or to bypass national security defense systems.
> 
> If acquired by non-state actors or malicious entities, they could endanger national security and the common security of humanity. The Chinese government’s necessary management of these technologies aims to solidify the security baseline, prevent misuse and abuse, ensure that AI remains under human control, and promote international governance of AI.
> 
> **Second, we encourage open source, open collaboration, and resource sharing.**
> 
> **…** For AI technologies classified as restricted, overseas localization deployment falls under the scope of technology export management; however, if deployed in relatively controllable situations such as overseas self-owned clouds, convenient measures such as automatic licensing may apply.

[Corbin Duncan calls this a ‘big step towards closing the Chinese frontier](https://x.com/kuhhbin/status/2111053316796924316).’

Dean Ball’s take seems correct here. China is creating optionality, and drawing a date after which you need to ask permission more formally. They do not themselves know if and when they will use it.

> [Dean W. Ball](https://x.com/deanwball/status/2111150928997019765) (OpenAI): This move does not mean “China is shutting down open-weight models,” but it does indicate the Chinese government establishing the optionality to shut down future open-weight models at will. It’s also a mirror image of the model-weight export control regime USG has already used.

One big argument you hear is between these two claims: That we need defenders to have differential advantage, and that we need to diffuse capabilities as quickly as possible to everyone.

> [Dean W. Ball](https://x.com/deanwball/status/2113317681436688412) (OpenAI): Everyone should be looking for data points to advance the longstanding debate in AI policy between “diffuse dual-use capabilities rapidly so the good guys can defend themselves” and “restrict capabilities proliferation to only carefully vetted good guys.” We are putting the former position to the test as we speak.
> 
> No motivated reasoning to reach your preferred conclusion; just pay attention and update as appropriate in whatever direction seems true. This is much too important for low-fidelity tribal polarization.

I see the argument for the second position, ‘spread dual-use capabilities far and wide,’ as being that we are going to do that anyway so we had better do it now, instead.

I do not think that is a good argument, or likely to end well, even if you despair and think there is no way we can stop capabilities development or diffusion for long.

That still leaves the puzzle of how to get the largest differential advantage for defenders, given control over some but far from all key decisions.

You need to strike a balance between how many people you trust to what extent and thus give a leg up, versus the risk that they cannot be trusted.

My current read is that we are being far too conservative about who gets access to the tools for defenders. I think we misunderstand the threat model. The situation is mainly not ‘one rogue actor gets their hands on Mythos for a day and all hell breaks loose.’ It is more like ‘those with access to dangerous capabilities continuously ramp up amount of hell breaking loose.’ It also seems likely that proper monitoring and classifiers can tell us if and when one of the accounts get compromised.

Even pure ‘KYC we can trust and someone we are confident we can throw in jail’ goes a long way. I expect us to get better at this balance over time.

Alternatively, we actually do offer it on that basis, as in Daybreak giving you access in 15 minutes, except no one knows to ask. We need to not wait for them to ask.

None of that matters if open model capabilities outpace our ability to patch. We should be committing far more resources to patching, and many are trying, but companies and individuals mostly cannot be forced to get in line. Ideally I’d like to give them more of a swift kick, perhaps by the threat of white hat probes backed by mandatory large bounties.

This last week of greater Hackening is plausibly in large part due to the new DeepSeek model. It is not frontier, but it is fast and cheap and pretty good, and that likely is tipping the calculus for many. Now we have a potential new Kimi problem as well. The good news is that Kimi claims to have intentionally held back on the cyber capabilities. Open model advocates will need to accept such things, and other restrictions, over time, and China will provide.

A lot of the damage we are seeing is accumulated damage, and a lot of what people are doing seems opportunistic and not well resourced. Thus, a strategy of ‘make doing attacks and using the good models maximally annoying’ as an additional ‘security through obscurity’ strategy might last longer and buy more time than you would think. Eventually the top bad guys scale without limit and none of that matters, the same way that so many things will stop mattering after superintelligence. For now, we need every advantage we can get.

On a personal level, I would urge taking ordinary precautions in Peter Wildeford’s list.

Again:

> \* use a good password manager (1Password) and do not duplicate passwords  
> \* use two factor auth for everything important (not via sms!! Google Authenticator or better yet YubiKey)  
> \* Auto-updates on, and restart weekly so they actually install  
> \* Freeze your credit  
> \* Get an IRS Identity Protection PIN  
> \* Get your cell carrier to give you a port-out PIN or number lock that makes the carrier refuse to move your number without the PIN

Assume that things will get worse before they get better, and that there is a long tail of potential ways things could get quite bad. But please do not panic. Do not cancel trips, avoid airplanes or anything like that. Remember this is a long haul problem, not an acute crisis. You want precautions that you can sustain.

As with many such things, you do not so much need to outrun the bear as much as outrun the other people, at least in the opening rounds. Then you need to prepare for other things to get taken down.

No posts