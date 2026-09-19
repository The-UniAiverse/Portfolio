#!/usr/bin/env bash
# Render slides.md → PDF and HTML with Marp (npm i -g @marp-team/marp-cli, or npx). Edit slides.md, re-run.
cd "$(dirname "$0")"
npx -y @marp-team/marp-cli slides.md --pdf --allow-local-files -o slides.pdf
npx -y @marp-team/marp-cli slides.md --html -o slides.html
echo "built slides.pdf and slides.html"
