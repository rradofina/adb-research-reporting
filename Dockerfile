# Reproducibility-anchor Dockerfile.
# Constitution §11. A clean clone of the repository at any tag should
# reproduce the exact computed values when run inside this image.
#
# Build:
#   docker build -t adb-research:latest .
# Run interactively at repo root:
#   docker run --rm -it -v "$PWD":/workspace adb-research:latest

FROM node:24-bookworm-slim AS base

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System packages: git for repo metadata, ca-certs for HTTPS, python3 +
# pip for the program pipelines that use Python (process-bgd.py,
# process-disagreement.py, etc.), curl for ad-hoc API checks, jq +
# csvkit for cache inspection during development.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
        curl \
        jq \
        python3 \
        python3-pip \
        python3-venv \
        build-essential \
        sqlite3 \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# DuckDB CLI — used for parquet-driven pipelines (Ookla, etc.).
ARG DUCKDB_VERSION=1.1.3
RUN curl -fsSL "https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-amd64.zip" -o /tmp/duckdb.zip \
    && unzip /tmp/duckdb.zip -d /usr/local/bin \
    && rm /tmp/duckdb.zip

# tsx for TypeScript pipeline execution without a build step.
RUN npm install -g tsx@4.19.2

# Python tooling. requirements lock pinned in pyproject when added; for
# now we install the small set the existing pipelines import.
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install \
        requests==2.32.3 \
        pandas==2.2.3 \
        pyarrow==18.1.0 \
        duckdb==1.1.3 \
        beautifulsoup4==4.12.3 \
        lxml==5.3.0
ENV PATH="/opt/venv/bin:${PATH}"

# Workspace. The repo is bind-mounted at runtime; this is the default cwd.
WORKDIR /workspace

# Verification step: scripts CI can also run.
CMD ["bash"]
