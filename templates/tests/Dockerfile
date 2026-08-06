# syntax=docker/dockerfile:1
# Terminus 3 verifier Dockerfile template
# REGULATIONS.md §6, §8 / docker_environment_review/verifier_dockerfile_requirements.md
#
# environment_mode = "separate" means this image is built and run
# independently from environment/Dockerfile — it must build on its own
# and must never depend on network access during testing.

FROM REPLACE_ME@sha256:REPLACE_WITH_REAL_DIGEST

LABEL org.opencontainers.image.title="REPLACE_TASK_NAME-verifier" \
      org.opencontainers.image.description="Verifier image for REPLACE_TASK_NAME"

# Every verifier dependency preinstalled here — nothing installed at
# test-run time, and no network calls in tests/test.sh or test_outputs.py.
RUN pip install --no-cache-dir pytest==REPLACE_PIN

WORKDIR /tests

# Ensure parent directories exist for every artifact declared in
# task.toml `artifacts` before test.sh runs.
# RUN mkdir -p /app/REPLACE_EXPECTED_OUTPUT_DIR
