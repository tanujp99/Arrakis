# Arrakis

A personal fork of the [Dune](https://github.com/sakasakiking/Dune) theme for
[Playnite](https://github.com/JosefNemec/Playnite) Desktop Mode, reshaped for
using Playnite as a **catalog** of owned games across platforms rather than as a
launcher.

Forked from Dune 0.9.4. All of Dune's original look and dual light/dark modes are
intact; the changes are structural.

## What differs from Dune

**Grid view overview panel** — the right-hand details panel is a single column of
cards instead of a two-column split, and is narrow by default (480px, with the
ThemeModifier slider floor lowered from 1024 to 360 so it can be dragged down).
The play / install / context action buttons and the install-directory block are
gone, since nothing here is launched from Playnite. Remaining fields are grouped
into three cards:

- **Play Stats** — data about *this copy*: platform, library, time played, last
  played, date added, completion status, achievements.
- **Details** — data intrinsic to the game: developer, publisher, series, release
  date, age rating, region, scores, categories, features, tags.
- **How Long To Beat** — a hand-built horizontal card. The HLTB plugin's own
  control lays out vertically, which does not fit a narrow panel.

**Platform banners on grid tiles** — eShop-style banners across the top of each
cover, driven by the
[ThemeExtras](https://github.com/felixkmh/ThemeExtras-for-Playnite) plugin.
Upstream Dune had this scaffolded but unfinished; this fork completes it. Banner
assets are from [Helium](https://github.com/darklinkpower/Helium), plus custom
Switch and Switch 2 art.

Banners are matched purely by filename under `Source/Images/Banners/`, in
priority order: `PlatformSpecId/` → `PlatformName/` → `PluginId/` →
`SourceName/` → `UnknownLibrary.png`. First match wins; no XAML maps platforms to
images.

## Requirements

- Playnite Desktop Mode, theme API 2.8.0+
- [Segoe Fluent Icons](https://learn.microsoft.com/en-us/windows/apps/design/downloads/#fonts)
  (inherited from Dune)
- Optional: **ThemeExtras** for platform banners, **HowLongToBeat** and
  **SuccessStory** for those cards. Each degrades to nothing if not installed.

## Layout

Theme files live in `Source/`. Playnite loads themes from
`Playnite\Themes\Desktop\<theme id>\`, which here is a directory junction
pointing at `Source/`, so edits are live in the app and version-controlled in
one place.

## Credits

- [Dune](https://github.com/sakasakiking/Dune) by **sakasaki** — the base theme.
- [Helium](https://github.com/darklinkpower/Helium) by **darklinkpower** — Dune's
  own ancestor, and the source of the banner assets.
- [ThemeExtras](https://github.com/felixkmh/ThemeExtras-for-Playnite) by
  **felixkmh** — the banner control.

MIT licensed, as is upstream Dune. See [LICENSE](LICENSE).
