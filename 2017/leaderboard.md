        --------Part 1---------   --------Part 2--------
    Day     Time   Rank  Score       Time   Rank  Score
    21      >24h   8439      0       >24h   8340      0
    20      >24h  10489      0       >24h   9829      0
    19      >24h  11002      0       >24h  10871      0
    18      >24h  12042      0       >24h  10216      0
    17      >24h  12631      0       >24h  11959      0
    16      >24h  13442      0       >24h  12383      0
    15      >24h  13700      0       >24h  13362      0
    14      >24h  12769      0       >24h  11976      0
    13      >24h  15137      0       >24h  13933      0
    12      >24h  16258      0       >24h  15655      0
    11      >24h  16421      0       >24h  15860      0
    10      >24h  17644      0       >24h  16010      0
    9       >24h  19516      0       >24h  19029      0
    8       >24h  22228      0       >24h  21647      0
    7       >24h  25426      0       >24h  19876      0
    6       >24h  27945      0       >24h  26761      0
    5       >24h  31949      0       >24h  30307      0
    4       >24h  36280      0       >24h  32700      0
    3       >24h  37650      0       >24h  28253      0
    2       >24h  53717      0       >24h  46070      0
    1       >24h  65105      0       >24h  54662      0

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
