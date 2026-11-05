# Video-production route check

Read this for a broad video-production search from varied inputs **or** a broad search from finished narration to a contentful video. It records one observed failure mode: a search for “audio to video” can repeatedly return stock-footage assemblers, waveform videos, or subtitle tools while missing a different route that times **new explanatory scenes** to a finished narration. This is a search aid, not a repository catalog or proof that any tool works.

## Compare substantive results

For each user-supplied starting point, name the least additional input a project needs and the final artifact. Group results by **what creates the visual content**, not by whether the file is MP4 or the wrapper is a Skill/MCP/CLI. Do not count a storyboard, template, draft, single clip, waveform card, or caption-only render as an equivalent completed explainer or edited film.

| Starting point | Decision-changing routes to consider | Failure to check |
|---|---|---|
| Topic, article, or script | Existing stock-media matching; generated imagery/video; diagrams or motion graphics rendered from code; optional TTS and final mux | A topic→new TTS workflow may require re-recording when the user already has narration. A document loader may only extract text. |
| **Finished voiceover**, ideally with its script | (1) transcript-driven stock-media matching; (2) generation of new image/video shots; (3) **word/phrase timing → semantic shot plan → code-rendered explanatory graphics/scenes → final MP4** | Audio wrapped in a colored MP4, waveform, captions, or a manually filled scene timeline does not perform the third transformation. Check if the project actually aligns the finished voice, plans contentful shots, renders them, and muxes the supplied audio. |
| Song | Audio-reactive/lyric visualizer; edited footage timed to beat; newly generated narrative MV | A lyric preview or waveform is narrower than a narrative music video. Check whether lyrics, visuals, or original footage must be supplied. |
| Photos or raw footage | Slideshow; semantic selection/rough cut; transcript/highlight-based edit; reference-guided re-edit | A silence remover does not select story beats. Existing footage may be mandatory. |
| Reference video | Style/beat extraction and planning; use of owned footage; new-asset generation or code re-creation | A plan or editable draft alone is not a finished new film, and a style reference may not supply the new video's content. |

For the finished-voiceover route, run a targeted query that **combines** the supplied audio, the missing alignment/semantic-scene operation, and the visual production mechanism. Examples without project names: `voiceover word alignment semantic scenes motion graphics explainer`; `narration script forced alignment storyboard Remotion video`; `已有配音 逐字对齐 语义分镜 动效 视频`. Try repository metadata and, when needed, web content search; the indexes return different surfaces. If the combined query has few useful hits, split it into shorter input-plus-operation and operation-plus-mechanism queries; zero hits from a long conjunction do not show the route is empty. Vary `word-level/forced alignment`, `semantic shots/storyboard`, and `motion graphics/animation/Manim/Remotion`. An `audio to video` query or one that says only `kinetic typography` does not test the same route. Keep this branch open if no suitable source survives inspection.

For any apparent match, read its real input contract: finished audio alone or audio **plus exact script**, already timed SRT, visual assets, model/API keys, editor, human scene approval, platform, license, and final export path. Distinguish a documented pipeline from a static implementation and from a successful test. A result from a code-rendered explainer does not automatically satisfy a stock-footage or general editing request; compare only when its visual form could meet the user's goal.

This card names a known blind spot, not a fixed quota of searches. Use the user's actual constraints to defer irrelevant branches with reasons. A real candidate supplied by the user still belongs in the known-lead ledger even if none of these query examples returns it.
