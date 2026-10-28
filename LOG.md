# Log

One entry for each recipe, selection or Track B model you train, newest at
the bottom. The numbers come from `experiments.csv`. "Why" and "what it means"
are in your own words: your agent asks you for them and does not make them up.
End the log with your plan for what to try next.

<!-- The form of an entry:

## <date> <tag> (Track A or B)
- changed: what is different from the run before
- why: your reason
- validation: 0.000 (before: 0.000)
- what it means: what you think the result says
-->

## Step 1 : Initial dataset observations 

Many photos are not actual street scenes. There are pictures of food, car parts, people, museums and indoor spaces. Some images have clear clues about their location, but others could have been taken almost anywhere.

I feel that recognizing the country seems easier than recognizing the exact city. For example, the writing alphabet on signs can help distinguish the country, but it doesn't necessarily help distinguish Seoul from Busan, for example.

For Busan, I noticed quite a lot of beaches and coastal views, which could be useful clues. There were also several metro stations, temples and houses with traditional rooftops with colors. However, I don't think coastal views alone would be enough to identify Busan, since other cities can also have coastal areas.

For Seoul, I noticed some palaces with people wearing hanbok, as well as views of the Han River. There were also many photos of roads with cars. I wonder whether car brands like Hyundai or Kia could help recognize Korea, although these brands are also found in other countries.

In Osaka's samples, I noticed several bridges, some of them with an arched shape, as well as temples, train stations and cherry blossom trees. There was also a particular long white train that caught my attention. I'm not sure how specific these elements are to Osaka though, especially since Tokyo also has many train stations and temples.

For Taipei, I noticed quite a few scooters in the street photos, which might help recognize the city. There were also many trees and green areas, Chinese signs and temples with roofs that looked a bit different from the ones in the other cities. I also noticed several photos of ceramics, probably taken in museums.

For Tokyo I noticed train stations, temples and roads, but these are also present in Osaka's samples. I couldn't really find a clear difference between the two just by looking at these photos.

I also thought about traffic direction as a possible clue. In Japan, cars drive on the left, while in Korea and Taiwan they drive on the right. This could help distinguish Japanese cities from the others, but it wouldn't help much with distingushing Tokyo from Osaka.

## Step 2 : Starter recipe baseline (Track A)

- changed: Ran the starter recipe with seeds 0 and 1, as instructed, to get a baseline before making any changes and see how much the results vary depending on the random seed.
- why: I ran the starter recipe with seeds 0 and 1 as instructed, to get a baseline before making any changes and see how much the results vary depending on the random seed.
- validation: 0.4936 (seed 0); 0.4998 (seed 1); difference: 0.0062
- what it means: The scores are very close, with a difference of only 0.0062. This suggests that changing the seed didn't have much impact on the overall score in these two runs. The model performs better on Tokyo and Seoul than on Osaka and Busan. I'm not sure why yet.

Next, I plan to look at the model's mistakes, as described in Step 3, to better understand which cities it confuses and whether there are any patterns in the errors.

