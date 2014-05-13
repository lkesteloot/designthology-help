
.PHONY: default dev prod

HELP_PATH=/opt/idwebtool/help

default:
	@echo "make dev|prod"

dev:
	python parseMarkdown.py . $(HOME)/go/src/idwebtool/dist/$(HELP_PATH)

prod:
	python parseMarkdown.py . $(HELP_PATH)