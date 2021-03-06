BUILDDIR = $(top_builddir)/docs

REF_VERSION = $(PYGOOCANVAS_MAJOR_VERSION).$(PYGOOCANVAS_MINOR_VERSION)
FULL_VERSION = $(REF_VERSION).$(PYGOOCANVAS_MICRO_VERSION)

HTML_STYLE = $(PYGOBJECT_DATADIR)/pygobject/xsl/ref-html-style.xsl
PDF_STYLE = $(PYGOBJECT_DATADIR)/pygobject/xsl/pdf-style.xsl

XMLFILES = 											\
	reference/pygoocanvas-ref.xml					\
	reference/pygoocanvas-hierarchy.xml				\
	reference/pygoocanvas-core-classes.xml			\
	reference/pygoocanvas-canvas-view.xml			\
	reference/pygoocanvas-canvas-model.xml			\
	reference/pygoocanvas-canvas-model-simple.xml


HTMLdir = $(datadir)/gtk-doc/html/pygoocanvas
HTML_DATA =								\
	html/class-hierarchy.html			\
	html/pygoocanvas-core-classes.html	\
	html/class-canvas-view.html			\
	html/class-canvas-model.html		\
	html/class-canvas-model-simple.html	\
	html/index.html						\
	html/index.sgml						\
	html/pygoocanvas.devhelp

CSS_FILES = $(PYGOBJECT_PYGDOCS)/style.css
CSSdir = $(HTMLdir)
CSS_DATA = $(CSS_FILES)

BUILT_SOURCES = 			\
	build_stamp 			\
	reference/builddate.xml	\
	$(HTML_DATA)

CLEANFILES = 				\
	build_stamp 			\
	pygoocanvas-ref.*		\
	reference/builddate.xml	\
	$(HTML_DATA)

EXTRA_DIST = 			\
	$(XMLFILES) 		\
	$(XSLFILES)			\
	$(FIX_XREF)

REFERENCE_DEPS = 		\
	reference 			\
	$(XMLFILES)			\
	$(XSLFILES)

$(HTML_DATA): build_stamp

reference/builddate.xml: $(REFERENCE_DEPS)
	$(PYTHON) -c 'import datetime; print datetime.date.today()' > $@

build_stamp: $(REFERENCE_DEPS)reference/builddate.xml
	xsltproc --nonet --xinclude -o $(BUILDDIR)/html/ \
		 --path $(BUILDDIR)/reference:$(srcdir)/reference \
                 --stringparam gtkdoc.bookname "pygoocanvas" \
                 --stringparam gtkdoc.version ${REF_VERSION} \
                 $(HTML_STYLE) $(srcdir)/reference/pygoocanvas-ref.xml
	$(PYGOBJECT_FIXXREF) -i /usr/share/gtk-doc/html/pygtk/ $(BUILDDIR)/html 
	touch $@

pdf: $(REFERENCE_DEPS) reference/builddate.xml
	xsltproc --nonet --xinclude -o pygoocanvas-ref.fo \
	         $(PDF_STYLE) reference/pygoocanvas-ref.xml
	pdfxmltex pygoocanvas-ref.fo >output </dev/null
