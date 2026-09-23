# Training & Mentorship tracks

Three tracks, three owners. Only **AI** is a public offering today. DevOps and Development are taught inside cohorts and are not standalone services (decision 2026-09-24; see `app/services/platform/content/registries/tracks.yaml`).

| Track | Owner | Status | Where the material lives |
|---|---|---|---|
| AI | Sarfi | final | `training-materials/<course>/` (25 courses, `curriculum.yaml`) |
| DevOps and deployment | Sachin | draft | `training-materials/tracks/devops/` — same kit convention: `demos/NN_name.py`, generated guide, exercises |
| Development / SDE | Harsh | draft, language not decided | `training-materials/tracks/development/` |

To add a course to a draft track: `python scripts/new_course.py <id> "<title>" --hours 8 --track devops` (or `development`), write two demos, run `python scripts/build_course_kits.py`. The track's `status` in `tracks.yaml` stays `draft` until Sarfi and the owner mark it `final`; the website shows only `final` tracks as offerings.
