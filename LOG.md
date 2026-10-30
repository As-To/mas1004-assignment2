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

## Step 3 : balanced (Track A)

- changed: In `sample_weights`, counted the photos for each city and returned a weight of `1 / city_count` for each photo, so every city is drawn equally often. No other training-recipe change was made.
- why: I wanted to test whether drawing every city equally often would improve the baseline before making another change.
- validation: 0.5062 (before: 0.4936; change: +0.0126)
- per-city accuracy: Seoul 0.4982 (before: 0.5721, -0.0739); Busan 0.4475 (before: 0.3705, +0.0770); Tokyo 0.5017 (before: 0.6238, -0.1221); Osaka 0.4718 (before: 0.3548, +0.1170); Taipei 0.6121 (before: 0.5466, +0.0655)
- what it means: The overall validation score increased by 0.0126. Accuracy increased for Busan, Osaka and Taipei, but decreased for Seoul and Tokyo. The largest increase was for Osaka, and the largest decrease was for Tokyo.

Next, I plan to decide what to try based on the mistake sheets and these per-city results.

## Step 3 – Baseline mistake analysis

I looked at the most confidently misclassified validation photos for all five cities and noticed two main patterns.

1. City confusion

The model mostly confuses Seoul with Busan and Tokyo with Osaka. This is particularly noticeable in the Busan and Osaka mistake sheets, where many photos are predicted as Seoul and Tokyo respectively. However, it also makes mistakes between cities from different countries.

Examples:
- Busan confused forr Seoul: images 1, 4, 7, 8, 10
- Osaka confused for Tokyo: images 1, 2, 5, 7, 9
- Seoul cnfused for Tokyo: images 1, 4, 6
- Taipei confused for Tokyo: images 2, 3, 6
- Tokyo confused Seoul: images 1, 2, 3

2. Lack of distinctive clues

Many mistakes involve ordinary streets, buildings, indoor scenes or foods, where it is difficult to identify the exact city. I also noticed several photos showing mostly nature, such as trees or parks, without clear clues that culd help about their location.

Examples of nature or green spaces:
Seoul: images 1, 10, 46
Busan: images 27, 38

Other examples:
Seoul: images 2, 7, 12 (food, car, indoor scene)
Busan: images 17, 19, 31 (ordinary urban scenes)
Tokyo: images 4, 21 (cars nit in the road)
Osaka: images 2, 9, 13 (ordinary streets and roads)
Taipei: images 9, 13, 16 (similar-looking roads)
