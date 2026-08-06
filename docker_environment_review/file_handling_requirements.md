# File Handling Requirements

Source: Doc 6.

- `.dockerignore` excludes: `solution/`, `tests/`, build/dependency caches,
  `.git`, `node_modules`, virtual environments, logs, and anything else not
  needed in the image.
- `COPY` instructions are narrow (e.g. `COPY src/ /app/src/`) rather than
  `COPY . .` whenever practical — broad copies both bloat the image and
  risk accidentally including excluded material if `.dockerignore` has a
  gap.
- Source files are copied directly (`COPY`) instead of embedded inline via
  heredocs in the Dockerfile — heredoc-embedded source is harder to review,
  diff, and keep in sync with the real source tree.
- Metadata-preserving copy options (`COPY --chmod=`, `COPY --chown=`) used
  when appropriate, instead of a separate `RUN chmod`/`RUN chown` layer.
- Large archives are extracted during the build (so the final image has
  the extracted contents) instead of remaining compressed in the image
  (which wastes runtime disk I/O and complicates offline execution).
