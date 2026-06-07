---
title: "GitHub's plan for Agents — Kyle Daigle, GitHub"
title_zh: "GitHub 的 Agent 计划：Kyle Daigle 谈 Copilot、Actions 与企业级上下文"
author: "Latent.Space / swyx; guest: Kyle Daigle"
author_title: "Latent.Space / GitHub COO / Microsoft Developer CMO"
publish_date: 2026-06-02
saved_date: 2026-06-07
original_url: "https://www.latent.space/p/github"
slug: "latent-github-plan-for-agents"
source: "latent.space"
fetch_status: "ok"
fetched_at: "2026-06-07T05:32:59+00:00"
fetch_type: "html"
content_length: 92568
tags:
  - "GitHub"
  - "Copilot"
  - "AI Agents"
  - "软件工程"
  - "企业 AI"
---

# GitHub's plan for Agents — Kyle Daigle, GitHub

> 🔗 原文：[https://www.latent.space/p/github](https://www.latent.space/p/github)

---

_I’m excited to work with Microsoft once again as the presenting sponsors of the [AI Engineer World’s Fair](https://www.ai.engineer/worldsfair/2026)!_ _We’ll streaming live from [MS Build](https://build.microsoft.com/) today for a special crossover pod with [our friends at No Priors](https://x.com/saranormous/status/2061681787169017949?s=20) and the one and only **Satya Nadella**. However we did not hold back with this interview - we asked all the burning questions about uptime and Copilot that we know you have in your minds. Lets go!_

For almost two decades, **GitHub** has been the home of software, where both open source and closed flow, through commits, pull requests, reviews, actions, etc.

[

![X avatar for @kdaigle](https://substackcdn.com/image/fetch/$s_!5q9J!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1775869471074258944%2FGJGhWau0.jpg)

Kyle Daigle@kdaigle

Happy 🍰 Day, GitHub! I'm celebrating our birthday with the story about how defunkt, co-founder of GitHub, turned me down for a job 18 years ago after their launch... but it all worked out. 🤣 On this day 18 years ago, GitHub was officially launched by defunkt, @mojombo,

![](https://pbs.substack.com/media/HFiCnT1akAM2OHh.jpg)

12:33 PM · Apr 10, 2026 · 21.9K Views

16 Replies · 18 Reposts · 243 Likes





](https://x.com/kdaigle/status/2042581612400120093)

This ecosystem flourished as open-source maintainers and contributors would continue shipping code for the benefit of the community. However as coding agents began to ship mass quantities of code - **growing 1400% in 2026**, it marked a new era that was both extremely exciting and challenging for GitHub.

[

![X avatar for @kdaigle](https://substackcdn.com/image/fetch/$s_!5q9J!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1775869471074258944%2FGJGhWau0.jpg)

Kyle Daigle@kdaigle

Yup, platform activity is surging. There were 1 billion commits in 2025. Now, it's 275 million per week, on pace for 14 billion this year if growth remains linear (spoiler: it won't.) GitHub Actions has grown from 500M minutes/week in 2023 to 1B minutes/week in 2025, and now

![X avatar for @ThePrimeagen](https://substackcdn.com/image/fetch/$s_!DKVJ!,w_20,h_20,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1924503772094517249%2FDfKkH0ph.jpg)

ThePrimeagen @ThePrimeagen

I would like to make my apologies for defending M$, but I must from time to time. I have to put respect on github for handling the amount of shit code that has been added over the last 3 months. literally 10s of billions of lines of code that will never see the light of a CPU

8:29 PM · Apr 3, 2026 · 2.62M Views

156 Replies · 569 Reposts · 7.14K Likes





](https://x.com/kdaigle/status/2040164759836778878)

While these agents help more people ship more projects, they also significantly increase the floor of how much code is shipped, how often it is shipped, how many people commit code, and basically orders of magnitude multiples in every dimension of GitHub infrastructure:

Now GitHub inevitably experiences more pressure on their infrastructure which was originally designed around human developers moving at human speed. This has resulted in a very publicly notable uptime story:

[

![X avatar for @SapphoSys](https://substackcdn.com/image/fetch/$s_!GKcK!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F2037174241318338561%2F2ijI6Zlz.jpg)

chloe 🐇@SapphoSys

world's first enterprise solution to reach zero nines uptime

![GitHub Platform: 89.91% uptime](https://pbs.substack.com/media/HE5aUPyaYAAwwFH.jpg)

11:31 AM · Apr 2, 2026 · 620K Views

120 Replies · 474 Reposts · 12.6K Likes





](https://x.com/SapphoSys/status/2039667138198372591)

So it begs the question of whether current systems around code can absorb what AI produces. Can CI/CD keep up when every idea becomes a build? Can open source maintainers survive floods of AI-generated slop contributions? Can GitHub preserve the human social contract of software while becoming the operating layer for agents?

Which brings us to the perfect person to answer these questions: **GitHub COO Kyle Daigle.** In this episode, he joins swyx to unpack what happens when AI doesn’t just autocomplete code, but starts changing how companies operate, how open source works, how pull requests get reviewed, and how GitHub itself has to scale.

We go deep on **GitHub’s internal AI workflows**: micro-skills, WorkIQ, MCP, Slack, Teams, email, Copilot workflows, the new Copilot desktop app, CLI, cloud agents, and how Kyle **uses agents to look backwards across company context before deciding what to do next.** Kyle also reflects on GitHub’s history building webhooks, APIs, Actions, npm, Dependabot, and Semmle, why the AI era is breaking GitHub in new ways, how Actions became a general-purpose compute layer, and what Copilot becomes after code completion.

**We discuss:**

*   Kyle’s **expanded role** across GitHub
    
*   How AI got Kyle **coding again** after years in leadership
    
*   Why GitHub rolls out AI through **existing workflows** instead of forcing new tools
    
*   WorkIQ, MCP, Slack, Teams, email, and GitHub as **company context**
    
*   Why massive “mega-skills” are giving way to small, **atomic micro-skills**
    
*   How AI changes **summarization, communications, marketing**, and analyst work
    
*   Why former developers in leadership may have a **unique advantage** in the AI era
    
*   Kyle’s **“15 agents on Saturday”** workflow
    
*   How Kyle built an **AI-generated executive presentation** for CRO/CFO teams
    
*   Why AI changes the **chief of staff role** without removing the human work
    
*   GitHub Actions, webhooks, arbitrary code execution, and **secure agent compute**
    
*   The npm acquisition, **supply-chain security**, 2FA, and token invalidation
    
*   Slop forks, vendoring, and whether AI agents change **dependency management**
    
*   What pull requests become when most PRs come from **agents**
    
*   Prompt requests, vouching, AI review, and **trust in open source**
    
*   What counts as a “developer” when AI lowers the **barrier to building**
    
*   GitHub Spark, low-code, and why GitHub refuses to **hide the code**
    
*   **14x commit growth**, Actions load, databases, monorepos, and availability
    
*   Copilot’s evolution from completion to **CLI, desktop app, cloud agents**, and SDK
    
*   Context, memory, rules, and making GitHub **“act like Kyle wants it to act”**
    
*   Ambient AI, OpenClaw, enterprise security, and the **new operating system for agents**
    
*   What swyx should ask **Satya Nadella** about Microsoft’s AI future
    

**Kyle Daigle**

*   **LinkedIn:** [https://www.linkedin.com/in/kyledaigle](https://www.linkedin.com/in/kyledaigle)
    
*   **X:** [https://x.com/kdaigle](https://x.com/kdaigle)
    

**00:00:00** Introduction

**00:03:36** Why AI Got Kyle Coding Again

**00:07:04** Running GitHub with AI: WorkIQ, MCP, Slack, Teams, and Skills

**00:15:39** The Golden Age for Former Developers in Leadership

**00:17:31** 15 Agents on Saturday and AI-Generated Executive Work

**00:20:20** How AI Changes the Chief of Staff Role

**00:21:45** GitHub’s History: Actions, npm, Webhooks, and Open Source

**00:28:45** Slop Forks, Vendoring, and AI Dependency Management

**00:33:57** Pull Requests, Prompt Requests, and Trust in Agent-Generated Code

**00:41:21** GitHub Stars, 200M+ Developers, and the New AI Builder Wave

**00:45:15** GitHub Spark, Low-Code, and Why GitHub Still Shows the Code

**00:47:38** GitHub’s Hardest Era: 14x Growth, Reliability, and Scale

**00:59:21** Actions as the Compute Layer for CI/CD and Automation

**01:02:04** The State and Future of GitHub Copilot

**01:08:24** Ambient AI, Background Agents, and the Future of the SDLC

**01:13:09** OpenClaw, Enterprise Security, and the New OS for Agents

**01:18:03** Build Announcements, WorkIQ, FoundryIQ, and Microsoft Context

**01:21:41** What Should swyx Ask Satya?

**Swyx \[00:00:00\]:** We’re here with Kyle Daigle, COO of GitHub. Welcome.

**Kyle \[00:00:07\]:** Hey, thanks for having me.

**Swyx \[00:00:08\]:** You’re not just CEO of GitHub. People know you as that. You have a new role.

**Kyle \[00:00:11\]:** So I have an expanded role now. I’ve been working at GitHub for thirteen years and doing all things developer. Joined as a developer myself. And now, I’m also responsible as the CMO of Developer for Microsoft. And so all the kind of learnings and passion for developers and how we work with them and how we communicate and how we bring our products to market, we’re also bringing that expertise to the broader Microsoft ecosystem and helping every developer that uses a Microsoft product or would like to have a sort of similar experience that they’ve had with GitHub over the years. So it’s a different role in some ways, but it’s also just building on the experience that I’ve had at GitHub of just sort of tell the truth, be authentic, show people how to use it and then let the products speak for themselves. Now just doing that with, all of Microsoft.

**Swyx \[00:01:09\]:** We’ll be releasing this in conjunction with Build. You got lots of stuff planned, and we can sort of touch on that whenever it’s appropriate. I think one of the interesting things is I rarely meet a COO who’s also a CMO. I think you’re a very outward facing and you’re very confident publicly. That’s rare. Do you actually view yourself as COO? What’s What is your thing?

**Kyle \[00:01:33\]:** I think for me, it’s been funny. The titles have always been, a— have always felt a little strange to me. I joined GitHub as a developer? I wrote so much of the

**Swyx \[00:01:46\]:** Let’s bring that up. You wrote the back ends?

**Kyle \[00:01:48\]:** I was going through, I was going through, some old photos, when folks were talking about how things were being built or how there was a build GitHub. I built, webhooks and worked with teams building the API, built the platform layer. Anything that integrated with GitHub, up until really twenty eighteen, I built or ran the engineering teams. And that’s kind of where my the beginning of my passion always was helping people build things, deliver them to, their customers. And so being a developer, building for developers was always super unique. In a— I think as my role expanded, it became my ability to talk to not just developers, but also enterprise customers or business leaders and have this translation layer. And then through all those years, GitHub has always operated pretty uniquely. Post-pandemic, working remotely was not as novel as it was when GitHub started in two thousand and eight. But all that expertise of running remote teams, doing it well, became this sort of bigger role, ultimately turning into the COO role of how do we operate GitHub in the way that GitHub’s always operated after the Microsoft acquisition. And kind of so on from there. So like for me, I think the— I’ve, I still code. I love coding but the problem has always been, people. It’s a much harder problem to both support our own employees, a harder problem to communicate to developers and enterprise buyers what we’re building why it matters, ‘cause those are two very different messages. And so getting to work in the mix of COO, CMO, also just being a dev, I think is what’s kept me at GitHub for so long.

**Swyx \[00:03:40\]:** Apparently, you have— your commits have gone up. What’s this? What’s going on?

**Kyle \[00:03:45\]:** Rui’s called me out pretty aggressively. So I think— as you can imagine, right, you can see my normal era of being a dev In the twenty thirteen, twenty fourteen era, and then moving into management, and then ultimately the COO role. I think what you see there is me, really getting back to coding thanks to AI. I— similar to, attaching problems between how to market and how to operate a business and how to code, I find, building agents and workflows that are connecting very disparate problems to be what’s driving this. So that’s, some of it’s writing software. A lot of it is, connecting a ton of a different data sources to, help me out. But that is completely me really diving in on the AI side in trying out our tools, trying out everyone’s tools, But building for me, building for the non-technical leader, though I’m technical and how we’re, able to use these tools more than just the simple, call and response that I think a lot of the non-technical, your employers, you have to get— you have to use AI, and so everyone uses, ChatGPT or Copilot or Claude or whatever. To really get into, how is this going to help me out, it— I find that it’s not the I need to write a blog post, I need to those simple examples. Helping people find the workflows of, “Okay, I need you to go through all the PRs today. I need you to go through everything that we’ve posted online. I need you to go through what we did the last three months. Go through all of my Obsidian notes for any mentions of this then go through my transcripts at work.” We use, Teams, so, using WorkIQ, go call that MCP server, grab all the transcripts, go through all the Slack, and then build me out the plan of, what this week’s messaging actually was. That’s something that was, impossible because for me, I find AI in a what most of this launch here is actually, less building forward. It’s actually, a recursive loop backwards. I’m always looking at what had happened first. Go back through the week and tell me what we did, what worked, what didn’t work? And then tell me in the next three or four days-What would you tweak based on this sort of like looking backwards and then looking ahead a little bit? I find that to be so much more valuable, especially for like non-technical, because that retrospection is actually LLMs are very good at that. Like finding all the patterns, pulling them out, and then applying that retrospection to just a couple of days or just like a short period of time. Is all a bunch of apps that I’ve built and launched a bunch of, internal tools. I use the new, GitHub Copilot app, the desktop app with workflows. Every time I crack open my laptop, it’s running workflows for me. It’s just a ton of different stuff and of course, it all ends up on, it all ends up on GitHub.

**Swyx \[00:06:47\]:** Of course. That’s where, that’s where, stuff is hosted. Man, there’s so much to ask you. I was going to leave the how do you run a company with AI thing at the end. I have to ask one— double click one thing. You said, you are looking back at the week. You’re, you’re understanding what happens. When you say we That’s three thousand people. How?

**Kyle \[00:07:09\]:** I think when we started rolling out AI internally beyond engineering, right? One of the things that I was really, passionate about is like we have to do this in a way where no one has to change how they work. I don’t want to have to teach you a tool. I don’t want to have to teach you something new. And so for us, we tried out a few tools. Most of them don’t work because I got to get you on board? I got to teach you how to use it. What we’ve actually ended up doing is we’ve built like a set of skills internally. We have we each have our set of skills, and we’ve just been distributing even to the non-technical folks, the CLI. And then effectively, we’re just giving it access to like read about everything that we’re writing. So that’s for us, that’s usually GitHub, Teams, Email, and Slack. So Teams for, video chat, generally speaking.

**Swyx \[00:08:03\]:** Teams and Slack?

**Kyle \[00:08:04\]:** so we use Teams for video communication, but we don’t use it for chat. W-we— GitHub for a long history, right? We’re always

**Swyx \[00:08:13\]:** Also Slack

**Kyle \[00:08:14\]:** Talking about ChatOps and like everything is built into Slack. Like every command, every flow.

**Swyx \[00:08:18\]:** So even though you have been acquired for I don’t know, eight years now

**Kyle \[00:08:22\]:** we still

**Swyx \[00:08:23\]:** You still use Slack?

**Kyle \[00:08:23\]:** it’s a purpose-built tool for us, and I think the reality is that moving off of it would be so bluntly expensive? Simply because all the tooling is, baked in with that paradigm. And they both have their pros and cons but they don’t work the same way at all. We still use a bunch of different tools Because it’s the purpose-built tools that We need. And then

**Swyx \[00:08:47\]:** Well, the same doesn’t go for the rest of Microsoft, presumably.

**Kyle \[00:08:50\]:** like the like various teams like operate

**Swyx \[00:08:53\]:** They make their own decisions

**Kyle \[00:08:54\]:** Various ways. I think it just matters what you’re trying to what you’re trying to do. But we do we do work across kind of every tool that we use, and then by giving everyone access to all of that context and the new WorkIQ MCP server, which is quite cool if you do live in the M365 like world. I can ask it all these backwards-facing questions, and it’s incredibly important for our teams that are working remotely. There’s a lot of stuff you miss when you’re not in an office, and we are spread out all over the world. So most of that is looking back. And then we post, we post either auto-automatically into GitHub issues or discussions, these sorts of like findings or like our industry reports. Like what’s happening this morning, today, yesterday. A little automation gets run. We’ll use the app. We might use GitHub Actions like with, our agentic workflows just to go do that run, and then we push it into GitHub, and w-we keep having a conversation. So usually for us, it’s about that sort of like looking back, looking forward on the non-technical side. And then of course for a lot of those folks, it’s also building an app, pushing it to GitHub pages or pushing it somewhere to host it et cetera. But it’s just like enabling everyone with that power of it’s going to take me a week to figure this out. Instead, we’re going “Okay I built a skill. Let’s put it into a repo. We’ll all share that skill together, and then we’ll use the CLI or now the app-” “just to run it.”

**Swyx \[00:10:26\]:** All right. I think, I think we’re going straight into like the team management and productivity thing. I think a lot of people are getting various levels of LLM psychosis. How do you manage the bloat of skills? Like everyone Has their thing, and they’re Like trying to promote it to the rest of their peers in their org, right? And obviously, whoever becomes a skill influencer internally becomes like an AI leader, right? Of sorts. I assume you have those.

**Kyle \[00:10:50\]:** like I think we have

**Swyx \[00:10:52\]:** And I assume it’s a mess a Yeah.

**Kyle \[00:10:54\]:** there’s like I— like I think the reality is there’s two pieces. Like first is I think that we’re ending the era of these like massive, beautiful, perfect skills that are just like not any of those things. ‘cause for a while, right every tweet every day is like go download the skills, the perfectly managed thing to do this entire workflow. And I think that like what we’ve found and what— I was just with my team, this week, and we were talking about the skill side, and we’re really talking about these like incredibly micro skills that are just doing one thing for us very well Versus a skill that’s going to do I said, that full report. That doesn’t really exist on our side anymore. It’s usually how do— like a single skill that’s going to identify the most important marketing information given any MCP server. Like this is the most important thing. Less about stitch a bunch of tools together and have it produce this mega output because then weeks go by, months go by, things change, and you want to tweak

**Swyx \[00:11:58\]:** It’s brittle

**Kyle \[00:11:58\]:** Your mega skill and you’re screwed? You can’t do that. And so now we’re really just talking about the Legos we’re using and just letting the instruction book be something we’re all putting together. Whereas I think a lot of AI skills for a while have been that mega instruction book style.

**Swyx \[00:12:15\]:** I’ve, thought a lot about Postel’s law. I don’t know if that’s a term that is, means things to folks. It’s the idea that you should be liberal in what you accept and strict in what you output, right? And I think that’s like a good framing principle for skills. This is my skills, obviously on GitHub. I feel like everyone should have like how like some repos In GitHub are special repos? I feel like we should sort of reify the slash skills and everyone like give it some kind of special presentation. Anyway, so, yeah, this is one of those like download Download anything, transcribe anything, and then you can string together the atomic skills that do one thing well Into like some kind of orchestration skill that calls other skills. I assume, does that match?

**Kyle \[00:12:56\]:** I like I think so. I think that the

**Swyx \[00:13:00\]:** Summarize anything.

**Kyle \[00:13:01\]:** Like I think the- For me, summarizing something for I do communications and PR and analyst relations and marketing and customer activities, and so my summarize everything is very different for each one of those like Contexts. What ‘Cause if I’m summarizing something for an analyst, that’s a very different thing than, probably how I’m going to summarize something for like a customer meeting or an engagement. So that’s I think like the difference when we’re talking about the like the tools I might use on Saturday or the skills I might use on a Saturday when it’s just for Kyle. Yeah, those are kind of like they have an atomic actual tool underneath or maybe skill, and then Kyle cares about X. But I think when we’re talking about work and enabling the the marketers, communicators there, it’s the atomic, this is what good summarization is, and then this is what I care about as for marketing for communications For whatever. And that I think is like the interesting matrix problem when we go from like a developer set of concerns to all kinds of different professions, is that what that word means to me is different than it means to you is different than it means to the analyst or the salesperson, and that’s where I think the matrix mess is that we’re starting to like still starting to find. It’s about these mega skills but they’re all just slight permutations, but those permutations are really important. It’s the difference between someone reading this and going “Did AI make this?” what Or “This makes total sense, and I would expect this when I’m giving a briefing to Gartner,” or like whatever else.

**Swyx \[00:14:37\]:** I think the beauty of it maybe is that you don’t have to be that careful about what goes in there. It doesn’t have to exactly fit as long as it like roughly is contained in there. I used to complain about plugin hell, basically. Like when you have a framework and then you have a hundred things that you need to integrate, everyone does like the GitHub used to be bloated full of these things. And now we don’t need them anymore ‘cause now you just use skills.

**Kyle \[00:15:00\]:** And like I think the most magical thing is the just that like I can just also crack it open. Like Like yes, I could go like change the how the plugin is coded, or like I could go do that now with AI, but I think there’s just something more magical about getting a response back and being “That’s not right,” and then you just crack the skill open, you just type English words and it’s different. That building block is just, I think very unique. Once I get everyone to kind of understand how to best how to best make those changes to get the most power out of them.

**Swyx \[00:15:36\]:** Is there a— you have a your peer group that Of people like you. Is there a common framing for Something I’m feeling is, which is true, is that is this a golden age for former developers who are now in leadership? Because you can wield the tools, you would know the right words, you’re maybe not too close to the details. Doesn’t matter. But like you’re more effective than someone who doesn’t come from that background.

**Kyle \[00:15:59\]:** I think that like the secret has always been your ability to identify patterns and solve problems, and I think that for folks that like myself that don’t code day to day anymore, that has made me successful as a developer, made me successful as a COO and now CMO. And so now that I have access to get and write code, I’m now applying that sort of like pattern finding and problem solving, and I know enough still about how to then go and say, “Oh, I want to make an app, but I don’t want to break into jail or create something that’s not going to be able to work or to be deployed scale or whatever.” that ability to apply all that additional business knowledge and still code I think is what makes that so interesting to me. Slightly different than I think some of the other like technical leaders that became business leaders and now are going back to their apps and updating them. Good for them? But I think the more, much more interesting thing is, well, now I have this whole new set of expertise over ten plus years. Why not take that and use that as a developer with these AI tools? So I definitely think that makes me more powerful, but I think that’s true for like every dev as well. Most of the dev friends I still have also have some other underlying skill and passion. There’s really talented, very kind of linear computer science software devs, absolutely. I just find that the folks that came from a different career, went to school for something else, went off and did this random thing, and then became a software dev, or were a dev, did a random thing, came back. Learning that extra set of information, learning those extra skills, and now having the power of an AI where I can crank up fifteen agents on Saturday while my kids are doing lacrosse, That’s like really powerful. And I think it gets me back to that feeling of like creation, and it’s very hard to replicate that in most other senses? That first time you build an app and you click it and you show someone that’s magical. And so being able to do that not just in code, but across all kinds of different assets that’s, that’s huge. We were doing we’re doing our every year we do our revenue planning. We talk about okay, what is it going to look like for next year? And of course as you imagine, there’s, slideshows everywhere talking about what are we going to talk about, what’s the narrative, et cetera. And so as you said I’m “Okay, well, I could probably just like build something to build this and then that way I don’t have to go build the whole spreadsheet or I have to pass it to my team.” So we went through this process, and I got all the information and used the skills I mentioned. I built like a little app just to make it so I could look at some of the information in a SQLite database, more easily. And I ultimately built this entire presentation without touching any of it and I was “Okay, I’m just going to present this to our CRO, the CFO, their teams,” without mentioning I’d built it with AI. I like built a skill to make it look very much not AI driven. Just not pretty.

**Swyx \[00:19:03\]:** Like a design. Yeah.

**Kyle \[00:19:03\]:** Not pretty. But just like very clearly not AI. Kind of like don’t do anything interesting.

**Swyx \[00:19:08\]:** That’s, yeah, that is valuable.

**Kyle \[00:19:08\]:** Just go Exactly. We did the whole thing through. It used my notes from Obsidian, it used all the context I mentioned before, the plans, and Never came up once that it was AI generated.

**Swyx \[00:19:20\]:** It didn’t matter.

**Kyle \[00:19:20\]:** Never once. D It didn’t matter. And so now I take

**Swyx \[00:19:23\]:** This is a tool

**Kyle \[00:19:23\]:** I can take that tool and go, “Look, I don’t want you to go build slideshows.” They’re just helping us share information with each other. If this thing can do it With a little bit of crafting from you and then we can look at it together, awesome. There’s no value in all that extra work. I think that the ability to, make it look humanly bad and and build a little app to, manipulate the data I think is part of, that upside for devs that are now in leadership roles. Because, the thing that I feel like I said before, this that’s all a people, that’s all a people problem. I know if you’ve used a coworker or not to build a slide deck, unless you spent a bunch of time to not do it.

**Swyx \[00:20:07\]:** I know, but like it was so, I think there’s a certain charm to just being blatantly AI. ‘Cause I think that you’re well, you’re just honest about There may be mistakes here that I cannot vouch for. So how much value is there? But anyway I think, actually the real question I want to ask is, there’s a— You were a chief of staff To Thomas. And in the pre-AI world, the that job would’ve been a chief of staff job of like Can you prep me these slides and all that? And now you do it yourself.

**Kyle \[00:20:35\]:** I still, I still have a chief of staff. Because, the difference is it’s sort of the discussion every time we have some sort of technology evolution is it’s not that the jobs the roles don’t all go away, they just change? And so yeah, I don’t have someone spending all their time building out slides for me and presentations ‘cause I don’t need that anymore. But now I need that person that is able to go and find all the different connections between humans in those discussions to help me find out, okay, I should be meeting with this group and this team, and they have an opportunity, and I’m going to be in San Francisco today, I’m going to be in Seattle tomorrow. Those sorts of human connection aspects are still incredibly valuable and has always been a big part of that chief of staff role. But now just like chiefs of staff are not opening up, letters to process, they’re doing emails. What It’s the same thing. And now they’re, they’re not building out as many of these presentations because they have the the ability to have a AI take it on for, and share that with me and great. Let’s keep moving ‘cause it’s allowing us to go faster and make better decisions more quickly.

**Swyx \[00:21:45\]:** Awesome. Well, so we can dive into more sort of, Productivity insights as you go. I did want to do a little bit of a brief history of colleague and hub. Because, we started here. And then you also involved the NPM acquisition. I did, I do want to touch upon that. And then more recently, I just want to bring up to present day where we’re having uptime issues Which transparently we’ve already Addressed publicly, but we’ll, we’ll discuss in the pod. Did I miss anything? Like what, any other major highlights? Obviously, it’s, it’s a lot of years to cover.

**Kyle \[00:22:15\]:** No the I think one of one highlight was right before the acquisition closed in twenty eighteen, I got to launch the first version of Actions

**Swyx \[00:22:27\]:** Oh

**Kyle \[00:22:27\]:** At GitHub Universe. So it was O

**Swyx \[00:22:29\]:** They’re that young?

**Kyle \[00:22:30\]:** It was October of twenty eighteen, I think. Yeah. Yeah.

**Swyx \[00:22:33\]:** Gee, Jesus.

**Kyle \[00:22:34\]:** I got to I was the engineering leader on that project and got to launch that. And then, yeah, we did acquisitions of NPM you said, Semmle, Dependabot Pul Panda a whole bunch of things. That was a big

**Swyx \[00:22:47\]:** Pul Panda.

**Kyle \[00:22:48\]:** Abi is doing well.

**Swyx \[00:22:51\]:** DX. Holy crap.

**Kyle \[00:22:52\]:** Did well on DX. I and like that was a that was the big shift, after the acquisition. I had to join the sort of business side.

**Swyx \[00:23:00\]:** So I need to hit you on some of these things ‘cause you were there. Right? And how often do I get to talk to someone who was there? But yeah, Actions. Is that the number one source of security issues on GitHub?

**Kyle \[00:23:11\]:** Oh, sh I think that the number one source of, security issues is probably like all, the literal code in everyone’s like underlying repositories. I would say back further than that is, if you remember I had to show in this graph was this is, I’m, didn’t say this before, this is ultimately webhooks.

**Swyx \[00:23:30\]:** You yeah.

**Kyle \[00:23:31\]:** Like circa whatever it was.

**Swyx \[00:23:32\]:** It says Hookshot in there.

**Kyle \[00:23:32\]:** I forget. Yeah. Yeah, Hookshot’s in there. And so like back then, it says GitHub Services. Do you see, it says Hookshot FE for front end, and then it says GitHub Services. GitHub Services back in the old days, right? You we had a repository that was Ruby code, and you could write any Ruby code in there, and then we would execute that On your behalf As a service, and then that way if an if you were trying to integrate with something, it didn’t we would run it for you.

**Swyx \[00:23:57\]:** And of course no containers ‘cause

**Kyle \[00:23:58\]:** No, ‘cause it was

**Swyx \[00:23:59\]:** Well, no containers

**Kyle \[00:24:00\]:** Twenty fourteen. And so there was some isolation obviously, but it was mostly the separations on the server level. That’s like an example as long as the very old version of Pages, which ran on its own containerization infrastructure, not on Actions.

**Swyx \[00:24:15\]:** Which like all-time great product.

**Kyle \[00:24:16\]:** Pages powers the internet at this point to some degree. Those were places where like clearly there were no like issues like to my knowledge. But it was those things where I’m looking at and going “Okay, well we can’t be running arbitrary Ruby code,” like on everyone’s behalf. Then containerizing all of that up intoUh into actions now where yeah the containerization, is r-really good. The pinning most folks aren’t pinning it the like to a particular

**Swyx \[00:24:48\]:** Images

**Kyle \[00:24:48\]:** Sha, et cetera like their workflows, and so that’s a big that’s a big place Of pain for folks if they’re just doing similar to any dependency management, just V1 or newest or latest, I think. But, that journey from that day to “Okay, we’re just going to run all this arbitrary code, and, it’ll basically be okay,” to now, no, we have, really good containerization. We have a new, underlying, ag-agent, containerization, service. It’s like we’re using it under the hood. It’s through Azure. They recently announced it. The Azure, Dev Compute, but it’s, very fast, very fast compute to be able to, spin up your own cloud agents, or whatnot. We’re using it under the hood for some parts of the new,

**Swyx \[00:25:36\]:** Microsoft Dev Box?

**Kyle \[00:25:37\]:** No. Dev Compute, yeah.

**Swyx \[00:25:41\]:** Hmm. Not finding it just yet.

**Kyle \[00:25:44\]:** Oh, it’s, it’s in there somewhere.

**Swyx \[00:25:46\]:** All right. Well, we’ll cut that out.

**Kyle \[00:25:47\]:** Sorry. But with, Dev Compute, you can, run, really fast, spin up really, small VMs really quickly, so you’re doing a tool call

**Swyx \[00:25:58\]:** Same concept

**Kyle \[00:25:58\]:** Just do it containerize exact-exactly. So we’re using that so definitely moving that direction to protect us from every every piece of code that we’re ultimately running.

**Swyx \[00:26:07\]:** look, that grows into the full SDLC? Code hosting was just the start and and then it’s grown beyond that. Let’s talk about NPM may-maybe ‘cause I think that’s also, a very major point in the industry. I do think, it was looking for a home. It was, kind of struggling as a business, right? I don’t know, I don’t know how you would characterize that whole acquisition and how it

**Kyle \[00:26:33\]:** like when we were talking to the team, I think the big thing for the both of us was to find a way to keep NPM, which was basically powering the internet then and way more so now to some degree running. Keep it going keep continuing to scale. It was having scaling problems, if I recall, back at that time. They were doing some rewrites. It

**Swyx \[00:27:00\]:** that’s cute compared to now.

**Kyle \[00:27:01\]:** Well, that’s the thing is like when I’m talking to folks now, there’s there’s so many more underlying uses of NPM than there were back when we had them join in with GitHub. But that was ultimately the goal. It was really okay, we used to have pages. We have, the world’s code. Let’s make sure that we can keep NPM running well for the world. And we put a bunch of time and investment into fixing some of the underlying backend, changes, some of which we talked about some of the manifest work, et cetera. And then now, really trying to bring the the security posture of NPM up to speed. But, it is a unique challenge in that every move that we make to make it more secure will break a lot of people. And security is paramount. And also, we take it very seriously. We’re, the any time that we have a problem with GitHub or we make a change that makes us more secure but hurts, there’s, a snow day for developers or a really bad fire that they have to go put out. And so we’ve, have changed the 2FA policies. We’ve changed the way the tokens work. When we find tokens that have been exposed or potentially, exposed, we invalidate them, and

**Swyx \[00:28:22\]:** I love that feature in GitHub. Yeah, it’s great

**Kyle \[00:28:23\]:** That creates issues, but, the but that’s the thing is we’re trying to push the community, forward without necessarily, doing something that is going to break the contract that’s been for 15 years or close to it or some amount of years on NPM.

**Swyx \[00:28:43\]:** I think the— So now we’re talking about, open source and publishing. And I think there’s something here with what people are calling slop forks, which, I think Malta from Vercel is doing. And, part of me thinks, well, the way to get past any vulnerabilities, we just, let’s just get rid of the concept of NPM. And we only publish source code. And anytime you want to import it you have your coding agent look at it and then adapt whatever subset you’re going to use into your vendor it. But, the AI vendor it. Is that realistic? I don’t know. Is it— Will that solve all our security issues? I don’t know.

**Kyle \[00:29:24\]:** I don’t think it’ll solve I so Mitchell was just talking Mitchell Hashimoto Was just talking about this today, and I think that I-in some ways, it’s all all things, old or new again? Yeah, absolutely vendoring everything. Like I do I do remember twenty thirteen, twenty fourteen.

**Swyx \[00:29:42\]:** This is Yeah. Let’s, we must return to

**Kyle \[00:29:43\]:** That’s what is We were vendoring everything. We were having actual discussions around, or at least I remember we were “Should we take this full thing?” “Why is this so big? We only need this one file.” And so I do think there’s something true there where having either taking only what you need or the dependencies just getting incredibly small over time, I think will help to some degree, but it’s not going to solve the fundamental problem, I don’t think, because the vulnerabilities in an agent looking at them, there’s time and time again, there’s a million different ways in which we can convince an agent that this thing is, secure or not and pull it in. Or we can do static code analysis or runtime testing to say whether the code works or not. That is, I think, the step that needs to continue to be, invested in. The question is just on, how much scope. Should it be this enormous project that I’m pulling down, or should it be this piece? Either most companies are running some amount of security checking on the on the packages that they’re bringing in or vendoring. That I think won’t change. That’s like what advanced security does to some degree, Socket does some degree. Like everyone is doing a piece of that. How we each do that like especially when we’re talking to enterprise customers, is just like very different. No there’s no one wants one single way to do it. And I think that’s always been GitHub’s, unique position in the world. I talk a lot to maintainers, I talk a lot to folks about this. It’s we’re— we rarely start like a process and a practice and like push it onto the community. We usually wait for the sort of like RFC process socially or literally, everyone agreeing, and then we’ll cement something in. Because otherwise we’re

**Swyx \[00:31:35\]:** That fits your role in the ecosystem, yeah

**Kyle \[00:31:36\]:** We’re GitHub. Yeah, we don’t want to shape the whole thing. We want it to be figured out. But like how do you balance that like sort of Role in the industry to keep everything as secure as is possible and make sure that you’re you’re not going to be compromised as a human, ‘cause that’s usually how it all happens. And Not not create a process or lock us into a flow that you’re not going to or like Mitchell’s not going to or other open source projects aren’t going to like. That’s always been a tricky balance for us, and I think that’s something that we haven’t talked about enough is we’re not going to be able to fix everything for everyone in a way that everyone is going to like. So tell, help us, tell us what is working. When Mitchell was talking about, the Upvote, the up

**Swyx \[00:32:22\]:** I was going to bring up his thing. Yeah.

**Kyle \[00:32:23\]:** I forget what it Yeah. When he’s talking to us, I was chatting with him and talking to him about this and I put it on Twitter and we talked to, also over DM, was “We’re going to keep working.” but I think the important thing is I do actually want to hear what isn’t working for you. And as, be as specific and clear for your project as is possible. And to every piece of credit over the many years that we’ve known each other through the industry, he’s always done that and I appreciate that ‘cause there are places that we need to fix up, and we hear from him, and we’ll fix up just like we do all other kinds of maintainers. But that that process between making those types of improvements and being more secure and like creating, I forget what he calls it’s not the proof process, not the claims process. Do what I’m talking about? He has that he his projects have a way for you to kind of like,

**Swyx \[00:33:13\]:** Vouch

**Kyle \[00:33:13\]:** Vouch. Thank you. Yeah. He has like the vouch system for saying, “Hey, you should accept my PRs.” That’s been

**Swyx \[00:33:20\]:** I just built this into GitHub. I don’t know.

**Kyle \[00:33:22\]:** Well, see, but that’s the thing is that you say that and like he and his community really likes this and then I’ll go talk to other maintainers and other maintainers, globally, and they’re “No, this doesn’t work for me.” And that is the tension, but also the kind of beauty of GitHub, depending on which way you look at it is we want to help maintainers, so we create all these tools to let you have more control over how much you take in from AI and PRs. But you can also use this. What You can go use this project, and if it takes off and becomes the kind of mostly standard, then yeah, we probably wouldn’t enforce it but we would add it in because that’s the flow that we tend to do?

**Swyx \[00:34:02\]:** I hear a lot of people don’t know the history of the pull request. And like like that’s how, that’s something that GitHub standardized basically.

**Kyle \[00:34:08\]:** Yeah. It was a very messy process Like beforehand, and now the we have the benefit of it being the process? And now we have to go and Figure out the next best process or what adaptations change, or what does a pull request look like when eighty percent of your PRs are just coming from your agents and not From other devs?

**Swyx \[00:34:31\]:** Do you like the prompt request idea from Peter?

**Kyle \[00:34:34\]:** like I think that for each like each idea I think has its merits. I’m not, I’m not avoiding saying anything good or bad, but I feel like I’ve seen a version of we have that we have entire Thomas’ store. Take all the assets of what you’ve built and put that in. I think that’s got great ideas. There’s all these various permutations of the PR flow, but I think the reason why there’s not a single answer is ultimately we’re trying to codify trust. We’re trying to say “Okay, if Sean reviews this I’m going to trust it because you’re Sean or you’re the senior dev or you’re the whatever.” And right now, when we are working in a flow where an agent writes code and another agent reviews code and then Kyle goes and looks at it the trust is kind of diffuse. And most of the tools that we’re talking about are talking more about verification flows. We have more assets to look at, so I can probably say whether this is a good PR or not. But that still doesn’t solve, I think, the human problem of I’m looking at a PR and I want to know if I can trust it. And we’re still, we still tend to use human signals for that? Mitchell approving it or Kyle approving it or whatever. And so I think that’s, I think that’s why most of these options haven’t really solved it is because, it’s a social problem ultimately. It’s a it’s a human problem to review it and agree. Or you fully trust the tool and you’re imbuing that tool with full trust Which I think in some cases that absolutely exists.

**Swyx \[00:36:08\]:** And so like in the same way that there will be a tipping point in society when we don’t allow humans to drive anymore Because machines are measurably better than Than humans. I’m looking for that tipping point, right? Like Mythos is ridiculously expensive. Someday we’ll have Mythos on a desktop. I don’t know. Will, does that change the equation?

**Kyle \[00:36:30\]:** I think it’s more I took a Waymo here, and I was on my phone and not looking around at all. There are other, self-driving, vehicles that I would not trust while, staring at the road. And I think that trust is something that is

**Swyx \[00:36:48\]:** Is this a Zoox thing? What is it

**Kyle \[00:36:50\]:** I think that is both. I think that is both. Like

**Swyx \[00:36:53\]:** There’s Zoox in this robo taxi. That’s it. It’s

**Kyle \[00:36:56\]:** Well, depending on what level Of self-driving. But, my point is sort of that I think part of that is I strongly believe that’s, a mixture of verifiable proof. Like how many accidents, how much data, and so on, and the human aspect of how I feel when I’m in this car, what it tells me, et cetera. And so that’s why I think some of the like Some of these some of our AI tools tend to, imbue me with more of that feeling of trust, even if the data says this is 100% accurate. I feel like it takes more time for us to go, “Should I trust this or not?” And that’s in the soft sense of, startups with high agency, weekend projects, and open source. And then there’s enterprises and regulated industries and everything else, and that is an even harder problem to go solve because even when it is fully verified, not only do you have to have trust from the humans on the team, you probably have to have trust from multinational,

**Swyx \[00:37:55\]:** Oh my God

**Kyle \[00:37:55\]:** Multi governments around the world and regulating agencies. And so that’s where I feel like until we tip over to your point on the sort of like human EQ side of it. I feel okay this feels okay I’ve been proven enough. Then the ball will start to roll a lot faster, where we’ll end up getting to the “Okay, we can trust this,” and feel good about it in the Most difficult of cases.

**Swyx \[00:38:18\]:** If human trust is the thing that matters, I feel like GitHub as the developer social network could maybe do more there. Like vouchers are one system But, we have star counts, and then we have Contributor rights, and that’s it. And I feel like there should be more in that space. I don’t know if there’s any other design decisions there.

**Kyle \[00:38:37\]:** I think that one of the places that we don’t really expose right now in this sort of way is, some degree of like hard trust and support, which would like for me is like sponsors is a good example of that.

**Swyx \[00:38:49\]:** Ah.

**Kyle \[00:38:49\]:** It like costs you something. To prove that I believe in your project and I trust you To some degree or I want to support you at the very least.

**Swyx \[00:38:56\]:** Solve payments for open source. Why not?

**Kyle \[00:38:58\]:** I think that I think that like as we keep moving forward, right, there’s more and more projects where I’m, adding more and more dollars into sponsors personally because I want to like support them, but I also like know of I’ve probably never met them in person, but, I know of enough of their work that I want to support them. I think the thing that I don’t love about stars or commit counts or anything else is ultimately, even with all of the various, abuse and de-spamming and deduplication work that we do or anti-abuse work that we do, these are all, not active social signals. They’re passive ones that are ultimately gamifiable. And you may trust me, but another open source maintainer may not. And on what heuristic should you be, trusting me? That I think, is kind of where some of our thinking is right now. What signal from me is most important to you? You— If you can define that potentially, honestly in an agentic workflow that’s what we see some of these open source projects do, where you have GitHub actions, and then you have like an agentic workflow that’s calling AI, and you’re setting these rules. Like if Kyle has submitted and gotten accepted PRs across any given project and has a social handle tied to his account in GitHub, and that social account’s older than a certain amount. Really complex measures that matter to you ‘cause most open source projects have that heuristic built into their heads, if not written down in the contributing guidelines. You could take that and then go apply that and then just say, “Oh, we’re not going to accept this PR.” Building something that is, I think, malleable to everyone’s needs, is a little bit better, rather than going “Hmm, this account’s too young.” Because what happens? The attackers just go and go and create a multitude of accounts, and they wait Until it ages up. Needs to have a certain amount of stars. That’s how star inflation happens. Need to have a certain amount of repos

**Swyx \[00:40:46\]:** Oh my God. Yeah

**Kyle \[00:40:47\]:** With PRs. They all just create repos and submit PRs to each other, and then they come in and do something nefarious. And so, it’s hard. It’s hard to find the measure. So I think we’re, we’re looking more at how can we provide you tools so you can kind of choose what’s best for you. And of course, we’ll give you some standards. But the trust vector, gets down to I don’t know, some version of like human digital ID like everyone’s been talking about. Like how do I prove that it’s me

**Swyx \[00:41:13\]:** Give me your eyeballs

**Kyle \[00:41:14\]:** On the internet. Give me your eyeballs. Exactly.

**Swyx \[00:41:18\]:** The I got to keep moving on Topics, but obviously I can go all day on this stuff because, I’ve been involved in GitHub and open source My entire professional career. Stars. Very superficial. Everyone knows it. But I think time to one hundred thousand stars is the fastest I’ve ever seen. Like people just reached that in I don’t know, months. And then like at the same time I don’t trust it right? Like how many of these are real or bot or like whatever. I don’t know how to ask this but like what can we do about it? Like

**Kyle \[00:41:49\]:** Just

**Swyx \[00:41:49\]:** Is stars broken? Is stars fine?

**Kyle \[00:41:51\]:** I think that there’s kind of two, there’s like two pieces. Obviously we’re constantly like trying to find ways in which like your users are producing spam, which would, I would include like be like only doing star gamification. When we find them, we pluck ‘em out and we,

**Swyx \[00:42:08\]:** But it’s like a Whac-A-Mole

**Kyle \[00:42:10\]:** It’s a hundred percent like a Whac-A-Mole

**Swyx \[00:42:11\]:** There’s no way

**Kyle \[00:42:11\]:** Now, powered by AI to be helpful. But I think more so what I’m seeing is, a lot of the like fastest time to X tends to be because we’re now inviting so many more people into like software development on GitHub That like the zeitgeist is just swarming? And it’s

**Swyx \[00:42:32\]:** It’s not just developers anymore

**Kyle \[00:42:33\]:** And it’s not you and I. Like like however you want to say like what a developer is it’s not just folks who have been coding for a very long time. It’s folks that have maybe started coding or only joined in since the AI era. And now

**Swyx \[00:42:44\]:** what’s the latest Octoverse number? I know eighty million was my lastRem- member that a number of developers on GitHub

**Kyle \[00:42:50\]:** Oh, we’re over 200 million now.

**Swyx \[00:42:53\]:** Okay. Well, so you see?

**Kyle \[00:42:55\]:** Like over 200 million developers now.

**Swyx \[00:42:56\]:** But it’s not developers, right? It’s, it’s people with a GitHub account.

**Kyle \[00:43:00\]:** So, so this is, this is the biggest debate that I would say, everyone loves to have at GitHub at this point. From my perspective, right, I think that there’s, there’s clearly a difference between, professional enterprise developer and then developers. But I think that I think that the idea that we should be I don’t know, splitting hairs or segmenting developers in the early era of software development is, not worth our not worth the time. So

**Swyx \[00:43:29\]:** When you get into gatekeeping

**Kyle \[00:43:31\]:** 100%

**Swyx \[00:43:31\]:** What is a developer?

**Kyle \[00:43:31\]:** 100%. ‘Cause I wasn’t a developer when I started writing code? I was going to

**Swyx \[00:43:36\]:** Oh, no. I made— I cloned a thing, seven years before I learned to code. And then I and then I wrote about my learning to code journey, and people Just called me a fraud ‘cause I had a GitHub account. And I’m “Well, no, I just use GitHub, but I don’t know-” “I didn’t know what I was doing.”

**Kyle \[00:43:49\]:** I I remember that. I remember those sets of posts, and like that’s, that’s bullshit. So I fight very clearly on the line of, if you create code, if you have an idea and you create it into some way of, I’m, I’m going to run it and use the app right now, you may still use AI in that moment, but that’s okay. At some point you’re going to do the next thing. You’re going to create a big— You’re going to have to learn about this database. You’re going to fix a bug, whatever. We’re all on some same journey, and those people are also hearing about the great new agent skill package or a new CLI tool or a new whatever. And those projects are going up because you want to be a part of this moment, just like I wanted to be a part of the Ruby community when Ruby was popping off when I started becoming a developer, and now I can just click the star button. And so I think that yes, there’s clearly some amount of like spamming and game gamification that we’re working against, but I really think we’re just seeing this whole new cohort of folks that are moving from technology to technology because they’re not working on a 20-year-old software application. They’re working on a side app that they built on the weekend for their friends or for their new idea or whatever. And that’s how you see these enormous charts going up and to the right with With stars.

**Swyx \[00:44:59\]:** I think something that’s remarkable is the persistence or, that GitHub extends to those folks. Usually when I see platforms go into a new audience, they usually have to, have like a second platform with a different name that wraps the main platform. But somehow GitHub has been able to sort of persist and extend, and it’s friendly and whatever? So it’s, it’s nice.

**Kyle \[00:45:19\]:** I that’s partially why I think as we’ve tried to move into I don’t know, more like low-code-y things. We so we started working on Spark as like a way to, build an app and run it. I think that the reality is that we anytime we try to, kind of put even a veneer on top of it without when we put a veneer on top of something, we still always show you the code. That’s kind of like a tenant. We’re never going to, hide the code from you ever, because what

**Swyx \[00:45:52\]:** Why would you?

**Kyle \[00:45:52\]:** That’s, yeah, that’s the whole point? However, I think that what we learned with things like Spark is that really the value of Spark for most devs is, easy runtime. And you may have a runtime or a host that you’re going to use for that or you just build something and run it but, the package of making that even more simple isn’t really needed for folks that are trying to build software and not just trying to build, an app, which is, slightly different, a slightly different goal. So I want to get you in, I want to get you comfortable. I think the best thing for me as, someone that did not traditionally come into software dev way back, I want anyone to be able to breach that chasm and not be in the I don’t know, I feel like we’re, we’re still in an era of, STEM. I’ve got a 12-year-old and an eight-year-old, and it’s “We got to get ‘em into STEM,”? Over and over. And I like I do, I do the things that good parents do. I was “Oh, you want to do coding?” “Yes, I want to do coding.” Do coding classes. But now they’re just not afraid of doing software. And that’s, I think, the thing that’s honestly kept me at GitHub for so long. Anyone should be able to go and build a thing, just like I can go change a light switch in my house. I’m not going to go into the breaker box ‘cause I’ll probably kill myself? But, I can go change that light switch. Everyone should be able to go and say, “This fricking app doesn’t do what I want. I want it to work like this.” And that I think, is what’s kind of kept us all connected with GitHub through the years and some and during the easiest of times or in the hard times because of that opportunity of, we’re the home for all developers, and we want everyone to be able to have that feeling that we’ve had of, had an idea, I created it and holy shit here it is.

**Swyx \[00:47:37\]:** Here it is. All right, I’m going to try to do more spicy questions.

**Kyle \[00:47:42\]:** Great.

**Swyx \[00:47:42\]:** Is it an easy time now or a hard time?

**Kyle \[00:47:45\]:** Oh at GitHub? It’s a hard time. Like, it’s a hard time and also, I was just with my team and I said, “This is also, the best and most exciting time that I think I can remember at GitHub.” Because

**Swyx \[00:47:57\]:** Best of times, worst of times. It’s never one

**Kyle \[00:47:59\]:** ‘cause we’ve we were talking about Octoverse reports and, usually we do an Octoverse report once a year, and we look at the numbers, and we say, “Oh my goodness.” I was at Universe in October saying, “This was the fastest year of growth that we’ve ever had,” right? And now we’re doing more in a month than we did in a year last year.

**Swyx \[00:48:20\]:** You’re talking about PRs.

**Kyle \[00:48:21\]:** Commits.

**Swyx \[00:48:21\]:** Commits, yeah.

**Kyle \[00:48:22\]:** PRs. Kind of like you name it by roughly every measure that we’re looking at, there’s some amount of sort of growth that is much bigger, and that is breaking our system in new ways, not old ways. Like webhooks were always notoriously, unreliable over the years?

**Swyx \[00:48:38\]:** Whose fault is that?

**Kyle \[00:48:39\]:** not anymore mine, but for a period of time, I’m sure you could pull up a tweet that was “It was me. I’m sorry.” but, now, that got rewritten at a scale level that is still working and is not having problems today. Now what we’re finding isn’t just the isn’t the-The simple stuff that folks are on the sometimes on Twitter or on the internet are “Hey, why is this like this?” Sure. There’s absolutely silly problems that we shouldn’t exist. But now we’re talking about, unique, novel permission problems that happen only at a scale across all different objects or whatever, that now we have to go rewrite this underlying system. And so it’s, there are problems that yeah, caught us off guard, which I think I said. Like the growth is astronomical, but also we’re making such material progress in that I’m excited once we’re once we’ve kind of like reimagined the underlying foundation layer, or pieces of it at least, what’s going to be possible when it’s not just all of us and all the new people that are being developers and all of their agents and all the tools like working together. Because that’ll still happen in that in that GitHub tool, that GitHub community. But it’s a it’s a hard day anytime we can’t give you what you’re looking for. We have the same problem internally. We operate through github. Com. Of course, we have backups when things go down and whatnot for our own operations but we feel it too. If it’s not working it’s not working for us, and that’s kind of like the promise of dogfooding for GitHub. It’s always been true. We’re using the same tool you’re using. We’re not using a super secret version. We and so we also need it to be great for us for our customers of course for open source. And now an exponential growth of agents, Doing it too.

**Swyx \[00:50:32\]:** I wanted to load for audio listeners who maybe haven’t seen your tweets, whatever. So one billion commits in twenty-five. Now it’s two hundred and seventy-five million per week on pace for fourteen billion this year, if growth remains linear. Is that still the pace? I don’t know. It’s been a

**Kyle \[00:50:48\]:** it’s, it’s speeding

**Swyx \[00:50:50\]:** Roughly.

**Kyle \[00:50:50\]:** It’s still speeding up.

**Swyx \[00:50:51\]:** It’s, it’s April, so yeah.

**Kyle \[00:50:51\]:** Exactly. This was in April.

**Swyx \[00:50:53\]:** All right. So basically you have fourteen x growth, right? Year on year on year. And I think that’s a scaling issue. I think, I’m going to like try to really steel man this thing. People have experienced fourteen x growth. They haven’t had your downtime. And that’s like— C-can we go dig into that? Why? Like what’s the— what broke? What are we doing to fix it? Like just anything for the community to reassure them.

**Kyle \[00:51:18\]:** so there’s a Like I was saying, there’s a couple different places that we’ve seen the growth issues. Some of the growth issues, which is why we’re t— I was talking about pushing hard on more CPUs is in actions in particular. More tools, more agents, more PRs mean more builds, more builds mean more CPUs. And so we are expanding through not just our data center, but obviously we were talking about moving to Azure and moving to, adding an additional cloud compute because we simply need more CPUs. Not as much GPUs. We definitely need GPUs too, but now CPUs are becoming a factor.

**Swyx \[00:51:53\]:** It’s very CPU heavy.

**Kyle \[00:51:54\]:** Underneath the hood when it comes to some of the underlying services, we’ve been breaking up over the years our database infrastructure, so that way we have, more cognitive separation between our the various services. The place that we continue to have pain is in, permissioning. And so right now m-many of our permissioning layers sit into a database that we like internally call MySQL One, and old Hubbers will know what I’m talking about. And so we’ve been pulling things out of MySQL One for many years, because like and we use we use Vitess and we use other technologies to shard and we do it as one big

**Swyx \[00:52:31\]:** Famous thing, PlanetScale was born from this and

**Kyle \[00:52:32\]:** A hundred percent. Sam Old Hubber and friend. And so finding these opportunities to like break this out and then do that globally. The other thing that I think is interesting and both a unique opportunity and tricky is we also run everything I just talked about in a black box container with GitHub Enterprise Server for people that work on-prem. So we take everything I just said, and we also do it on-prem, and we also do all of that and we do it in a data residence setup for customers that need to have their data in a single location. Each of these has the unique characteristic around how we’re sort of storing that data in MySQL or in a permissioning setup. That’s where some of these outages have oc-occurred, where you’re seeing it more like across the board rather than just like the one piece

**Swyx \[00:53:17\]:** Filling the database

**Kyle \[00:53:17\]:** Isn’t quite working. Exactly. And so part of it is that. I think there’s been some other places where agents are much more or more projects appear to be moving towards monorepo versus we were going the other direction for many years in the industry. Repos were smaller, but there were more of them, and now we’re seeing the opposite. Repos are bigger, and there’s, not fewer of them per se ‘cause there’s new growth, but, we’re just seeing many more big repos. Big repos, big monorepos have always had, a unique performance problem. Because each one, is slightly different if, particularly if the underlying blobs are incredibly big Inside the repos. And so we’ve done a ton of work that you pro— like most people haven’t probably experienced, unless you’re in this case of the monorepo. But that Git, infrastructure layer improvement does help the overall, system because, many of the improvements that make monorepos work better make all repo infrastructure work better. And so, I could kind of keep going down the line where it’s another thing where we’re moving out of, We’re changing how we do j I’ll just say job queuing for lack of a better, explanation changing the underlying technologies there.

**Swyx \[00:54:32\]:** I spent two years being a job queuing guy, so.

**Kyle \[00:54:34\]:** And so it’s kind of a little bit of a little bit of piece by piece, and it’s mostly because as we were— as it was built, we built everything in a way that assumed, I guess in some ways that the size of the pipe of work was going to remain the same. There’s just going to be more people coming through each of those pipes. But instead now in places whereA git push was, generally a certain size for example, is now, no longer true.

**Swyx \[00:55:03\]:** Oh, yeah.

**Kyle \[00:55:03\]:** Or

**Swyx \[00:55:05\]:** I push a thousand

**Kyle \[00:55:06\]:** On the average. 100%

**Swyx \[00:55:06\]:** A thousand line commits like daily

**Kyle \[00:55:07\]:** Same thing with PRs. Like PRs same thing. And like we’ve talked about optimizing that and making changes where, and there were technology choices that did not work there? And it got slow, and it didn’t It was not fast. It did not do what the users wanted. And so we’ve been reeling that all out and going “Okay, that’s just not right. Let’s stop putting good money after bad and do it the do it the right way or the right way now.” So there’s It’s a it’s a lot of things, not quite when I’ve experienced scale at GitHub historically, it’s almost always two options that we’ve used. We go vertical scaling, particularly with databases, right? And we go horizontal scaling. Oh, we just have more people using this service. Great. We’re going to add more servers, and we rack them in our data center, or we use it in a cloud. And now we’re sort of in a like diagonal, where like vertical doesn’t really work anymore. Horizontal isn’t work either because we’re all We all have some CPU or GPU constraints in the world now, and now we have to go in and like crack open services that have been running for 10 or 15 years and go, “Okay, the rules of this service have legitimately changed, and now we have to rewrite them.” None of this is an excuse. This is like we’re We have to do the work. We have to make it better.

**Swyx \[00:56:22\]:** actually as an infra guy, I’m “This is like one of the most fascinating scaling challenges I’ve ever seen.”

**Kyle \[00:56:26\]:** That’s that’s, that’s the thing that’s the thing that it’s hard for Like when we weren’t talking about it publicly, and I was like I came out, and I was “Hey, I just want to explain what’s going on.” Part of it comes from a very old GitHub ethos, which is it’s our it’s our uptime. It’s down. W What I know you’re a developer, so you’re, you’re inclined to want to understand more what’s going on. But at the same time us going “Hey, this service didn’t, perform the way we expected, and now we have to go change it,” we weren’t We’re not trying to hide anything from you in that. It’s that well, that’s our problem because you expect us to be up, and I think that’s really baked into the core, origins of GitHub. And so now what we’re trying to do as a team is do all that work and just tell Talk about it more and just share you more technical details, write these blogs, write the posts, get the engineers who built it after they finish the work, just tell you “Okay, this is what we did.” I think that’s the contract that we want to bring back to the community and say, “Hey, we’re still very serious about what we’re doing. We haven’t been telling you about each piece. So let’s do that and we’re going to keep building this and scaling it in a way to support the If it’s not 14, then it’s 30 or it’s 50 or whatever the next exponential growth is going to be.”

**Swyx \[00:57:40\]:** First of all, fantastic answer. I think

**Kyle \[00:57:44\]:** And I apologize in advance if like any of that

**Swyx \[00:57:47\]:** I think it’s all nice

**Kyle \[00:57:47\]:** Is slightly incorrect just simply because

**Swyx \[00:57:49\]:** No

**Kyle \[00:57:49\]:** I’m not the I’m still in the weeds with this but it’s not my day-to-day. But like that’s the thing is we’re all looking at it to that level.

**Swyx \[00:57:58\]:** And obviously, if people want to help, they can join.

**Kyle \[00:58:00\]:** Absolutely

**Swyx \[00:58:01\]:** So like I think the that is, good. I think people also would just want to know when are, when are you through the thick of it right? Like is there Have we identified all the issues? Is this just never-ending? Is Git broken? Do we have to change the Git, protocol? Like what how much is breaking, right? It’s been a while. And so I think people do want to know What’s the path back to the reliability that everyone expects out of GitHub.

**Kyle \[00:58:30\]:** So like our availability in like recent few weeks has been much better than the three weeks before that or the three weeks before that and so forth. And so a lot of these improvements are still very much paying off for us. I think that we’re still working on that that database piece that I mentioned, and that just is a little bit physics a little bit of time to get it to get it fixed up. Because we have to the w

**Swyx \[00:58:59\]:** My the answer I had in my head Was call YouTube.

**Kyle \[00:59:03\]:** So YouTube ultimately is

**Swyx \[00:59:04\]:** ‘Cause they also use Vitess.

**Kyle \[00:59:05\]:** They also use Vitess. But the,

**Swyx \[00:59:09\]:** Like whoever was the guy, the scaling guy at YouTube?

**Kyle \[00:59:11\]:** Like that’s That I believe went to PlanetScale, and was a part of PlanetScale too. But like

**Swyx \[00:59:16\]:** Oh, you mean Sugo?

**Kyle \[00:59:17\]:** I think so. Yeah. And so, and so like

**Swyx \[00:59:19\]:** He’s at Superbase now.

**Kyle \[00:59:20\]:** Ah.

**Swyx \[00:59:21\]:** There’s a whole Postgres drama Thing there, right?

**Kyle \[00:59:25\]:** So like some of it’s that. I think the other piece of it is, our move to get additional compute will alleviate a fair amount of this particularly on the action side ‘cause a lot of the underlying, outages is actually related to,

**Swyx \[00:59:39\]:** I’ll tell you actions is the it’s the root of all evil.

**Kyle \[00:59:42\]:** it’s all It has its pros

**Swyx \[00:59:47\]:** Some extent

**Kyle \[00:59:47\]:** In that it’s the core It’s the core compute layer for either CI, side projects, et cetera.

**Swyx \[00:59:52\]:** Is the main money maker? Like is

**Kyle \[00:59:54\]:** Actions?

**Swyx \[00:59:55\]:** No? I don’t know.

**Kyle \[00:59:56\]:** like Actions

**Swyx \[00:59:57\]:** I pay a lot for compute, right?

**Kyle \[00:59:58\]:** like Actions is definitely a piece of the overall business, but I would say that like we ultimately also

**Swyx \[01:00:06\]:** Storage

**Kyle \[01:00:07\]:** Give away so many like minutes as part of our entitlements as that. But that’s what I was saying. Everyone’s using it. We talk about it as CI/CD, but the reality is people use it for CI/CD and

**Swyx \[01:00:17\]:** Automation

**Kyle \[01:00:17\]:** Various processing and automation, exactly. And so like part of it is also that like compute piece that is also alleviating some of our availability.

**Swyx \[01:00:26\]:** This is my abuse of, actions. I have been

**Kyle \[01:00:29\]:** Oh, yeah

**Swyx \[01:00:29\]:** I have been scraping for every day, and just like I just tell people to

**Kyle \[01:00:34\]:** Thank you for your service

**Swyx \[01:00:35\]:** Go dog because I But this is also how I track, actions all time. So anyway,

**Kyle \[01:00:41\]:** So like some of it’s going to be that. I would say that like each month I expect in the next three months, you’re going to see fewer and fewer moments where we have an availability problem Where things are going to go down, and that’s not just it’s stopped. It’s that we’re still experiencing faster growth than ever before. It’s just that those underlying improvements that we’ve been hard at work on, are finally paying off. It’s just that the improvements take-It’s less about, these incremental improvements where you make a small change, and you get this big output. It’s now material change That takes a bit of time, and then you see a step change in our availability.

**Swyx \[01:01:14\]:** There’s a thing we used to do at Amazon, I don’t know if this is, a thing, but, if automated software verification or simulation of load testing and all that. I’m, I’m just like at this point, you have a whole map of GitHub. And, while you can assume whatever growth rates on whatever dimensions that you care about and just run it through a system, right? I feel like there’s a way to, I don’t know, have a systems model of GitHub and, see what breaks. But obviously, I’m pro— I’m not that close to the problem, so.

**Kyle \[01:01:39\]:** But yeah, so yes, totally. And I would say, that’s been the journey and work that’s been happening since, I would say November to now. Because October, right, was the time where we even said, “Oh, look at the growth,” and, and then you start to see the chart

**Swyx \[01:01:53\]:** It doesn’t

**Kyle \[01:01:53\]:** Really pick up. And it’s oh, we tested it at N amount of scale, and now it’s at, N cubed maybe like in some in some vectors. And so now we have to go and build it that way and make sure that it can handle all of that scale.

**Swyx \[01:02:08\]:** Let’s talk Copilot. So how many original creators of Copilot are there?

**Kyle \[01:02:15\]:** Oh, geez.

**Swyx \[01:02:18\]:** ‘Cause I count like twelve authenticated.

**Kyle \[01:02:19\]:** We haven’t— Yeah, I forget, all joking aside, I forget the number of people that were on, the original, GitHub Copilot team. But, there was a bigger group.

**Swyx \[01:02:30\]:** I heard it’s, it’s Alex. It there’s, there’s, a three people

**Kyle \[01:02:32\]:** Alex worked on it. Udo worked on it. There’s a a bunch of people that were on the team.

**Swyx \[01:02:35\]:** And then their entire management line. Okay. So enormously successful at its in its in its day. I think the last number, I think Mario Came to my conference, and talked about the hundred million dollar mark. I think most recently three hundred. I might be out of date as well there.

**Kyle \[01:02:53\]:** I don’t think we shared the dollar amounts.

**Swyx \[01:02:54\]:** All right, cool. Just, what’s the state of Copilot? It’s, it’s obviously as a concept brought into More of Microsoft. But just at GitHub.

**Kyle \[01:03:03\]:** so I think One of, one of the challenges is, that we had with Copilot, right, is that we came out the gate with code completion, and it was super great, powerful, et cetera. And then what we initially worked on after that sort of, initial year and a half, was, going after fine-tuning because our customers, the industry on the whole was really talking about, okay, well, how do we get more more correctness or performance out of this? And so we were working on a whole bunch of efforts to do fine-tuning on, larger and larger code completions or, next edit suggestions with fine-tuning, et cetera.

**Swyx \[01:03:43\]:** And let me clarify. Is this fine-tuning one model or per customer a fine-tuned model for

**Kyle \[01:03:48\]:** Per cust— Well, both. But, but, fine-tuning one model for the overall, use, and then fine-tuning per customer that wants this as, a service effectively. And around that time is when the next generation of models came, and that’s around the same time that all these other AI, coding tools came to be because the models really sped up. And so everyone kind of, will ask, “Well, what happened to GitHub Copilot?” there’s all this time, and I would say that we were on an era of going okay, we want to improve everyone’s results, and so let’s focus in on fine-tuning because that’ll give us these better results. And then the models got better. And so then ever since, we’ve been really on this kind of journey to go, okay of course, we have, this great code completion, and we’ve done a ton of investment in the better underlying models that we have post-trained better, next set of suggestions with post-training language specific models. All this stuff that kind of, sits in the ether of GitHub Copilot is code completion, but also have now ha— now have, a single underlying, SDK and harness for our coding agent Copilot ultimately. The new CLI, the new desktop app, cloud agents that use the same SDK. And so there was this moment of both, really trying to figure out what our customers want, models, Sherlocking us a little bit, then going and saying, “Okay, what does everyone ultimately need?” And what we think is that it’s not solely about the code generation. It’s really about having the ability to use these coding agent brained, harnesses or run times across, not just the coding experience where I’m going to, send a bunch of tasks out, or I’m going to use Fleet to break up a single task or autopilot similar to Goal all this stuff. But also how do I do that for all of my security remediation? How do I do that for every GitHub issue that comes in, just stick a coding agent on it just to see if it’s possible? How do go through my repository and see all of my documentation and extract out okay, this doesn’t actually match? That amount of sort of AI coding agent automation, I think is a big part of what we see when we’re looking at, okay, we’re still kind of going through a similar but very different flow. It’s just all happening at the same time. There’s not really the same, I’m going to create an issue to track my idea of building this. You’re probably just going to go, do it.

**Swyx \[01:06:22\]:** Just do it.

**Kyle \[01:06:22\]:** You’re going to say, “Hey, just build this,” right? And, there are still tons of, open issues and projects, et cetera, that are using issues like Peter and OpenClaw to be able to sic all of his agent on that. That kind of infrastructure layer and a really great coding experience that allows you to handle the sort of multiplexing, aspect is what we’ve built, are still building with GitHub Copilot. And so for folks that haven’t really used GitHub Copilot sinceThe thing that got them excited about this Which I I get. I really encourage you to, look at especially the GitHub, Copilot app. That’s my new daily driver. I obviously, if you prefer the CLI, also the CLI, be able to use all the models, the bring your own key side of it. We’re still improving our own models and using those too. And, it’s just like a very different experience, but I think that broader sense is of like software development and how coding agents can help throughout, not just Writing the code, or even verifying it or deploying it is is where we have this unique, angle. The other side is the context piece. Like

**Swyx \[01:07:44\]:** Oh, God

**Kyle \[01:07:44\]:** we’re still It’s like one of those things where I think the the final thing that will let me ultimately, feel complete at GitHub is, when we have this ability for GitHub to act like Kyle wants it to act Or Shawn or whatever. And we all codify that in rules and in memory and everything else, but

**Swyx \[01:08:03\]:** Well, that’s an open research problem, right? Like it’s

**Kyle \[01:08:05\]:** A hundred percent. A hundred percent

**Swyx \[01:08:07\]:** AGI when you get it. Yeah.

**Kyle \[01:08:07\]:** A hundred percent. But, if we can even just do it where my team, Without me having to codify everything, and as our methods shift on purpose to be able to have that full experience and all the understanding of what’s happening in my dependencies or open source, that feels like a big place for us to be able to continue to provide something really unique and valuable with GitHub Copilot.

**Swyx \[01:08:29\]:** Is there a form factor that we haven’t explored? I think like we did code completion Then we did kind of let’s broadly call it agentic IDE Which Cursor Famously popularized, and then now it’s, now it’s all about the sort of agent orchestration Background agent, whatever. And then there’s the security review. I feel like everyone’s like just throwing agents at everything. The entire SDLC has Just, covered with agents. Are we like at the end of history here, basically? Like is it just refinements from here on out?

**Kyle \[01:09:04\]:** I think that we’re all still in such this hypermyopic era of AI Where the reality is that for various, boring security and governance reasons at least for most people’s work, why is my coding agent, even if it’s all background agents, background running not, losing all the context that’s available to it across everything that I’m doing outside of coding? I think the most interesting thing to me in AI is actual ambient AI, not insert assistant name thing or, I’ve tried just about every pin in tool and whatever, and they don’t work the way that I’m looking for them to work because they are just trying to capture, and then they are trying to codify and then recall. And I think the thing that I’m looking for, back to the very beginning, I’m looking to be building out the next version of webhooks or, implementing a new feature, and it for it to know every spec doc, every email, the conversations that I’ve had online, everything about how this could be implemented and be able to, use that as part of its decision-making and none of these tools are ultimately doing this. So I think that it’s as if, software development work was a single lane task, was like it only needs a developer. Once I once I write the perfect code, we’ll be done here, but that’s just never been true. It’s all the context of the other team members, what the business is doing what’s popular right now, and I think that’s this huge opportunity for us to go much broader than really excellent coding agents? And that is honestly why I think OpenClaw has been so interesting is that sure, it’s connecting to all the data, sources that Kyle the human cares about, and now my question’s “Okay, how can I take all that and use that every day as a software dev connected together, not just have a new way to kick off a coding agent?” And that’s where we’re at. We’re saying, “Okay, I’m going to go use this CLI under the hood or this SDK,” but that’s not what I’m talking about. I’m talking about I’m having a conversation with you it downloads the podcast, and it realizes, “Oh, Kyle, sounds like Kyle needs this app or this thing or this “ That level of

**Swyx \[01:11:16\]:** Just recommends it.

**Kyle \[01:11:16\]:** That level of, that level of connectivity I think is where we still have a ton of ways to go in software because then when we have that red thread we want to pull, that idea, it can not only use the perfect way to write that code, but instead all of the sort of taste and judgment calls and expertise that I’ve earned or that we’ve earned as a group and use it as part of the actual implementation.

**Swyx \[01:11:42\]:** The extreme of it is AI runs your life, right? And I think there’s a scary inversion of control in the way that I literally doing it in the way that developers mean it in terms of frameworks Like the Hollywood principle, “Don’t call me, I’ll call you.” Like there at some point there is an inversion of control where, you should you stop telling what the AI, the AI what to do. AI tells you what to do. And, that’s a little bit scary, but also, maybe better.

**Kyle \[01:12:10\]:** like Nat, I think Nat Friedman shared this in a like a Stripe event like talking about his OpenClaw was, he connected OpenClaw to his cameras, and it was, watching him.

**Swyx \[01:12:20\]:** It redirected his Uber. And it,

**Kyle \[01:12:23\]:** there’s a degree of this where I was I actually would love OpenClaw to tell me to Drink water. I don’t know that I want it to be, Changing where my car goes, but I do think that’s kind of what I’m talking about, which is it needs to have so much more information at its disposal for it to be helpful to me, and I still don’t think we’re, anywhere near talking about AGI. I’m just talking about every time I have to tell you something I care about that I’ve ever kind of said or I’ve said a dozen times, it should be able to know that codify that or gain access to it. Like the dreaming ideas, are an attempt to kind of do some version of this but I think there’s a much more proactive angle that will help software devs if we can test that out a bit more.

**Swyx \[01:13:05\]:** Yeah. Well, the other thing about OpenClaw that reminded me Is Microsoft has a CVP Dedicated to OpenClaw. Why?

**Kyle \[01:13:16\]:** Because you don’t think they should?

**Swyx \[01:13:17\]:** I don’t, I don’t know. I think CVP is a high title. What, why is this so important? Like Microsoft Doesn’t even own OpenClaw. What’s, what’s the

**Kyle \[01:13:29\]:** so I— we’re talking a lot more about this at, Microsoft Build this year too. I think, the main thing is that what OpenClaw has done is it has made this connection for people to have access to the resources that you have access to and be able to do things for you in a way that previously people were trying to codify into their own agents. And so when you think about it like in the work context, wouldn’t it be great to have a Claw-like object that I could actually run on my work device that or had access to my work assets, made— worked well on Windows what that would look like. And so I think that OpenClaw has become the personification of, a valuable agent that understands me because it has access to all of my information, and it can use a computer. And so thus it can do a lot more than, just a task-oriented process or like a a chat tool, et cetera. And that’s like a bunch of the goal of Build, right? We’re at Build this year trying to take a very different approach of it’s unapologetically aimed at developers. We’re trying to show the bigger investment to not just say, “Hey,” like you said, “Why do you have a CVP of OpenClaw?” Well, because, one of the problems that we have, right, is that our agents, if you install them not on a Mac Mini or not on a hosted device, you install them on a personal device or a work device, we need better sandboxing at the OS level. I need to be able to use that Claw and not, get fired. And so Microsoft is “Okay, great, let’s, do that too.” And then it’s, okay, well, where should I be able to talk to this agent? Should each of us just have a Claw available to us at work? Probably. And so there you go. And continuing to contribute a ton to the open source project too. Microsoft, I think as I’ve gotten more and more, information there’s so much investment into the open source, projects themselves that for whatever reason just I think there’s like this they don’t want to come off those teams don’t want to come off as like taking any credit or getting any recognition. But so many of these core contributors or teams are full-time just pushing into open source projects. And, I think that’s, that kind of shows the difference between, well, why are we looking so hard at something like Claw? Why are we looking at sandboxing on Windows? Why are we looking at cloud versions of sandboxing? Why are we looking— Because ultimately, we need more platform components. We don’t need everyone to be building the same exact, top-line product. And so if we’re building for builders, that requires us to give you all these components and tell you what they are and how they work and why you should be interested versus only delivering that single vertical over and over and over again.

**Swyx \[01:16:23\]:** I think, my maybe one way of framing it Is that Microsoft is the original operating systems company. And here is the new operating system for AI.

**Kyle \[01:16:35\]:** like I think that we are also in an era where we are— we need to help build that bridge? All joking aside operating systems need to look different than they looked five years ago because it’s not just you using them anymore. And that’s changed the whole idea. It’s not, “Okay, my Claw is going to create a user account.” Doesn’t work like that? And so just just like all of us, we all have to look much more deeply in the stack, all the way down to, the silicon layer in Azure to be “Okay, well, What do we need now?” ‘Cause the workloads are different. It’s not just, “Okay, we need more inference.” It’s, “Okay, well, what type of inference do we need? What type of compute do we need to run these agents or run these agentic flows?” it’s a really interesting kind of like multi-layer problem, versus kind of, I would say software in the last five or six years were all going to our events, and we’re kind of saying a version of the same thing. SaaS product has new SaaS thing. It’s the best SaaS thing ever.

**Swyx \[01:17:42\]:** It was boring for a while.

**Kyle \[01:17:43\]:** And so now it’s like Oh my goodness, we’re at physics.

**Swyx \[01:17:47\]:** It’s great.

**Kyle \[01:17:48\]:** We’re at physics problems. And that’s exciting.

**Swyx \[01:17:50\]:** We’re— we’re now trying to make, semicondu- room temperature superconductors. Still. That’s, that’s, that’s never going away. No, I think, that’s a really good overview of, everything. I think, have I have we left anything unsaid that you wanted to really get out there that we should cover?

**Kyle \[01:18:07\]:** I’m really excited by for folks checking out, checking out the announcements that we have at Build go you can go look at them online, take a look. I think that I’m hoping that it’s driving, a degree of curiosity and interest because there’s such this big shift that we’re making at Microsoft for developers, where if you’re a daily driver of a Mac device or a Linux device, and you’re “Okay, I don’t use Windows,” there’s improvements that are being made that I think are going to surprise folks to just be “Oh, that’s in— they really want to do that?” not, And I’m talking for developers. I’m not talking for I play video games on the weekends on my Windows computer. I’m talking my daily driver. Like-All the way from that to, okay, well, what is it like to build an agent or build an app and deploy it and run it at work in particular? I think that is a big piece of it where I talk all the time with the team how I build on the weekend should be how I build at work. But if you’re working at a Fortune one hundred or a Fortune five hundred, you’re probably not vibe coding an app and then shipping it to some service. You got to go through security and compliance. How can we move just as fast at work? And that’s, I think, something that we have a bunch of different offerings for to give you that same sort of agility and power, but in the work context. And then I will tell you I’ve mentioned it a couple times, and, it’s very freaking cool. If you are in the M365 land in any way, check out WorkIQ, check out FoundryIQ. These little, oversimplifying it context engines are wild good. And, we’ve given them to our developers at GitHub, we’ve given them to employees at GitHub as we’ve used these tools to be able to just ask questions around everything that you have in your work context. And with FoundryIQ, be able to just do the same exact thing across all your existing stores. What— Not move to new tools, just connect them in. It’s surprisingly powerful, and you your boss is still not going to get fired, and IT is not going to turn it off because it’s leaking all this private information. That is the trick that I think, is sometimes getting lost when we’re talking about all these all these great new platforms. ‘Cause I can use them, I’m “Oh, this is super powerful. Oh, and I can’t I can’t use it.” and it’s Not because I’m at work at GitHub. It’s be

**Swyx \[01:20:34\]:** ‘Cause I’m not allowed, yeah

**Kyle \[01:20:35\]:** It’s ‘cause I’m not allowed, because they can’t do all the things that large, complicated companies need. And so, whether it be I said, just the kind of interesting daily driver curiosity all the way through to, “Oh, my gosh,” “I can go use this at work tomorrow potentially,” and have that context layer, have that intelligence, it’s a huge, it’s a huge shift. And so check it out. I’d love to hear— I’m, I’m not shy on social. I’d love to hear feedback. What’s working what’s not. But hopefully surprise folks a little bit.

**Swyx \[01:21:07\]:** What I’m hearing— so first of all, I think that’s, that’s a great pitch. What I’m hearing, actually, is that you should put the WorkIQ people next to the Copilot people. ‘Cause, the exact prob- context problem that you named They solve enough for you to do your job, which is nuts.

**Kyle \[01:21:23\]:** So, the thing that we are lit— that’s literally what has been Happening the last several months.

**Swyx \[01:21:29\]:** I already forecast you were going there.

**Kyle \[01:21:30\]:** It’s totally ‘cause, you’re totally right. The code, the code and the code asset problem is a little bit unique. But otherwise

**Swyx \[01:21:36\]:** That’s it

**Kyle \[01:21:37\]:** We’re all working

**Swyx \[01:21:37\]:** It’s context

**Kyle \[01:21:37\]:** With each other now. It’s all just context, exactly.

**Swyx \[01:21:40\]:** Amazing. Great. I’m going to be there. I’m going to be doing

**Kyle \[01:21:43\]:** Great

**Swyx \[01:21:43\]:** A couple sessions there. I’m going to be interviewing Satya.

**Kyle \[01:21:46\]:** I know.

**Swyx \[01:21:47\]:** When I first started the pod, though, I had, Jeff Dean on. Jeff like It’s like hall of fame of People I want to meet someday. Satya’s on there. So, what should I ask Satya?

**Kyle \[01:21:57\]:** I think, I think that the best question to ask is what he thinks is true in, two or three years from now. It seems like such a throwaway question. But ultimately, the way that the way that he is looking at this AI problem in, inference problem, token problem, and what we’re how we’re actually going to be working I think you can see some of the recent shifts that have been happening inside of Microsoft to kind of drive us to a place where it’s not four, five, six, seven, eight different things. It’s not a lack of context everywhere. But, why is this sort of approach in two years going to, pay off? Because that I think

**Swyx \[01:22:41\]:** Wow, that’s a bold Okay. I’ll ask it. I’ll say you I’ll say I prompted by you but

**Kyle \[01:22:45\]:** Absolutely

**Swyx \[01:22:45\]:** It’s a bold question because there, I think there’s a lot of, doubts to be honest, Externally. And so, yes, I want, a straight answer from him on that I think would reassure a lot of people, and honestly, give me a lot of food for writing. So, thank you so much for spending your time. Thank you for doing what you do. I think as a CEO, you don’t need to be the external face. But, because you are authoritative, ‘cause you have so much background with GitHub, and it’s so authentic, we on the outside feel it. So thank you for that.

**Kyle \[01:23:16\]:** Of course. Appreciate it. Thank you so much, Sean.
