# OREHA website — production source

## Edit this file for the live site

**`/Users/charlottechen/Desktop/oreha/index.html`** is the one and only production page.

Changes to that root file, committed and pushed to `main`, deploy to:

<https://chenicus.github.io/oreha/>

## Current production pouch artwork

Use these files whenever the three product pouches are needed in a layout. They are transparency-trimmed, reusable source assets, so a shared CSS height makes the visible pouches the same size.

- `oreha-peach-normalized.png`
- `oreha-grape-normalized.png`
- `oreha-honey-lemon-normalized.png`

The production page already uses these files. Do not switch it back to the older `oreha-*-transparent.*` or `oreha-peach.*` assets without rechecking visual scale.

## Local folders that are not live

| Location | Purpose | Deploys? |
| --- | --- | --- |
| `index.html` at the project root | Current production site | Yes |
| `publish/` and `publish-fixed/` | Older local exports/snapshots | No |
| `concepts/` | Design explorations and prototypes | No |
| `output/` and `.launch-build/` | Generated local output | No |

## Safe update routine

1. Edit the root `index.html` and its root-level assets.
2. Preview `file:///Users/charlottechen/Desktop/oreha/index.html` locally.
3. Commit and push `main`.
4. Confirm the same change at the live URL above.

If a local file is not at the project root, assume it is an experiment or archive unless this document says otherwise.
