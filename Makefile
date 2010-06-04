CSS_FILES := $(patsubst %.sass, %.css, $(filter-out css/fonts.sass, $(wildcard css/*.sass)))

all: $(CSS_FILES)

%.css: %.sass css/fonts.sass
	sass --style=compressed $< $@
