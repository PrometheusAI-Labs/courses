# Prometheus AI Labs: Courses

## Онлайн-курсы

**[Открыть каталог курсов →](https://prometheusai-labs.github.io/courses/)**

Сайт на GitHub Pages: https://prometheusai-labs.github.io/courses/

Five interactive courses with a shared static catalog.

- `nautilus/`: three Russian-language NautilusTrader courses, plus learning materials and third-party notices.
- `rust-incubator-course/`: Rust Incubator, six modules in Russian.
- `rust-training-course/`: Inside Microsoft's Rust Training, five modules in English.

## Local preview

Run `python3 -m http.server 8000` from this directory.

## Validation

```sh
python3 scripts/verify_site.py
python3 nautilus/verify_courses.py
```

## Publishing

GitHub Pages publishes the repository root from `main`. `.nojekyll` keeps the prebuilt files intact. No build step or external service is required. Push a commit to `main` to update the site.

This repository contains only the course packages, not the original source checkouts, downloaded video archives, credentials, or personal learning records.

Existing licensing and attribution are preserved in `nautilus/LICENSE.md`, `nautilus/THIRD_PARTY_NOTICES.md`, and `nautilus/LICENSES/`. No blanket license is granted for third-party content. These are independent educational materials, not official programs of the companies mentioned.
