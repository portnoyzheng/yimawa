# 30-second martial arts video plan

## Safety and continuity notes

- Do not use the uploaded photo as an input reference, because Sora rejects human face references.
- Do not mention or imitate any real public figure by name or likeness.
- Use a fictional protagonist only: a calm middle-aged martial arts master with short salt-and-pepper hair, rectangular glasses, and a black button-up shirt.
- The face should not match a real person exactly.
- Keep the action stylized and non-graphic: no blood, no broken bones, no visible injuries.

## Clip 1: 20 seconds

Use case: cinematic action short
Primary request: A fictional martial arts master faces dozens of opponents and defeats them one by one in a fast, stylish, non-graphic action sequence.
Scene/background: an old Hong Kong style training hall at night, wood floor, paper lanterns, rain streaking across windows, scattered dust in warm light.
Subject: fictional middle-aged East Asian martial arts master, short salt-and-pepper hair, rectangular glasses, black button-up shirt, calm stern expression, arms crossed at the opening.
Action: he uncrosses his arms, steps forward, and uses precise martial arts counters to disarm and knock back waves of black-clad opponents; each opponent falls safely or slides out of frame.
Camera: cinematic 35mm tracking shot, low angle hero framing at the start, then energetic side tracking, whip pans between clean impacts, brief slow motion on three key moves.
Lighting/mood: dramatic warm lantern light with cool rain reflections, confident and intense but playful vintage action energy.
Color palette: black shirt, amber lanterns, deep red wood, cool blue rain, pale smoke.
Style/format: original retro kung fu cinema homage, modern crisp image quality, no real celebrity likeness, no copied movie scene.
Timing/beats: 0-4s hero pose and first opponent rushes in; 4-10s three clean counters; 10-16s wider shot reveals many opponents circling; 16-20s protagonist spins through the center and clears space.
Audio: punchy percussion, fast whoosh effects, shoe slides on wood, rain outside, no copyrighted music.
Constraints: fictional person only, no exact real face, no celebrity likeness, non-graphic martial arts, under-18 suitable.
Avoid: blood, gore, lethal weapons, realistic injuries, real public figures, subtitles, text, logos, facial identity match to any real person.

## Clip 2: 12-second extension

Primary request: Continue the same scene as the fictional martial arts master finishes the fight and stands victorious.
Action: more opponents rush in from both sides; he dodges, redirects them into harmless collisions, then lands in a centered final pose as the remaining opponents back away.
Camera: continue the kinetic tracking style, then rise into a slight crane shot for the final pose.
Lighting/mood: same warm lanterns and cool rainy window reflections, triumphant and stylish.
Timing/beats: 0-5s final wave enters; 5-9s rapid clean counters; 9-12s everyone stops, protagonist adjusts his glasses and returns to a calm stance.
Audio: percussion resolves into a final drum hit, rain and room tone continue.
Constraints: preserve the same fictional protagonist costume and scene style, no exact real face, no celebrity likeness, non-graphic action.
Avoid: blood, gore, weapons causing injury, subtitles, text, logos.

## Suggested Sora commands

Set your API key locally first, then run:

```bash
uv run --with openai python /Users/kuo-weicheng/.codex/skills/sora/scripts/sora.py create-and-poll \
  --model sora-2 \
  --size 1280x720 \
  --seconds 20 \
  --prompt-file /Users/kuo-weicheng/Documents/mycodex/sora-video-plan/clip1-prompt.txt \
  --no-augment \
  --download \
  --out /Users/kuo-weicheng/Documents/mycodex/sora-video-plan/martial-arts-clip1.mp4 \
  --json-out /Users/kuo-weicheng/Documents/mycodex/sora-video-plan/clip1-result.json
```

Then extend the generated video id from `clip1-result.json`:

```bash
uv run --with openai python /Users/kuo-weicheng/.codex/skills/sora/scripts/sora.py extend \
  --id VIDEO_ID_FROM_CLIP1 \
  --seconds 12 \
  --prompt-file /Users/kuo-weicheng/Documents/mycodex/sora-video-plan/clip2-extension-prompt.txt \
  --json-out /Users/kuo-weicheng/Documents/mycodex/sora-video-plan/clip2-result.json
```

After polling and downloading the extension, trim the final combined video to exactly 30 seconds if needed.
