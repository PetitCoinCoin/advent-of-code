#### https://adventofcode.com/2017

Day 13: first day of 2017 where it takes a little bit loo long. But a little bit more than a minute is still correct.
Then I realised I did not need all the part one treatment and escaped loop early: down to a couple of seconds!

Day 15: clearly not optimised, but runs in less than 1 minute for part one (especially when you realise it is 
40 millions loops, and not 40 billions -_-)

Day 17: I tried to find a pattern to calculate second item in list, without success. Then I realised I did not have to 
actually build the list, so I decreased algorithmic complexity by keeping track of only the second value in list. Went down
to less than 10 sec.

Day 18 looked awfully like assembunny code. So I tried to look at it like last year's advent and understand what it does.
Worked for part 1. But then, I just had to implement the full program.

I'm proud of me on day 21: first idea was the good one. Instead of flipping and rotating each sub-matrix, I only rotated
and flipped rules once, and stored them directly in a dict. This is faster than manipulating matrices.

Day 22 is probably not optimized because part 2 takes few seconds. But it works, I found a solution quickly, and I think it is elegant with complex numbers, so I'm happy.

Had to look for a hint on day 23 part 2. I had the global loop architecture, but did not manage to understand that it was looking for non prime numbers. Once understood, this is pretty straight forward.

Day 24: probably not optimized, but less than 5 seconds seems fine to me.
