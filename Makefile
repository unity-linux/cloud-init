NAME=cloud-init
DISTREL=2
VERSION=0.7.9

RPMBUILD=$(shell which rpmbuild)
CAT=$(shell which cat)
SED=$(shell which sed)
RM=$(shell which rm)
SPECTOOL=$(shell which spectool)

all:

$(NAME).spec: $(NAME).spec.in
	@$(CAT) $(NAME).spec.in | \
		$(SED) -e 's,@VERSION@,$(VERSION),g' | \
		$(SED) -e 's,@DISTREL@,$(DISTREL),g' \
			>$(NAME).spec
	@echo
	@echo "$(NAME).spec generated in $$PWD"
	@echo

spec: $(NAME).spec

get:
	@echo
	@echo "Downloading Sources"
	@echo
	@$(SPECTOOL) -gf $(NAME).spec
	@echo
	@echo "Downloading Sources Finished"
	@echo

srpm_build:
	$(RPMBUILD) "--define" "_sourcedir $(shell pwd)" "--define" "_topdir $(shell pwd)" -bs $(NAME).spec
	@$(RM) -rf SOURCES SPECS BUILD BUILDROOT RPMS

srpm: spec get srpm_build

clean:
	@$(RM) -f *.spec
	@$(RM) -rf SRPMS RPMS SOURCES SPECS BUILD BUILDROOT
	@$(RM) -rf *.tar.*
	@find -name '*~' -exec $(RM) {} \;
	@echo
	@echo "Cleaning complete"
	@echo
