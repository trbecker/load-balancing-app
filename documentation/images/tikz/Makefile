.PHONY: all pdf eps png clean

all: pdf eps png

IMAGES:=control_architecture_vertical control_architecture_horizontal \
	monitoring_architecture_vertical monitoring_architecture_horizontal

IMG_PDF := $(foreach img,$(IMAGES),$(img).pdf)
IMG_EPS := $(foreach img,$(IMAGES),$(img).eps)
IMG_PNG := $(foreach img,$(IMAGES),$(img).png)


pdf: $(IMG_PDF)
eps: $(IMG_EPS)
png: $(IMG_PNG)

control_architecture_vertical.pdf control_architecture_horizontal.pdf: control_architecture.tex stylesheet.tex

monitoring_architecture_vertical.pdf monitoring_architecture_horizontal.pdf:  monitoring_architecture.tex stylesheet.tex

%.pdf: %.tikz tikz_template.latex
	pdflatex -jobname=$(basename $<) "\def\inputfile{$<} \input{tikz_template.latex}"

%.eps: %.pdf
	pdftops -eps $<

%.png: %.eps
	convert $< $@

clean:
	rm -fr *.aux *.log *.pdf *.eps
