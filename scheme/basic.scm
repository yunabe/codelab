;; scm basic.scm
(define sum (lambda (x y) (+ x y)))
(define dbl (lambda (x) (* x 2)))
(define twice (lambda (f) (lambda (x) (f (f x)))))
(print (sum 3 4))
(print ((twice dbl) 1))
(exit)
