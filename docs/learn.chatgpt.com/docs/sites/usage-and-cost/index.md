---
source_type: 'learn'
source_area: 'learn_sites'
source_url: 'https://learn.chatgpt.com/docs/sites/usage-and-cost'
source_kind: 'learn_markdown'
---

# Usage and cost

Source: https://learn.chatgpt.com/docs/sites/usage-and-cost

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

We plan to show your Sites hosting usage in the app starting **January 1, 2027**. Hosting is free through **January 31, 2027**. We plan to start charging Plus, Pro, and Business customers for hosting usage above their monthly allowance on **February 1, 2027**. Enterprise billing follows your organization’s agreement.

You can create as many sites as you want. Building and editing them count toward your plan’s [Codex usage](https://learn.chatgpt.com/docs/pricing). Hosting covers the traffic your sites receive and the storage they use.

## Monthly hosting allowances

On Plus, Pro, and Business, all your sites share one monthly hosting allowance.

| Plan                      | Monthly hosting allowance                             |
| ------------------------- | ----------------------------------------------------- |
| Plus                      | 125 credits                                           |
| Pro                       | 375 credits                                           |
| Business                  | 125 credits per seat                                  |
| Enterprise (credit-based) | Draws from your organization’s contracted credit pool |

If your Enterprise agreement uses a dollar commitment, Codex tokens and Sites hosting have separate rates. Both draw from the same commitment. For example, $10 of Codex usage and $2 of hosting use $12 of the commitment. Ask your account team for your hosting rates.

## Hosting usage rates

Use these approximate credit rates to estimate hosting costs.

| What you use                                                       | Billing unit             | Approx. credits |
| ------------------------------------------------------------------ | ------------------------ | --------------- |
| Site without storage                                               | 1 Site per month         | 0               |
| Site with storage, including an empty database                     | 1 Site per month         | 25              |
| Traffic                                                            | 100,000 requests         | 15              |
| Database storage (saved records, such as form responses)           | 1 GiB stored for a month | 150             |
| File storage (uploaded files, such as images or PDFs)              | 1 GiB stored for a month | 3.75            |
| Custom domain (domain registration costs extra)                    | 1 domain per month       | 25              |
| Site–tunnel connection to a private system (Enterprise plans only) | 1 connection for 30 days | 125             |

A request loads a page, image, or other resource. One page visit typically generates 30–50 requests, depending on the site.

A site with an empty database uses about 25 credits per month before traffic. If it stores 1 GiB of records for the full month, the base fee and database storage together use about 175 credits. One GiB is about 1.07 GB.

### Private connections on Enterprise

A Site–tunnel connection costs approximately 125 credits for 30 days, prorated daily. Each Site–tunnel pair counts once per UTC day, even if the Site is unpublished or sends no traffic. A tunnel with no Sites attached during the day counts as zero connections.

- Three Sites that share one tunnel count as three connections, even if they attach at different times that day.
- One Site attached to two tunnels counts as two connections, including when it switches from one tunnel to the other.
- Disconnecting and reconnecting the same Site to the same tunnel on the same UTC day counts as one connection.

## Estimate your monthly cost

Choose an example site or enter your monthly requests, database storage, and file storage. Select your plan to see how much of your hosting allowance the site would use.

<SitesCostEstimator
  client:load
  plans={[
    { label: "Plus", monthlyCredits: 125 },
    { label: "Pro", monthlyCredits: 375 },
    { label: "Business", monthlyCredits: 125, perSeat: true },
    { label: "Enterprise" },
  ]}
  rates={{
    traffic: { credits: 15, requests: 100000 },
    monthlyStorageBase: 25,
    databasePerGiB: 150,
    filesPerGiB: 3.75,
  }}
/>

Estimates assume a full month of storage. Select **This Site has a database** to include its base fee even when saved records are zero. For custom domains and Enterprise Site–tunnel connections, add the charges listed under [Hosting usage rates](#hosting-usage-rates).
