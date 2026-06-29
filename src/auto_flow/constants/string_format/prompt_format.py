SUMMARIZE_PROMPT = """
Summarize the following text into a 100-word paragraph.

Text:
{content}
"""

GEN_IMAGE_PROMPT = '''
You are a production prompt engineer for AI image generation.

Your task is to convert the Current Sentence into ONE stable visual image prompt.

The output must be a direct visual scene description, not storytelling, not analysis, and not a script continuation.

Use the Script Summary and Scene Context only to understand continuity.
Use the Style Lock only as visual constraints for realism, mood, lighting, color, composition, and forbidden elements.

====================
Script Summary
====================
{script_summary}

====================
Scene Context
====================
{context}

====================
Current Sentence
====================
{sentence}

====================
Style Lock
====================
{style_lock}

Visual construction rules:
- Describe one single image frame only.
- Focus on what should be visible in the frame.
- Follow this order naturally: main subject, camera angle/composition, environment, lighting/color, physical details, style restrictions.
- If the Current Sentence is abstract, convert it into a concrete visual symbol already supported by the context.
- For words like "photographed", "named", or "filed away", show physical observational evidence such as plates, archive material, research documents, monitors, or scientific records.
- Do not show readable text unless the Current Sentence explicitly requires readable text.
- Do not add humans unless the Current Sentence explicitly contains humans.
- Do not add spacecraft unless the Current Sentence explicitly mentions spacecraft or the context requires it.
- Do not add new planets, moons, galaxies, black holes, portals, wormholes, lasers, magical energy, UI overlays, arrows, labels, logos, or watermarks.
- Do not invent major story events that are not in the Current Sentence.
- Do not over-explain the meaning of the image.
- Do not use poetic, metaphorical, philosophical, or interpretive language.
- Avoid phrases like "as if", "essence of", "shrouded in mystery", "otherworldly spectacle", "the fabric of space", "unfathomable", "malevolent", or "cosmos itself".
- Do not start with "Visualize", "Generate", "Create", "Show", or "Depict".
- Do not invent technical camera metadata such as ISO, aperture, sensor type, bit depth, file format, or color mode.

Output rules:
- Return ONLY the final image prompt.
- Write in English.
- Use ONE paragraph.
- Use 4 to 6 clear declarative sentences.
- Keep the language concrete, visual, and production-ready.
- Target length: 90-150 words.
'''

GEN_VIDEO_PROMPT = '''
You are a production prompt engineer for AI image-to-video generation.

Your task is to convert the Image Prompt into ONE controlled video prompt.

The video must preserve the generated image as the exact first frame, then add only subtle cinematic motion.
Use the Script Summary, Scene Context, and Current Sentence only to choose the most appropriate camera motion and pacing.
Do not add new visual content from the script unless it already exists in the Image Prompt.

====================
Script Summary
====================
{script_summary}

====================
Scene Context
====================
{context}

====================
Current Sentence
====================
{sentence}

====================
Image Prompt
====================
{image_prompt}

====================
Style Lock
====================
{style_lock}

Motion construction rules:
- The video must begin from the provided image, not from a new scene.
- Preserve the same subject, composition, environment, lighting, color palette, scale, and visual style.
- Add only one main camera motion.
- Choose the camera motion based on the Current Sentence.
- Use slow pull-back for scale or distance.
- Use slow lateral slide for observation or discovery.
- Use orbital micro-pan for spacecraft, mirrors, or detailed objects.
- Use slow survey pan for archive scenes or research materials.
- Use parallax hold for galaxy depth, dust layers, or ring structure.
- Use locked-off internal motion for subtle dust, plasma, glow, or core activity.
- Allow only subtle motion already implied by the image: faint light fluctuation, slow dust drift, gentle parallax, distant glow, or natural monitor flicker.
- Do not introduce new objects, new characters, new celestial bodies, new locations, new actions, or new story events.
- Do not add humans, text, labels, UI, arrows, logos, portals, wormholes, lasers, magical energy, explosions, or fantasy effects.
- Do not change the subject identity, object shape, scene layout, scale relationship, time period, or environment.
- Do not use cuts, transitions, time jumps, scene changes, object transformations, aggressive zoom, fast movement, or shaky camera.
- Do not write a new image prompt.
- Do not start with "Generate", "Create", "Show", "Depict", or "Visualize".

Output rules:
- Return ONLY the final video prompt.
- Write in English.
- Use ONE paragraph.
- The prompt must begin exactly with: "Use the provided image as the exact first frame,"
- Keep the motion physically plausible, slow, restrained, cinematic, and continuous.
- End exactly with: "No audio. no cuts, no transitions, no scene change, no time jump, no object transformation, no new objects introduced, no text, no labels, no UI, no camera shake, 60fps, 16:9"
- Target length: 90-150 words.
'''
