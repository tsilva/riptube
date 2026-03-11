PYTHON ?= python3

.PHONY: check-clean check-main current-version release release-patch release-minor release-major

check-clean:
	@test -z "$$(git status --porcelain)" || (echo "Working tree must be clean before releasing."; exit 1)

check-main:
	@test "$$(git branch --show-current)" = "main" || (echo "Releases must be created from main."; exit 1)

current-version:
	@$(PYTHON) scripts/bump_version.py --current

release-patch: VERSION_PART=patch
release-patch: release

release-minor: VERSION_PART=minor
release-minor: release

release-major: VERSION_PART=major
release-major: release

release: check-clean check-main
	@test -n "$(VERSION_PART)" || (echo "Set VERSION_PART to patch, minor, or major."; exit 1)
	@NEW_VERSION="$$( $(PYTHON) scripts/bump_version.py $(VERSION_PART) )"; \
	uv lock; \
	git add pyproject.toml riptube/__init__.py uv.lock; \
	git commit -m "chore: release $$NEW_VERSION"; \
	git push origin main; \
	echo "Pushed $$NEW_VERSION to main. GitHub Actions will publish it to PyPI."
