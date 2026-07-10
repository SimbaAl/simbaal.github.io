# simbaal.github.io

Personal academic portfolio of Dr Simbarashe Aldrin Ngorima.
Static site, no build step, hosted free on GitHub Pages.

## Structure

```
index.html          The experience: three.js signal-lock hero, GSAP scroll
                    narrative, HUD sync readout, gait visualisation
publications.html   Full publications, preprints and presentations
assets/
  aldrin.jpg        Headshot
  Ngorima_CV.pdf    Downloadable CV
  vendor/           three.js r128, GSAP 3.12 + ScrollTrigger (self-hosted,
                    no CDN dependency)
```

## Updating the live site

Edit files, then:

```bash
git add .
git commit -m "Describe your change"
git push
```

The live site updates within a minute or two.

## Design notes

- Dark "instrument" sections and paper "printout" sections alternate
  deliberately; the HUD strip at the bottom shows scroll progress as SYNC %.
- The hero is ~1,700 three.js particles converging from channel noise into a
  16QAM constellation; it responds to the cursor like phase error.
- All motion respects the visitor's reduced-motion preference: the loader is
  skipped, the constellation renders locked, reveals appear instantly.
- Everything is self-hosted; the only external requests are Google Fonts.

## Maintenance checklist

- [ ] Update the "Now" section every month or two. A stale Now section is
      worse than none.
- [ ] When papers are accepted, change the status pills from "under review"
      and update publications.html.
- [ ] Optional: add a DOI link for the SATNAC 2024 paper when available.
- [ ] Optional: custom domain later (Settings → Pages → Custom domain).
