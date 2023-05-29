(define factorial (
	
		   lambda (num) (cond
				  ((zero? num) 1)
				  (#t (* num (factorial (- num 1))))
				  )
		   )
  )
(begin (display (factorial (read))) (newline))
