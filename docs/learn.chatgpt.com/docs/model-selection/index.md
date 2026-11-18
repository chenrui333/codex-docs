---
source_type: 'learn'
source_area: 'learn_model_selection'
source_url: 'https://learn.chatgpt.com/docs/model-selection'
source_kind: 'learn_markdown'
---

# Model selection

Source: https://learn.chatgpt.com/docs/model-selection

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Meet the models

<ModelOverview />

Availability, tools, reasoning settings, and usage limits differ by product and
model version. Check the [models available in ChatGPT](https://learn.chatgpt.com/docs/models) or the
[API model catalog](https://developers.openai.com/api/docs/models).

## Find the right model for your workflow

Choose a task and a priority to see a suggested model and reasoning effort.

<ModelRecommender client:load />

## How to think about models and reasoning effort

  To optimize usage, start with the suggested model and reasoning effort. Check
  which settings your plan offers and how much of your allowance the task uses.

1. **GPT-6 Luna · Low**

   Making small edits to files and extracting fields when the expected result is clear.

2. **GPT-6 Luna · Extra high**

   Finding updates across apps, prioritizing follow-ups, and solving problems with clear constraints.

3. **GPT-6.1 Terra · Medium**

   Navigating desktop apps, updating records, and making focused fixes you can verify.

4. **GPT-6.2 Sol · Medium**

   Fixing bugs and adding features in an existing codebase, or drafting documents for review.

5. **GPT-6.2 Sol · Extra high**

   Working through multistep tasks that need testing and revision along the way.

6. **GPT-6.2 Astra · Low**

   Turning a clear brief into polished work that's ready to use.

7. **GPT-6.2 Astra · Medium**

   Planning and carrying out complex projects, adjusting the approach as new information comes in.

8. **GPT-6.2 Astra · Extra high**

   Solving open-ended problems that require weighing trade-offs and testing assumptions.

**Model strengths**

Farther from the center means a stronger fit for that type of work. The ratings are high-level estimates based on benchmarks, independently run task examples, and user feedback.

Models ordered by estimated fit for each type of work

| Type of work | Models from strongest fit to weakest fit |
| --- | --- |
| 3D and design | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna |
| Software engineering | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna |
| Data analysis | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna |
| Creating deliverables | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna |
| Computer use | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna |
| Research decisions | GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna |

### Experiment

Treat the guidance on this page as a starting point. The best way to find the right
model for your workflow is to experiment with different models and reasoning
settings to see what works.

Start by considering:

- **How often does your workflow run?** A frequent automation makes usage and cost
  add up faster than an occasional project.
- **How quickly do you need the result?** A task you're waiting on may need a
  faster setting than one that runs overnight.
- **How will you use the output?** A draft for your review may need less polish
  than something you'll share externally.
- **How important is the quality of the result?** Depending on your use case or
  industry, you might want to use a stronger model to put an emphasis on quality.

If you can, experiment using the same inputs to compare results and keep the
lightest setting that meets your quality bar.

Choose acceptance criteria before comparing models:

- **Writing:** check required facts, qualifications, audience, and voice. Review
  both outputs before deciding whether the shorter one is more useful.
- **Computer use:** reopen the affected record or page to verify saved changes,
  confirm that the workflow preserved unrelated data, and compare the completion
  report with the actual result.
- **Code and interfaces:** run regression tests. For an interactive application,
  also inspect the rendered result on desktop and mobile.

Repeat the comparison across representative tasks. Measure completion time
alongside quality, including time spent reviewing or repairing the result. Then
vary reasoning effort while keeping the model and inputs fixed.
