# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = .build

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

.PHONY: clean help html dirhtml singlehtml pickle json epub text man texinfo info changes linkcheck doctest spelling

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  epub       to make an epub"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  texinfo    to make Texinfo files"
	@echo "  info       to make Texinfo files and run them through makeinfo"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"

clean:
	-rm -rf $(BUILDDIR)/*

html dirhtml singlehtml:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/$@."

pickle json:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Build finished; now you can process the $@ files."

epub:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Build finished. The $@ file is in $(BUILDDIR)/$@."

text:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Build finished. The $@ files are in $(BUILDDIR)/$@."

man:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/$@."

texinfo:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/$@."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."

info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo $@
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

changes:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "The overview file is in $(BUILDDIR)/$@."

linkcheck:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/$@/output.txt."

doctest:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/$@/output.txt."

spelling:
	$(SPHINXBUILD) -b $@ $(ALLSPHINXOPTS) $(BUILDDIR)/$@
	@echo "Spell checking the sources finished, look at the results in " \
	      "$(BUILDDIR)/$@/output.txt."
