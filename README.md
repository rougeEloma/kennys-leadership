# Kenny's leadership site: sources

The live site (branch `main`, deployed on Render) is generated from this branch.

- `build.py` holds the page content (directors, bios, social links, gallery intros) and the design.
- `gallery/<slug>/` holds each director's photos, shown in filename order; `captions.json` maps each file to its caption.
- `site/assets/` holds the logo and the photos used on the homepage and portraits.

Rebuild (needs Python 3 and Pillow):

    python3 deploy.py        # writes the static site to deploy/

Then copy `deploy/` into the `main` branch and push; Render redeploys automatically.
