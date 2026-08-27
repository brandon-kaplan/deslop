# Worked examples

Each pair shows one dominant pattern. Rule numbers point at `SKILL.md`.

## Rule 1, manufactured significance

> The engineering team adopted trunk-based development in Q2, marking a pivotal moment in the organization's journey toward continuous delivery and reflecting a broader industry shift away from long-lived branches.

> The engineering team adopted trunk-based development in Q2.

The original states one fact and three unsupported claims about what the fact means.

## Rule 2, advertising register

> Our seamless, purpose-built ingestion pipeline boasts best-in-class throughput and a robust commitment to data quality.

> The ingestion pipeline handles 40k events per second and validates every record against its schema before write.

Replacing brochure words forces the specifics into view. If no specifics exist, the sentence had no content.

## Rule 6, unnamed sources

> Experts agree that observability tooling is now essential for distributed systems, and studies show teams that adopt it resolve incidents faster.

> Google's 2024 DORA report found that teams with mature observability practices restored service faster after incidents.

If no real source exists, delete the claim. Do not swap one vague attribution for another.

## Rule 8, trailing -ing analysis

> The service now retries failed writes three times with exponential backoff, ensuring reliability and reflecting our commitment to data integrity.

> The service retries failed writes three times with exponential backoff.

The clause added no information. If retry behavior does improve a measured reliability number, state the number in its own sentence.

## Rule 9, speculative gap-fill

> The library's original author is not listed in the repository, suggesting the project was likely an internal tool before it was open-sourced.

> The repository does not name the original author.

The second sentence invented a history. State the gap, or say nothing.

## Rule 10, binary contrast

> This isn't just a refactor, it's a rethinking of how the scheduler reasons about priority.

> The refactor changes how the scheduler ranks priority.

## Rule 11, forced triads

> The release improves performance, enhances security, and delivers a better user experience.

> The release cuts p99 latency from 800ms to 210ms and adds TLS on the internal service mesh.

Two real facts beat three vague ones. The third item existed to complete the rhythm.

## Rule 12, false ranges

> The platform handles everything from user onboarding to enterprise procurement to real-time fraud scoring.

> The platform handles user onboarding, enterprise procurement, and fraud scoring.

Onboarding and fraud scoring are not endpoints of a scale, so the range was decorative.

## Rule 13, fragment runs

> Then the cache expired. No warning. No fallback. No way to recover. The whole tier went down.

> The cache expired with no warning and no fallback, and the whole tier went down.

One fragment lands. Four in sequence read as theater.

## Rule 15, synonym cycling

> The scheduler assigns each job a priority. The component then sorts the queue. This subsystem finally dispatches work to the pool.

> The scheduler assigns each job a priority, sorts the queue, and dispatches work to the pool.

Three names for one thing forced the reader to re-resolve the subject twice.

## Rule 18, passive voice

> Configuration is loaded at startup and defaults are applied automatically when values are omitted.

> The server loads configuration at startup and applies defaults for any value you omit.

## Rule 19, false agency

> The postmortem decided that the alerting threshold was too aggressive.

> The team decided in the postmortem that the alerting threshold was too aggressive.

A document cannot decide. Name the people.

## Rule 25, stacked hedging

> It could potentially be argued that the change might have some effect on tail latency in certain cases.

> The change may reduce tail latency.

Four hedges collapse into one, and the sentence gains a direction it did not have.

## Rule 28, preemptive defense

> To be clear, I'm not arguing that tests don't matter, and you could frame this differently, but a tempting approach would be to gate every merge on the full suite, which would slow everyone down. The point is that the suite takes 40 minutes.

> The test suite takes 40 minutes, which is too slow to gate every merge.

Three defenses against objections nobody raised, wrapped around one fact.

## Rule 31, inline-header lists

> - **Performance:** Performance has been improved through query optimization.
> - **Reliability:** Reliability has been increased with automatic retries.
> - **Security:** Security has been strengthened using scoped tokens.

> Query optimization cut average response time in half. Failed requests now retry automatically, and service tokens are scoped per environment.

Each label restated its own sentence, so the labels carried nothing.

## Rule 33, feelings instead of mechanisms

> The new API feels much more intuitive and gives developers confidence.

> The new API uses one method per operation and returns typed errors instead of status codes.

## Rule 35, documenting the previous version

> This function replaces the old approach, which looped over every record and caused O(n squared) behavior on large inputs.

> This function looks each record up in a hash map, so it runs in O(n).

Current behavior belongs in the doc. The old approach belongs in the change log.
