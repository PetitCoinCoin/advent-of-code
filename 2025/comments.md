#### Ready to decorate the North Pole: https://adventofcode.com/2025

Wow. Day 1 part 2 gave me way too much trouble. I had to tick 1 by 1 to finally get the correct answer, and then rework my code to make it work.

Day 2 is really unefficient, even for part 1 (I had a solution in ~0.7sec but decided to group part 1 and 2 in the same function and it increased - don't know why I like it when both parts can work with the same logic).
Edit: reworked this day a little and went from ~7.5sec to ~4.5sec for part 2. I think there is something clever to do and not test all ids in a range. Once you have an invalid id, the next one in the range cannot be invalid. But I don't have it yet.

Day 3 was fun. I knew in part 1 that there should be better than bruteforce, but went for it anyway. Well, I had to think this through in part 2 XD.

Day 4 part 2 can probably be optimized (it runs in ~0.5 sec). But I got to use my new helpers, and I can use part 1 for part 2 with clean code, so I'm happy :)

Meh. Poor choice of DS for day 5 part 1, and then, I struggled with the merge of the ranges. At least it's efficient.

Late to the party for day 6. It wasn't so difficult, but it was fun to manipulate the data.

Day 7 part 1 is a bit less efficient once grouped with part 2 (one could only use set, and give up the timelines dict for part 1) but that's alright.

I'm tired of me as I had a really silly mistake for day 8 part 1 (index error instead of using `math.prod`). By the time I fixed that, it was to get ready for the day... then part 2 was quite quick. Well, not the runtime (~4sec) but it's quick enough. I saw nice tricks to optimize the solution, that's interesting! Edit: updated to merge the circuits on the fly. It's way better.

Wow day 9 part 2 wasn't easy. I really need to get some theory about polygons and how to detect if a point is inside it. This one would need some improvement.

Day 10 part 2 took me the whole day, but I'm really happy with it, even though it's really slow (about 20min). I identified systems of equations, and new I already solved such with sympy for 2023, day 24. But I want to only use standard libraries, so I tried to build a solver on my own. Well, I did. It's inefficient, I already see several possible optimizations, but it works! And I got to use `itertools` and discovered `Fraction`! 

Of course I tried to solve day 12 with a general algorithm. I flipped, rotated, and tried a lot. It did work on the test input, but it already took 5min tu run. So I figured, maybe I could narrow the candidates - which wouldn't work for the example, but that wouldn't be the first time the test is not solved the same way as the real input. It turns out, that was the only thing expected, and I now have my last star ⭐
