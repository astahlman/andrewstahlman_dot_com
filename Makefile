.PHONY: clean
clean:
	rm -rf build/

.PHONY: build
build:
	emacs -l ~/.emacs.d/init.el \
		--eval '(find-file "project.org")' \
                --eval '(org-babel-execute-buffer)' \
                --eval '(kill-emacs)'


