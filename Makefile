SHELL = /usr/bin/env sh -eu
PODMAN = $(shell command -v podman || command -v docker)

FORCE:

.PHONY: help
# List available commands.
help:
	@sed -n '/^\.PHONY: / {N;s/.*: \(\S\+\)\( # \(.*\)\)\?\n# \(.*\)/\1 \3:\4/p}' Makefile | column -ts:


# Manage


.PHONY: init
# Initialize development environment.
init:
	@command -v gh || echo 'Command "gh" not found, see https://cli.github.com'
	@command -v git || echo 'Command "git" not found, see https://git-scm.com'
	@command -v lefthook || echo 'Command "lefthook" not found, see https://lefthook.dev'
	@command -v podman || command -v docker || echo 'Command "podman" not found, see https://podman.io'
	@command -v uv || echo 'Command "uv" not found, see https://docs.astral.sh/uv'
	@command -v yq || echo 'Command "yq" not found, see https://github.com/mikefarah/yq'
	make -B sync

.PHONY: sync
# Synchronize development environment.
sync: .venv
.venv uv.lock &: pyproject.toml
	uv sync --all-extras --all-groups --all-packages

.PHONY: news
# Add changelog news entry.
news:
	uv run scriv create

.PHONY: pre-commit
# Run pre-commit hook.
pre-commit:
	lefthook run pre-commit --all-files

.PHONY: update-dependencies
# Update project dependencies.
update-dependencies:
	uv sync --all-extras --all-groups --all-packages --upgrade
	make build

.PHONY: update-template
# Update project template.
update-template:
	uvx copier update --trust --vcs-ref main
	uv run que wait -p'Resolve merge conflicts and' -a
	make build


# Develop


.PHONY: lint
# Run project linters.
lint:
	lefthook run pre-commit --jobs lint --all-files

.PHONY: build
# Build project.
build: badges docs package requirements

.PHONY: package
# Build package.
package: .tmp/dist
.tmp/dist: src/**/* README.md pyproject.toml uv.lock .venv
	rm -rf $@
	uv build -o .tmp/dist

.PHONY: docs
# Build documentation.
docs: README.md
README.md: docs/*.md
%.md: FORCE
	uv run docsub sync -i $@

.PHONY: badges
# Build project badges.
badges: docs/img/badge/coverage.svg docs/img/badge/tests.svg
docs/img/badge/%.svg: .tmp/%.xml
	mkdir -p $(@D)
	uv run genbadge $* --local -i $< -o $@

.PHONY: requirements
# Export testing requirements.
requirements: tests/requirements.txt
tests/requirements.txt: pyproject.toml uv.lock
	uv export --frozen --no-emit-project --no-hashes --only-group testing > $@

.PHONY: test # [ TOXARGS="..." ]
# Run tests, optionally pass extra args to tox.
test: package requirements
	mkdir -p .tox
ifdef TOXARGS
	${PODMAN} compose run --rm tox run --installpkg="`find .tmp/dist -name '*.whl'`" ${TOXARGS}
else
	${PODMAN} compose run --rm tox run --notest --skip-pkg-install
	${PODMAN} compose run --rm tox run-parallel --installpkg="`find .tmp/dist -name '*.whl'`"
endif

.PHONY: shell # [ SERVICE=tox ]
# Enter service container, tox by default
shell:
	${PODMAN} compose run --rm --entrypoint bash $(or ${SERVICE},tox)

.PHONY: clean
# Clean up intermediate files.
clean:
	rm -rf .coverage .tmp .tox .venv
	find . -name __pycache__ -exec rm -rf {} \;


# Release


.PHONY: seed
# Seed the repository after it is created.
seed:
	uv sync
	make init
	lefthook install

.PHONY: version-bump
# Bump project version.
version-bump:
	@uv run bump-my-version show-bump
	@uv run que --plain --file .tmp/.bump \
	  select -p'Choose version component:' --as component -c'["major","minor","patch"]'
	uv run bump-my-version bump --tag `cat .tmp/.bump | cut -d'=' -f2`
	@rm .tmp/.bump
	uv lock

.PHONY: changelog
# Collect changelog entries.
changelog:
	uv run scriv collect
	sed -e's/^### \(.*\)$$/***\1***/' -i'' CHANGELOG.md

.PHONY: publish
# Publish package on PyPI.
publish: package
	hatch publish .tmp/dist/*.*

.PHONY: merge
# Merge current branch to "main"
merge:
	make build
	make pre-commit
	make github-pullrequest
	uv run que wait -p'Manually merge PR created and' -a
	git switch main
	git fetch
	git pull

.PHONY: release
# Process release branch
release:
	# update version and changelog
	make version-bump
	make changelog
	uv run que wait -p'Proofread the changelog and' -a
	make build
	uv run que wait -p'Proofread changes and commit, then' -a
	make pre-commit
	# tag
	git tag "v`uv run bump-my-version show current_version`"
	git push --tags
	# merge
	make merge
	make github-metadata
	make github-release
	make publish


# GitHub helpers


.PHONY: github-pullrequest
github-pullrequest:
	@git diff --name-only --exit-code
	@git diff --name-only --cached --exit-code
	@git ls-files --other --exclude-standard --directory
	git push
	@export ISSUE_ID=`git branch --show-current | cut -d- -f1` && \
	export ISSUE_TITLE=`GH_PAGER=cat gh issue view "$$ISSUE_ID" --json title -t '{{.title}}'` && \
	  gh pr create --web -t "$$ISSUE_TITLE"

.PHONY: github-release
github-release:
	@[ "`git branch --show-current`" = "main" ] || (echo "Release from "main" branch only." && false)
	@export TAG="v`uv run bump-my-version show current_version`" && \
	  gh release create --draft -t "$$TAG — `date -Idate`" --generate-notes "$$TAG"

.PHONY: github-metadata
github-metadata:
	@export DESCRIPTION=`yq .project.description pyproject.toml` && \
	  gh repo edit -d "$$DESCRIPTION"
	@export HOMEPAGE=`yq .project.urls.Documentation pyproject.toml | sed '/^https:\/\/github.com/d'` && \
	  gh repo edit -h "$$HOMEPAGE" || true
	@export REPO=`git config --get remote.origin.url | sed 's|.*/\(.*/.*\)\.git$$|\1|'` && \
	export OLD_TOPICS=`GH_PAGER=cat gh api "repos/$$REPO" | yq -r '.topics | join(" ")'` && \
	  [ -n "$$OLD_TOPICS" ] && \
	  gh repo edit `echo " $$OLD_TOPICS" | sed 's/ / --remove-topic /g'` || true
	@export NEW_TOPICS=`yq -r '.project.keywords | join(" ")' pyproject.toml` && \
	  gh repo edit `echo " $$NEW_TOPICS" | sed 's/ / --add-topic /g'`
	@gh label create "code of conduct" --force -c D73A4A -d "Code of Conduct issues"
