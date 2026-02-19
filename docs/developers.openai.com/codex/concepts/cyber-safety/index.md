# Cyber Safety

Source: https://developers.openai.com/codex/concepts/cyber-safety

Cybersecurity safeguards and trusted access for Codex users

[GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/) is the first model we are treating as High cybersecurity capability under our [Preparedness Framework](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf), which requires additional safeguards. These safeguards include training the model to refuse clearly malicious requests like stealing credentials.

In addition to safety training, automated classifier-based monitors detect signals of suspicious cyber activity and route high-risk traffic to a less cyber-capable model (GPT-5.2). We expect a very small portion of traffic to be affected by these mitigations, and are working to refine our policies, classifiers, and in-product notifications.

## Why we’re doing this

Over recent months, we’ve seen meaningful gains in model performance on cybersecurity tasks, benefiting both developers and security professionals. As our models improve at cybersecurity-related tasks like vulnerability discovery, we’re taking a precautionary approach: expanding protections and enforcement to support legitimate research while slowing misuse.

Cyber capabilities are inherently dual-use. The same knowledge and techniques that underpin important defensive work — penetration testing, vulnerability research, high-scale scanning, malware analysis, and threat intelligence — can also enable real-world harm.

These capabilities and techniques need to be available and easier to use in contexts where they can be used to improve security. Our [Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/) pilot enables individuals and organizations to continue using models for potentially high-risk cybersecurity activity without disruption.

## How it works

Developers and security professionals doing cybersecurity-related work or similar activity that could be [mistaken](#false-positives) by automated detection systems may have requests rerouted to GPT-5.2 as a fallback. We expect a very small portion of traffic to affected by mitigations, and are actively working to calibrate our policies and classifiers.

The latest alpha version of the Codex CLI includes in-product messaging for
when requests are rerouted. This messaging will be supported in all clients in
the next few days.

Accounts impacted by mitigations can regain access to GPT-5.3-Codex by joining the [Trusted Access](#trusted-access-for-cyber) program below.

We recognize that joining Trusted Access may not be a good fit for everyone, so we plan to move from account-level safety checks to request-level checks in most cases as we scale these mitigations and [strengthen](https://openai.com/index/strengthening-cyber-resilience/) cyber resilience.

## Trusted Access for Cyber

We are piloting “trusted access” which allows developers to retain advanced capabilities while we continue to calibrate policies and classifiers for general availability. Our goal is for very few users to need to join [Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/).

To use models for potentially high-risk cybersecurity work:

- Users can verify their identity at [chatgpt.com/cyber](https://chatgpt.com/cyber)
- Enterprises can request [trusted access](https://openai.com/form/enterprise-trusted-access-for-cyber/) for their entire team by default through their OpenAI representative

Security researchers and teams who may need access to even more cyber-capable or permissive models to accelerate legitimate defensive work can express interest in our [invite-only program⁠](https://docs.google.com/forms/d/e/1FAIpQLSea_ptovrS3xZeZ9FoZFkKtEJFWGxNrZb1c52GW4BVjB2KVNA/viewform?usp=header). Users with trusted access must still abide by our [Usage Policies⁠](https://openai.com/policies/usage-policies/) and [Terms of Use⁠](https://openai.com/policies/row-terms-of-use/).

## False positives

Legitimate or non-cybersecurity activity may occasionally be flagged. When rerouting occurs, the responding model will be visible in API request logs and in with an in-product notice in the CLI, soon all surfaces. If you’re experiencing rerouting that you believe is incorrect, please report via `/feedback` for false positives.

