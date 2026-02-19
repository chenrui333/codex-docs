# Worktrees

Source: https://developers.openai.com/codex/app/worktrees

In the Codex app, worktrees let Codex run multiple independent tasks in the same project without interfering with each other. For Git repositories, [automations](/codex/app/automations) run on dedicated background worktrees so they don’t conflict with your ongoing work. In non-version-controlled projects, automations run directly in the project directory. You can also start threads on a worktree manually.

## What’s a worktree

Worktrees only work in projects that are part of a Git repository since they use [Git worktrees](https://git-scm.com/docs/git-worktree) under the hood. A worktree allows you to create a second copy (“checkout”) of your repository. Each worktree has its own copy of every file in your repo but they all share the same metadata (`.git` folder) about commits, branches, etc. This allows you to check out and work on multiple branches in parallel.

## Terminology

- **Local checkout**: The repository that you created. Sometimes just referred to as **Local** in the Codex app.
- **Worktree**: A [Git worktree](https://git-scm.com/docs/git-worktree) that was created from your local checkout in the Codex app.

## Why use a worktree

1. Work in parallel with Codex without breaking each other as you work.
2. Start a thread unrelated to your current work
   - Staging area to queue up work you want Codex to start but aren’t ready to test yet.

## Getting started

Worktrees require a Git repository. Make sure the project you selected lives in one.

1. Select “Worktree”

   In the new thread view, select **Worktree** under the composer.
   Optionally, choose a [local environment](/codex/app/local-environments) to run setup scripts for the worktree.
2. Select the starting branch

   Below the composer, choose the Git branch to base the worktree on. This can be your `main` / `master` branch, a feature branch, or your current branch with unstaged local changes.
3. Submit your prompt

   Submit your task and Codex will create a Git worktree based on the branch you selected. By default, Codex works in a [“detached HEAD”](https://git-scm.com/docs/git-checkout#_detached_head).
4. Verify your changes

   When you’re ready, follow one of the paths [below](#verifying-and-pushing-workflow-changes)
   based on your project and flow.

## Verifying and pushing workflow changes

Worktrees look and feel much like your local checkout. But **Git only allows a branch to be checked out in one place at a time**. If you check out a branch on a worktree, you **can’t** check it out in your local checkout at the same time, and vice versa.

Because of this, choose how you want to verify and commit changes Codex made on a worktree:

1. [Work exclusively on the worktree](#option-1-working-on-the-worktree). This path works best when you can verify changes directly on the worktree, for example because you have dependencies and tools installed using a [local environment setup script](/codex/app/local-environments).
2. [Work in your local checkout](#option-2-working-in-your-local-checkout). Use this when you need to bring changes back into your main checkout, for example because you can run only one instance of your app.

### Option 1: Working on the worktree

If you want to stay exclusively on the worktree with your changes, turn your worktree into a branch using the **Create branch here** button in the header of your thread.

From here you can commit your changes, push your branch to your remote repository, and open a pull request on GitHub.

You can open your IDE to the worktree using the “Open” button in the header, use the integrated terminal, or anything else that you need to do from the worktree directory.

![Worktree thread view with branch controls and worktree details](/images/codex/app/worktree-light.webp)

Remember, if you create a branch on a worktree, you can’t check it out in any other worktree, including your local checkout.

If you plan to keep working on this branch, you can [add it to the sidebar](#adding-a-worktree-to-the-sidebar). Otherwise, archive the thread after you’re done so the worktree can be deleted.

### Option 2: Working in your local checkout

If you don’t want to verify your changes directly on the worktree and instead check them out on your local checkout, click **Sync with local** in the header of your thread.

You will be presented with the option of creating a new branch or syncing to an existing branch.

You can sync with local at any point. To do so, click **Sync with local** in the header again. From here, you can choose which direction to sync (to local or from local) and a sync method:

- **Overwrite**: Makes the destination checkout match the source checkout’s files and commit history.
- **Apply**: Calculates the source changes since the nearest shared commit and applies that patch onto the destination checkout, preserving destination commit history while bringing over source code changes (not source commits).

![Sync worktree dialog with options to apply or pull changes](/images/codex/app/sync-worktree-light.webp)

You can create multiple worktrees and sync them to the same feature branch to split up your work into parallel threads.

In some cases, changes on your worktree might conflict with changes on your local checkout, for example from testing a previous worktree. In those cases, you can use the **Overwrite local** option to reset the previous changes and cleanly apply your worktree changes.

Since this process uses Git operations, any files that are part of the `.gitignore` file won’t be transferred during the sync process.

## Adding a worktree to the sidebar

If you choose option one above (work on the worktree), once you have created a branch on the worktree, an option appears in the header to add the worktree to your sidebar. This promotes the worktree to a permanent home. When you do this, it will never be automatically deleted, and you can even kick off new threads from the same worktree.

## Advanced details

### How Codex manages worktrees for you

Codex will create a worktree in `$CODEX_HOME/worktrees`. The starting commit will be the `HEAD` commit of the branch selected when you start your thread. If you chose a branch with local changes, the uncommitted changes will be applied to the worktree as well. The worktree will *not* be checked out as a branch. It will be in a [detached HEAD](https://git-scm.com/docs/git-checkout#_detached_head) state. This means you can create several worktrees without polluting your branches.

### Branch limitations

Suppose Codex finishes some work on a worktree and you choose to create a `feature/a` branch on it using **Create branch here**. Now, you want to try it on your local checkout. If you tried to check out the branch, you would get the following error:

```
fatal: 'feature/a' is already used by worktree at '<WORKTREE_PATH>'
```

To resolve this, you would need to check out another branch instead of `feature/a` on the worktree.

If you plan on checking out the branch locally, try Workflow 2 ([sync with local](#option-2-working-in-your-local-checkout)).

Why this limitation exists

Git prevents the same branch from being checked out in more than one worktree at a time because a branch represents a single mutable reference (`refs/heads/<name>`) whose meaning is “the current checked-out state” of a working tree.

When a branch is checked out, Git treats its HEAD as owned by that worktree and expects operations like commits, resets, rebases, and merges to advance that reference in a well-defined, serialized way. Allowing multiple worktrees to simultaneously check out the same branch would create ambiguity and race conditions around which worktree’s operations update the branch reference, potentially leading to lost commits, inconsistent indexes, or unclear conflict resolution.

By enforcing a one-branch-per-worktree rule, Git guarantees that each branch has a single authoritative working copy, while still allowing other worktrees to safely reference the same commits via detached HEADs or separate branches.

### Worktree cleanup

Worktrees can take up a lot of disk space. Each one has its own set of repository files, dependencies, build caches, etc. As a result, the Codex app tries to keep the number of worktrees to a reasonable limit.

Worktrees will never be cleaned up if:

- A pinned conversation is tied to it
- The worktree was added to the sidebar (see above)

Worktrees are eligible for cleanup when:

- It’s more than 4 days old
- You have more than 10 worktrees

When either of those conditions are met, Codex automatically cleans up a worktree when you archive a thread, or on app startup if it finds a worktree with no associated threads.

Before cleaning up a worktree, Codex will save a snapshot of the work on it that you can restore at any point in a new worktree. If you open a conversation after its worktree was cleaned up, you’ll see the option to restore it.

## Frequently asked questions

Can I control where worktrees are created?

Not today. Codex creates worktrees under `$CODEX_HOME/worktrees` so it can
manage them consistently.

Can I move a session between worktrees?

Not yet. If you need to change environments, you have to start a new thread in
the target environment and restate the prompt. You can use the up arrow keys
in the composer to try to recover your prompt.

What happens to threads if a worktree is deleted?

Threads can remain in your history even if the underlying worktree directory
is cleaned up. However, Codex saves a snapshot of the worktree prior to
cleaning it up and offers to restore it if you reopen the thread associated
with it.

