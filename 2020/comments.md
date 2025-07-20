#### https://adventofcode.com/2020

Back to python! Yeah I work in Typescript now, so I want to keep up to date with Python. I plan to learn a new language for the next "past" year.

Day 4: sure, I could have use regex! But why bother when a million "if" can do the trick.

I'm so happy I understood what was happening under the hood for day 5. I'm always confused when it is about binary manipulation. But this one felt easy. Nevertheless, I'm pretty sure that if I had done it "live" (I mean, in Decembre 2020), I would have gone for a more "bruteforce" approach. No time to think!

I didn't expect the bruteforce approach to work for day 9...

Day 11 is the starting day of increased runtimes \o/ (3~4sec)

CRT spotted for day 13! But the example was so unclear to me!

Once again, the difficulty here was more to understand what was expected. For part 2, it took me a while to understand that mask application changed (0 is not enforced anymore).

I knew Day 15 part 2 would be this kind of evolution. I expected a faster runtime (~15sec), but looking at reddit, it appears that I'm not the only one having such time.

Out of curiosity I looked at reddit for day 16 and realized I've got lucky: I didn't have any '0' invalid field. I would have been stuck for a loooong time in part 2!

I thought I was being clever for using recursion in day 18 but `maximum recursion depth exceeded` got me!

Day 19 was fun! Also I'm kinda disappointed we had a hint directly in the puzzle. I'm sure it would have taken me way more time without it. But I also would have liked to see if I gained experience on this and if the idea of checking my input occured to me. Anyway, liked it! Also, tried to cache, but it had no impact for part 1 (which ran in about 0.7sec). I refactored part 1, based on part 2, and it now runs in ~2ms (both parts).

Day 20 may not be the most beautiful answer, but it's rather quick, and I found it myself, so I'm realatively happy!

Day 22 was surprinsingly easy... if you carefuly read the instructions! It took forever until I read it correctly. About 6sec for part 2. Not that bad for day 22! Anyway, I liked this one a lot.

New achievement unlocked for day 23 part 1: solved on a cellphone! But I had to get an hint for part 2. I kept my part 1 with linked list for "archive" purpose, but the data representation suggested on Reddit allowed my code for part 2 to run in less than 5sec (instead of days !)

I'm relatively happy with my solution for day 24. But the code seems so ugly, idk. Anyway, part 2 runs in 10sec, which is not great, but not that bad either. At first it ran in about 50sec, but I managed to narrow the borders' tiles of the floor area to update.

I had to try the bruteforce approach for day 25. I'm surprised it worked, even though it's clearly suboptimal (it ran in almost 3sec, I narrowed it to ~1.5sec with the use of `pow` function). Looking at Reddit for a more "mathematical" solution, it seems I'm not the only one to chose the bruteforce path! The theory behind was to use Fermat's Little Theorem, but when I tested it out of curiosity, it didn't seem quicker...
