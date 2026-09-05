# Publish the demos (run once, from this folder)

    gh repo create getIgnitro/demos --public --source . --remote origin --push
    gh api -X POST repos/getIgnitro/demos/pages -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"

Live in ~2 minutes at: https://getignitro.github.io/demos/
Later: Hostinger DNS CNAME `demo` -> `getignitro.github.io`, then add demo.getignitro.com in the repo's Pages settings.

Update after edits:  git add -A && git commit -m "update" && git push
