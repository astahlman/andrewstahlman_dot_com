(require 'org)

(setq org-confirm-babel-evaluate nil)

;; TODO: Put this in project.org
(require 'ox)
(with-eval-after-load 'ox-html
    (add-to-list 'org-html-mathjax-options '(path "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML")))

;; TODO: Put this in project.org
(setq org-export-with-sub-superscripts `{})

(defun build-website ()
  "Publish the project to build/"
  (progn
    (org-babel-do-load-languages
     'org-babel-load-languages
     '((emacs-lisp . t)
       (shell . t)
       (python . t)
       (perl . t)
       (java . t)))
    (find-file "./project.org")
    (org-babel-execute-buffer)))
