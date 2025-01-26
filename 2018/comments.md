#### https://adventofcode.com/2018

I'm suprised by day 4. It wasn't that hard, but it wasn't that easy to organize input data. Required much more thinking than I expected, especially for a 4th day.

Initial solution for day 5 ran in about 25sec, and I got both stars with it. I was curious on how to improve that, and saw that someone used a deque. Indeed, it now runs in less than a sec!

I knew while implementing day 9 that naive approach with list would not get me the 2nd star. Indeed! I knew it was a data structure issue, but failed to see what was needed here. Quick look on subreddit to discover Linked list. Nice trick! Glad I learnt this. Moreover I thought "omg, I need to implement a new class!" but it turned out easy!

Day 10 was fun! I love that in order to get the solution, it's not only about math or code.

Day 11 made me discover partial sum.

Day 14 part 2 takes a bit long (almost 20sec) but it runs. And gives the right answer. As it is still reasonable, I'll leave it that way.

I thought my approach would not very efficient, but it is reasonable, and I'm glad I handled it with objects. It runs in about 0.33/1.33sec for part 1/2.

Oh my gelkjcfe. Let's quickly forget about day 17, move on, and never touch this awful code again. This will never - ever - ever be refactored. Never.

Day 19, I finally understood one of those. It took me some time to figure out the loops, but I did :) Fun one.

Had to get some hint for day 20. But I'm still amazed how fast deque is.

First iteration for day 22 part 2 ran in about 35sec because I calculated an arbitrary large map. I went down to ~10sec, which is long, but that'll do.

Couldn't have done day 23 part 2 without [this answer](https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecdqzdg/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button). Nevertheless, I didn't understand the `max(0, dist - r)` so I changed that. Not very happy with myself on this, but at least I'm glad I managed to twist another solution.

For day 24 part 2, I found boost value manually. I thought I would code it with a simple while loop, but for some reason, fight just get stucks at a certain point. It took me long enough to find the correct solution, so I'll leave it as it is.
