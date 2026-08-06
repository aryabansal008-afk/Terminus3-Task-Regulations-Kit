# syntax=docker/dockerfile:1
# Terminus 3 environment Dockerfile template
# REGULATIONS.md §6 / docker_environment_review/

# --- Builder stage (only if compilation is required for this task) ---
# Digest-pin here too. Delete this stage entirely if nothing needs compiling.
# FROM REPLACE_ME@sha256:REPLACE_WITH_REAL_DIGEST AS builder
# WORKDIR /build
# COPY <narrow-source-path>/ ./
# RUN <build-command>

# --- Final runtime stage ---
# Digest-pin. Use an approved Terminal-Bench base image where possible;
# if not, document the justification for a non-canonical base right here.
FROM REPLACE_ME@sha256:REPLACE_WITH_REAL_DIGEST

# OCI metadata labels (Doc 6 — "OCI metadata labels" compliance item)
LABEL org.opencontainers.image.title="REPLACE_TASK_NAME" \
      org.opencontainers.image.description="REPLACE_SHORT_DESCRIPTION" \
      org.opencontainers.image.source="REPLACE_REPO_URL_IF_APPLICABLE"

# Install stable, infrequently-changing dependencies FIRST (cache-friendly
# layer ordering) — pin every version, consolidate apt operations, never
# `apt-get upgrade`, and clean caches in the SAME layer as the install.
RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux=REPLACE_PIN \
    asciinema=REPLACE_PIN \
    && rm -rf /var/lib/apt/lists/*

# If a builder stage was used above, copy only the built artifacts —
# narrow COPY, not COPY . . — and prefer --chmod/--chown over a separate
# RUN chmod/chown layer.
# COPY --from=builder --chmod=755 /build/output /app/output

# Do NOT COPY solution/, tests/, secrets/credentials, expected outputs, or
# any verifier-only assets into this image.
# COPY solution/ /solution/     <-- forbidden, do not uncomment
# COPY tests/ /tests/           <-- forbidden, do not uncomment

WORKDIR /app

# Task files LAST (most frequently changing — cache-friendly ordering).
# Prefer narrow COPY over `COPY . .`.
# COPY <specific-task-files> /app/

# Ensure parent directories for every artifact referenced in task.toml
# `artifacts` and in instruction.md actually exist at container start.
