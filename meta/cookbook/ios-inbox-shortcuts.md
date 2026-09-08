---
name: ios-inbox-shortcuts
what: Two iPhone Shortcuts that drop a dated, provenance-stamped note into sources/inbox/ from anywhere on the phone, one for typing and pasting, one as a share-sheet target for links, text, and images
type: workflow
requires: iPhone with the Shortcuts app; Obsidian mobile with the vault open and Obsidian Sync (or any sync that carries sources/ and attachments/); no accounts, no keys
effort: ~20 minutes to build both by hand, following the steps below tap by tap
suggest_when: the user wants to capture something to the inbox from their phone, mentions seeing something on mobile they wanted remembered, or says the inbox is only reachable from the desktop
status: recommended
---

# iOS inbox shortcuts: phone capture into sources/inbox/

Apple's Shortcuts app can open an Obsidian URL that creates a note at an exact vault path with prefilled content, and can save a file into the vault's folder on the phone. Two small shortcuts built on that give the phone a real inbox: one creates a dated note and hands you to the Obsidian editor to type or paste (images included, since Obsidian's paste puts them in the attachments folder and embeds them), the other sits in the share sheet and takes whatever an app offers, a link, selected text, a photo, or a screenshot. Nothing else is in the loop: no AI, no third-party service, no server. The vault's sync layer carries the note to the machine where the pipeline runs. Obsidian's URL scheme is documented at [obsidian.md/help/Extending Obsidian/Obsidian URI](https://obsidian.md/help/Extending+Obsidian/Obsidian+URI). Obsidian's own share extension is not the right tool here: it files into the vault's default new-note folder and its format is fixed, so a shared item would land as a note, not an inbox drop.

## Why this is here

The vault this program came from had a working inbox for months, reachable from the desktop only. The friction that earned this recipe: the user, on his phone, read a course announcement, acted on it (accepted a GitHub invite), and wanted to drop the details into the inbox for the next morning's run, with nothing to do it. His words: "there is the daily note I could have posted there, but I was really looking for an inbox. Somewhere I could paste and type whatever info and context and know that the next morning run will ingest it." Both shortcuts were built and verified the same night. The unlock is that capture stops being a desk activity. The moment something is worth remembering is usually on the phone, and the gap between that moment and the desk is where captures die.

## What you'll end up with

- A Home Screen icon (or Action Button binding) called **Inbox Note**. Tap it and Obsidian opens on a fresh note at `sources/inbox/<yyyy-MM-dd-HHmm>-phone-capture.md` whose first line reads `Me, <date time>, from phone:` with the cursor below it. Type, paste text, paste images. Leave.
- A share-sheet entry called **Share To Inbox** in every app. Share a link, text selection, photo, or screenshot and Obsidian opens on `sources/inbox/<yyyy-MM-dd-HHmmss>-phone-share.md` with the same header and the shared thing already in the body: a link or text inline, an image saved to `attachments/` and embedded. Add context in the editor, or don't.
- Both notes reach the pipeline machine through the vault's sync within about a minute, while Obsidian is open. Ingest treats the provenance header as the user's own dated speech and an embedded image as a cited attachment.

## Setup

Everything here is the user's hands on their phone. The agent's job is to walk them through it and verify the result on the pipeline machine (see Verify). Two facts to pin before starting: the vault's name as Obsidian shows it (the folder name; `exocortex` in the steps below, substitute yours), and where the vault lives in the Files app (with Obsidian Sync it is **On My iPhone → Obsidian → <vault>**; with iCloud it is **iCloud Drive → Obsidian → <vault>**).

Three Shortcuts quirks shape the steps, and skipping them cost an hour the first time:

- The **URL** action is secretly a list, and a stray Return while typing splits the address in two. Build the full address in a **Text** action instead and hand that to Open URLs.
- A **Subpath** or name field takes one variable or plain text, not a mix. Build the filename in its own Text action and insert that.
- Inside an **If** block, an action with a dim placeholder input (Convert Image showing a grey "Image") has no input at all. Set it to Shortcut Input explicitly.

### Shortcut 1: Inbox Note

1. Open **Shortcuts** → tap **+** → tap the title → **Rename** → `Inbox Note`.
2. Add **Format Date**. Date: **Current Date**. Date Format: **Custom**. Format String: `yyyy-MM-dd-HHmm`. (This is the filename stamp.)
3. Add a second **Format Date**. Current Date, Custom, Format String: `yyyy-MM-dd h:mm a`. (This is the readable header date.)
4. Add **Text**. Type `Me, `, tap **Select Variable** and pick the *second* Format Date (the one whose string starts `yyyy-MM-dd h`), type `, from phone:`, then press Return twice.
5. Add **URL Encode**. Its input should auto-fill with the Text from step 4.
6. Add **Text**. On one line with no Returns: `obsidian://new?vault=exocortex&file=sources%2Finbox%2F`, then Select Variable → the *first* Format Date (string starts `yyyy-MM-dd-H`), then `-phone-capture&content=`, then Select Variable → **URL Encoded Text**.
7. Add **Open URLs**. Tap its pill → Select Variable → the Text from step 6.
8. **Done**. Long-press the shortcut card → **Add to Home Screen**. Optionally Settings → Action Button → Shortcut → Inbox Note.

### Shortcut 2: Share To Inbox

1. **+** → rename to `Share To Inbox`. Tap the ⓘ → toggle on **Show in Share Sheet** → Share Sheet Types: leave **Any** (or tick everything) → Done. A **Receive ... from Share Sheet** block appears at the top; set "If there's no input" to **Continue**.
2. Add **Format Date**: Current Date, Custom, `yyyy-MM-dd-HHmmss` (seconds, so two shares in one minute don't collide).
3. Add **Format Date**: Current Date, Custom, `yyyy-MM-dd h:mm a`.
4. Add **Get Type**. Input: Shortcut Input.
5. Add **If**. First field → Select Variable → **Type**. Condition: **is**. Value: `Image`.
6. Inside the If, above Otherwise, in this order:
   - **Convert Image**. Tap the dim **Image** field → Select Variable → **Shortcut Input**. Format: **JPEG**. Quality about 80%.
   - **Text**: Select Variable → the *first* Format Date, then type `-phone-share.jpg`. (The filename.)
   - **Set Name**. Input: **Converted Image**. Name: Select Variable → the filename Text.
   - **Save File**. Input: **Renamed Item**. Toggle **Ask Where To Save** off. Tap the destination pill and navigate to the vault's `attachments` folder → Open. In **Subpath** → Select Variable → the filename Text.
   - **Text**: `Me, ` + *second* Format Date + `, from phone (shared image):`, Return, Return, `![[` + the filename Text + `]]`, Return, Return.
7. Under **Otherwise**: **Text**: `Me, ` + *second* Format Date + `, from phone (shared):`, Return, Return, Select Variable → **Shortcut Input**, Return, Return.
8. Below **End If**: **URL Encode**. Input → Select Variable → **If Result**.
9. **Text**, one line: `obsidian://new?vault=exocortex&file=sources%2Finbox%2F` + *first* Format Date + `-phone-share&content=` + **URL Encoded Text**.
10. **Open URLs** → that Text. **Done**.

If the Save File destination pill refuses to pin the vault folder, toggle **Ask Where To Save** on instead; the Subpath row disappears (Set Name then supplies the filename) and each share pops a folder picker where the user navigates to `attachments` and taps Open. One extra tap, same result.

## Verify it works

1. Tap **Inbox Note**, type a word, paste an image, leave. On the pipeline machine within a minute: a file `sources/inbox/<stamp>-phone-capture.md` with the header, the word, and a `![[Pasted image ...]]` line, and the PNG in `attachments/`.
2. Share a photo from Photos to **Share To Inbox**. Expect `sources/inbox/<stamp>-phone-share.md` embedding `<stamp>-phone-share.jpg`, and the jpg in `attachments/`. If the note arrives but the jpg does not, the Convert Image input is unset (quirk three above).
3. Share a page from Safari. Expect the URL in the note body.
4. Delete the test captures before the next pipeline run, or let ingest quarantine them.

Sync only runs while Obsidian is open, which is why both shortcuts end by opening the note rather than writing silently. A note written and immediately backgrounded still arrives the next time Obsidian opens.
