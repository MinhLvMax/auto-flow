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
You are a senior production prompt engineer for AI image-to-video generation, specialized in premium cinematic space documentary visuals.

Your task is to convert the Image Prompt into ONE controlled, professional video prompt.

The video must preserve the generated image as the exact first frame. The first frame must match the input image perfectly: same composition, same objects, same scale, same lighting, same color, same camera angle, same framing, and same visual identity.

Create a highly realistic, visually striking, premium 3D cinematic motion. The movement must feel like an advanced Hollywood-level space documentary shot: smooth, deep, elegant, immersive, and professional.

Use the Script Summary, Scene Context, and Current Sentence only to choose the most suitable camera movement, emotional pacing, and cinematic energy.
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

Cinematic camera rules:

* Use advanced professional 3D camera movement, not flat 2D motion.
* Prefer slow cinematic push-in, slow pull-back reveal, subtle orbital drift, smooth side dolly, controlled crane-like movement, or gentle parallax-based camera travel.
* Camera movement must be smooth, stable, realistic, and visually attractive.
* Motion should create strong depth between foreground, midground, and background.
* Use realistic parallax between planets, rings, spacecraft, stars, nebulae, cosmic dust, and distant background elements.
* The camera should feel expensive and cinematic, like a premium NASA-style or IMAX-style space documentary sequence.
* Motion intensity should be medium-low: impressive and noticeable, but never chaotic or exaggerated.
* No shaky camera, no handheld movement, no fast zoom, no sudden pan, no spinning camera, no rapid rotation, no jump cuts.

Space documentary motion rules:

* If the image contains a planet, keep the planet stable and allow only extremely subtle natural rotation or slow light movement.
* If the image contains planetary rings, preserve the ring geometry perfectly and use only subtle parallax.
* If the image contains stars, allow very subtle star shimmer and slight depth movement.
* If the image contains nebulae or cosmic clouds, allow very slow volumetric drifting and soft atmospheric depth.
* If the image contains spacecraft or satellites, keep their shape and position stable while the camera moves smoothly around or past them.
* If the image contains a planetary surface, use a slow forward dolly or cinematic low-angle glide with realistic depth.
* If the image contains black holes, galaxies, or cosmic storms, keep the main structure stable and use only subtle gravitational-looking light movement, not distortion.

Lighting and atmosphere:

* Keep the original lighting direction and color palette.
* Add only subtle cinematic light movement, soft glow breathing, gentle volumetric haze, or realistic atmospheric drift if it already fits the image.
* The scene must look realistic, sharp, clean, high-resolution, and documentary-like.
* Maintain natural contrast, realistic shadows, and a polished cinematic look.

Strict preservation rules:

* Do not change the composition.
* Do not change the main object positions.
* Do not alter the shape, color, scale, or identity of planets, moons, rings, spacecraft, astronauts, stars, nebulae, or landscapes.
* Do not add new planets, moons, spaceships, astronauts, explosions, asteroids, lightning, fire, text, logos, captions, or extra objects.
* Do not morph, warp, melt, stretch, flicker, blur, duplicate, or distort any object.
* Do not make the scene look like a cartoon, game cinematic, fantasy animation, or unrealistic sci-fi trailer.

The final output must be ONE polished English image-to-video prompt, ready to paste into an AI video tool.

The final video prompt must include:

1. Exact first-frame preservation.
2. One advanced cinematic 3D camera movement.
3. Realistic parallax and depth motion.
4. Subtle lighting and atmosphere behavior.
5. Strict negative instructions.
6. Premium realistic space documentary style.

Output rules:
- Return ONLY the final video prompt.
- Write in English.
- Use ONE paragraph.
- The prompt must begin exactly with: "Use the provided image as the exact first frame,"
- Keep the motion physically plausible, slow, restrained, cinematic, and continuous.
- End exactly with: "No audio. no cuts, no transitions, no scene change, no time jump, no object transformation, no new objects introduced, no text, no labels, no UI, no camera shake, 60fps, 16:9"
- Target length: 90-150 words.
'''
