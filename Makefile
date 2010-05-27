CSS_FILES := $(patsubst %.sass, %.css, $(wildcard css/*.sass))

all: $(CSS_FILES)

%.css: %.sass
	sass --style=compressed <$< >$@
