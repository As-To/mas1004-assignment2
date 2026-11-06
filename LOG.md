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


## Step 3 : balanced (Track A)

<30/10/2026> <balanced> (Track A)
- changed: In `sample_weights`, counted the photos for each city and returned a weight of `1 / city_count` for each photo, so every city is drawn equally often. No other training-recipe change was made.
- why: I wanted to test whether drawing every city equally often would improve the baseline before making another change.
- validation: 0.5062 (before: 0.4936; change: +0.0126)
- per-city accuracy: Seoul 0.4982 (before: 0.5721, -0.0739); Busan 0.4475 (before: 0.3705, +0.0770); Tokyo 0.5017 (before: 0.6238, -0.1221); Osaka 0.4718 (before: 0.3548, +0.1170); Taipei 0.6121 (before: 0.5466, +0.0655)
- what it means: The overall validation score increased by 0.0126. Accuracy increased for Busan, Osaka and Taipei, but decreased for Seoul and Tokyo. I expected balancing the cities to help Busan and Osaka, since they had some of the lowest scores in the baseline, and it did. But I was surprised by how much Seoul and Tokyo dropped. So I'm wondering if giving every city exactly the same weight is a bit too aggressive. I might try a less extreme balancing strategy later. For now, I want to test whether removing horizontal flipping helps preserve useful clues like signs and road layouts, without changing how often each city is sampled.

The overall validation accuracy improved from 0.4936 to 0.5062. I decided to test balanced sampling because I had noticed large differences in the number of training photos available for each city.

What I found particularly interesting was that Busan and Osaka improved significantly (+7.70 and +11.70 percentage points), while Seoul and Tokyo dropped (-7.39 and -12.21 points). When examining the baseline mistakes, I had noticed that many Busan photos were predicted as Seoul, and many Osaka photos as Tokyo. I wonder if the original imbalance made the model more likely to predict the cities with more training photos, and whether balanced sampling helped reduce this tendency.

However, the large drops for Seoul and Tokyo make me wonder if equal sampling is too aggressive. A less extreme balancing strategy might offer a better compromise, although I would need to compare the confusion matrices to confirm my hypothesis.



The overall validation accuracy improved from 0.4936 to 0.5062. I decided to test balanced sampling because I had noticed large differences in the number of training photos available for each city.

What I found particularly interesting was that Busan and Osaka improved significantly (+7.70 and +11.70 percentage points), while Seoul and Tokyo dropped (-7.39 and -12.21 points). When examining the baseline mistakes, I noticed that many Busan photos were predicted as Seoul (e.g., images 1, 2 and 9), while many Osaka photos were predicted as Tokyo (e.g., images 1, 4 and 13). These mistakes often involved ordinary streets or roads that looked quite similar across cities in the same country.

I wonder whether the original imbalance made the model more likely to predict Seoul and Tokyo, and whether balanced sampling helped reduce this tendency by giving Busan and Osaka more opportunities to be learned. However, the large drops for Seoul and Tokyo make me wonder if equal sampling is too aggressive. A less extreme balancing strategy might offer a better compromise, although I would need to compare the confusion matrices to confirm this hypothesis.


<30/10/2026> <balanced_no_flip> (Track A)
- changed: Removed only `T.RandomHorizontalFlip()` from `train_transform()`. The equal-city sampling weights from the balanced recipe were kept exactly as they were.
- why: I wanted to test the effect of removing horizontal flips while keeping the balanced recipe.
- validation: 0.4992 (before: 0.5062; change: -0.0070); baseline seed 0: 0.4936 (change vs baseline: +0.0056)
- per-city accuracy: Seoul 0.5125 (balanced before: 0.4982, +0.0143; baseline: 0.5721, -0.0596); Busan 0.4396 (balanced before: 0.4475, -0.0079; baseline: 0.3705, +0.0691); Tokyo 0.5045 (balanced before: 0.5017, +0.0028; baseline: 0.6238, -0.1193); Osaka 0.4398 (balanced before: 0.4718, -0.0320; baseline: 0.3548, +0.0850); Taipei 0.5996 (balanced before: 0.6121, -0.0125; baseline: 0.5466, +0.0530)
- what it means: I expected removing horizontal flipping to help preserve geographical clues such as signs and road layouts. However, the overall accuracy dropped by 0.7 percentage points compared to balanced (from 0.5062 to 0.4992), with the largest drop in Osaka (-3.2 percentage points). However, I've got to say that the difference is qute small. My guess is that the current cropping is quite aggressive, so the model might not see enough signs or road layouts for their orientation to matter much. I'm wondering whether removing flipping could become more useful if I first make cropping less aggressive, allowing the model to see more of the original scene (the scale of the crop in the baseline is 0.35).Maybe the current cropping is too aggressive because by removing too much of the surrounding environment, it could make geographical clues harder to learn. For now, I'll keep flipping and test whether less aggressive cropping helps preserve useful geographical context.


<31/10/2026> <balanced_crop_07> (Track A)
- changed: Changed only `T.RandomResizedCrop()` scale from `(0.35, 1.0)` to `(0.7, 1.0)`. Horizontal flipping was enabled again, and the equal-city sampling weights from the balanced recipe were kept exactly as they were.
- why: I wanted to test whether less aggressive cropping would help preserve useful geographical context.
- validation: 0.4885 (before: 0.5062; change: -0.0177); baseline seed 0: 0.4936 (change vs baseline: -0.0051)
- per-city accuracy: Seoul 0.5101 (balanced before: 0.4982, +0.0119; baseline: 0.5721, -0.0620); Busan 0.4237 (balanced before: 0.4475, -0.0238; baseline: 0.3705, +0.0532); Tokyo 0.5001 (balanced before: 0.5017, -0.0016; baseline: 0.6238, -0.1237); Osaka 0.4243 (balanced before: 0.4718, -0.0475; baseline: 0.3548, +0.0695); Taipei 0.5840 (balanced before: 0.6121, -0.0281; baseline: 0.5466, +0.0374)
- what it means: I expected less aggressive cropping to help the model by keeping more geographical context. However, accuracy dropped by 1.77 percentage points compared to balanced (from 0.5062 to 0.4880). My guess is that stronger cropping actually helps the model learn from smaller parts of the images and creates more variety during training. Since the model sees each photo several times (around 6 times), this variety might help prevent memorization. For now, I'll keep the original cropping and focus on removing training photos that contain little geographical information.
I noticed that many validation mistakes involve outdoor scenes, while some training photos contain little geographical information. Since the training budget is fixed, I wonder whether removing these less useful photos could help the model spend more time learning from street scenes.

When examining the suspects from balanced_no_flip, I noticed that some photos contained potentially useful geographical clues spread across the image, such as the street signs and buildings in Osaka image 48 or the wider urban landscape in Tokyo image 43. I wondered whether aggressive cropping was removing some of this context, making the cities harder to distinguish.

However, validation accuracy dropped from 0.5062 to 0.4885. Osaka had the largest decrease (-4.75 percentage points), followed by Taipei (-2.81) and Busan (-2.38), while Seoul improved slightly. This surprised me because I expected preserving more context to help with street scenes.

Looking again at the suspects, I also noticed that some photos, such as Busan image 19, contain very few distinctive geographical clues even when viewed entirely. This makes me wonder whether preserving more of an image is not always beneficial. Another possible explanation is that stronger cropping helps the model learn from different parts of the same photo, creating more variety during training. Since each photo is presented around six times, this could help the model avoid relying too much on the same visual features.

I would be interested in testing cropping again at a higher image resolution to see whether preserving more visual detail changes the result.

<01/11/2026> <balanced_crop_05> (Track A)
- changed: Changed only `T.RandomResizedCrop()` scale from `(0.35, 1.0)` to `(0.5, 1.0)`. Balanced equal-city sampling and horizontal flipping were kept unchanged.
- why: I wanted to test whether less aggressive cropping would preserve more useful geographical context.
- validation: 0.5034 (before: 0.5062; change: -0.0028)
- per-city accuracy: Seoul 0.5072 (before: 0.4982, +0.0090); Busan 0.4367 (before: 0.4475, -0.0108); Tokyo 0.5305 (before: 0.5017, +0.0288); Osaka 0.4525 (before: 0.4718, -0.0193); Taipei 0.5898 (before: 0.6121, -0.0223)
- what it means: The overall validation accuracy decreased slightly, by 0.28 percentage points. So reducing the cropping from 0.35 to 0.5 didn't really help overall. However, Tokyo improved by 2.88 percentage points, which I found interesting. Maybe keeping more of the original image helps the model recognize Tokyo, while stronger cropping works better for some other cities.
This makes me wonder whether using different cropping scales for different cities could be useful. However, since the overall result is still worse than balanced, I don't think it's worth keeping this change for now. I'll go back to the original cropping scale of 0.35.

<01/11/2026> <filter_indoors_busan> (Track A)

- changed: Removed the 534 explicitly selected Busan training photos with little or no visible geographical information, while keeping the balanced recipe unchanged.

- why: When looking at the validation mistakes, I noticed that the model often struggles with outdoor scenes. At the same time, some training photos show indoor spaces with very few clues about their location. Since the training budget is fixed at 250,000 images, I wonder if removing these photos could help the model spend more time learning from street scenes. For now I am testing my thoery only on Busan.

- validation: 0.5134 (before: 0.5062; change: +0.0072)
- per-city accuracy: Seoul 0.5331 (before: 0.4982, +0.0349); Busan 0.4554 (before: 0.4475, +0.0079); Tokyo 0.5102 (before: 0.5017, +0.0085); Osaka 0.4577 (before: 0.4718, -0.0141); Taipei 0.6108 (before: 0.6121, -0.0013)
- what it means: The overall validation accuracy increased by 0.72 percentage points, which is encouraging, although the improvement is quite small. Busan improved, as I hoped, but what surprised me was that Seoul improved even more (+3.49 percentage points). My guess is that by removing less useful Busan photos, the model might have learned to distinguish Busan from Seoul a little better, so it could be confusing the two cities less often. I would need to check the confusion matrix to confirm this.
Osaka's accuracy decreased by 1.41 percentage points. I'm not really sure why. Maybe changing the Busan training data also affected how the model distinguishes other cities, or maybe this is just some variation between training runs.
Overall, the result makes me want to continue filtering Busan photos, but I can't say yet whether the improvement is reliable.

<02/11/2026> <filter_busan_extended> (Track A)

- changed: Removed 149 additional explicitly selected Busan photos—6 indoor photos and 143 car-focused photos—while preserving the previous 534 exclusions and the balanced recipe.
- why: The suspects for Busan showed some remaining indoor photos and some photos of cars that were probably taken during some sort of car exhibition. I wanted to see whether deleting those could improve the model.
- validation: 0.4997 (before: 0.5134; change: -0.0137)
- per-city accuracy: Seoul 0.5113 (before: 0.5331, -0.0218); Busan 0.4475 (before: 0.4554, -0.0079); Tokyo 0.5022 (before: 0.5102, -0.0080); Osaka 0.4309 (before: 0.4577, -0.0268); Taipei 0.6068 (before: 0.6108, -0.0040)
- what it means: The overall validation accuracy dropped from 0.5134 to around 0.500, and all five cities performed worse. This surprised me because I expected removing more photos with little geographical information to help.
One possible explanation is that some of the car photos I removed were actually useful. For example, they showed Korean car brands like Hyundai or Kia, which might have helped the model recognize Korean environments, even if the photos didn't show much of the city itself. Another possibility is that the validation set contains similar car exhibition photos, so removing these examples from training may have made it harder for the model to recognize them.

<02/11/2026> <filter_busan_press> (Track A)

- changed: Removed manually selected Busan press conference photos while preserving the 534 exclusions from `filter_indoors_busan` and keeping the balanced recipe unchanged.
- why: While reviewing the Busan training photos, I noticed that there were a lot of press conference images. Most of them showed people speaking in front of cameras or microphones, without much geographical information. I wanted to see whether removing these photos would help the model focus on more useful visual features for identifying Busan.
- validation: 0.5088 (before: 0.5134; change: -0.0046)
- per-city accuracy: Seoul 0.5265 (before: 0.5331, -0.0066); Busan 0.4676 (before: 0.4554, +0.0122); Tokyo 0.4983 (before: 0.5102, -0.0119); Osaka 0.4516 (before: 0.4577, -0.0061); Taipei 0.6001 (before: 0.6108, -0.0107)
- what it means: Removing the press conference photos improved Busan accuracy by 1.22 percentage points, which was what I hoped for. When reviewing the training images, I had noticed many press conferences and political events where the main focus was on people rather than the surrounding city. I thought these photos might not help the model learn what Busan looks like. Busan accuracy improved from 0.4554 to 0.468, which suggests that removing press conference photos might have helped the model recognize Busan better. My guess it that by removing press conferences photos that give very little geographic information, the model could be trained on more relevant images for Busan. However, the overall validation accuracy decreased slightly. This is difficult to interpret. I think that might be an interesting filter to apply for other cities if they also have press conferences photos. Looking at the training photos for Seoul and Tokyo I noticed that they also have press conference photos. It could be interesting to try removing them during the training.

<02/11/2026> <filter_busan_firefighters> (Track A)

- changed: Removed 128 additional explicitly selected Busan firefighter or emergency intervention photos while preserving the previous 600 exclusions and the balanced recipe.
- why: I wanted to test whether removing firefighter and emergency intervention photos with little geographical information would improve the model.
- validation: 0.5034 (before: 0.5088; change: -0.0054)
- per-city accuracy: Seoul 0.4977 (before: 0.5265, -0.0288); Busan 0.4417 (before: 0.4676, -0.0259); Tokyo 0.5187 (before: 0.4983, +0.0204); Osaka 0.4384 (before: 0.4516, -0.0132); Taipei 0.6206 (before: 0.6001, +0.0205)
- what it means: Maybe some of firefighters interventions I've decided to remove had interesting features for recognizing the architecture of busan. I expected removing photos of firefighter interventions, especially buildings on fire, to help because I thought the smoke would hide useful geographical information or make the model focus too much on the fire itself. 
What surprised me most was that both Korean cities performed worse: Busan dropped by 2.59 percentage points and Seoul by 2.88 points, while Tokyo and Taipei improved by about 2 points each.
Looking back at the training photos I removed, I wonder if some of them were actually useful. Even when the main subject was an emergency intervention, the background could still contain Korean signs, buildings or street features. Removing these photos may have reduced the visual information helping the model recognize Korean environments. However, I could not examine the mistakes from this experiment because of Colab's GPU limitations, so I cannot confirm this explanation.

<03/11/2026> <filter_indoors_tokyo_seoul> (Track A)

- changed: Removed 591 additional explicitly selected indoor photos—422 from Seoul and 169 from Tokyo—while preserving the previous 534 Busan indoor exclusions and the balanced recipe.
- why: I wanted to test whether removing indoor photos with little or no visible geographical information from Seoul and Tokyo would improve the model.
- validation: 0.5132 (before: 0.5134; change: -0.0002)
- per-city accuracy: Seoul 0.5006 (before: 0.5331, -0.0325); Busan 0.4669 (before: 0.4554, +0.0115); Tokyo 0.5233 (before: 0.5102, +0.0131); Osaka 0.4615 (before: 0.4577, +0.0038); Taipei 0.6139 (before: 0.6108, +0.0031)
- what it means: The overall validation accuracy remained almost unchanged, but the results differed across cities. Tokyo improved slightly, while Seoul dropped by 3.25 percentage points. One possible explanation is that some of the removed indoor photos from Seoul still contained useful visual clues, such as Korean signs or distinctive interiors. Removing them may have reduced the diversity of the training data. Another possibility is that the Seoul validation set contains more indoor scenes than Tokyo's, making these exclusions more harmful for Seoul. 

<03/11/2026> <filter_museum_objects> (Track A)

- changed: Removed 454 additional manually selected museum-object photos from Busan, Seoul, and Tokyo while preserving all previous exclusions and the balanced recipe.
- why: I wanted to test whether removing indoor photos focused on museum objects, with little or no visible geographical information, would improve the model.
- validation: 0.5017 (before: 0.5132; change: -0.0115)
- per-city accuracy: Seoul 0.5072 (before: 0.5006, +0.0066); Busan 0.4496 (before: 0.4669, -0.0173); Tokyo 0.5171 (before: 0.5233, -0.0062); Osaka 0.4309 (before: 0.4615, -0.0306); Taipei 0.6037 (before: 0.6139, -0.0102)
- what it means: Removing the museum-object photos reduced validation accuracy from 0.5132 to 0.5017.  I initially expected these photos to be less useful because they often showed isolated objects rather than recognizable city environments. However, some may still have contained useful cultural or visual clues, or resembled images in the validation set. Osaka had the largest drop, even though I did not remove any Osaka photos. When examining the mistakes, I noticed that most misclassified Osaka images were street scenes predicted as Tokyo. One possible explanation is that removing museum photos from Tokyo increased the relative importance of its remaining street photos during training. Since Tokyo and Osaka streets can look similar, this may have made the model more likely to classify Osaka streets as Tokyo. 

<04/11/2026> <lr_1e4> (Track A)

- changed: Changed the learning rate from `3e-4` to `1e-4` in both the AdamW optimizer and the OneCycleLR scheduler's `max_lr`. All other training settings, including the balanced recipe and selection, were kept unchanged.
- why: I wanted to test whether a lower learning rate would improve validation accuracy by making smaller updates to the pretrained ResNet18 weights.
- validation: 0.5068 (before: 0.5132; change: -0.0064)
- per-city accuracy: Seoul 0.5125 (before: 0.5006, +0.0119); Busan 0.4468 (before: 0.4669, -0.0201); Tokyo 0.5107 (before: 0.5233, -0.0126); Osaka 0.4652 (before: 0.4615, +0.0037); Taipei 0.5988 (before: 0.6139, -0.0151)
- what it means: I wanted to test whether a lower learning rate would help preserve the useful features learned during ImageNet pretraining, by making smaller adjustments to the model's weights. However, validation accuracy decreased from 0.5132 to 0.5068. Interestingly, Seoul improved slightly (+0.0119), while Busan (-0.0201), Tokyo (-0.0126), and Taipei (-0.0151) performed worse. Osaka remained almost unchanged (+0.0037). This suggests that the lower learning rate did not affect all cities in the same way, possibly because some cities require more adjustments to learn their distinctive visual features. Since the training budget was fixed at 249,984 photo presentations, I wonder if the smaller updates were not enough for the model to adapt to the specific visual differences between the five cities. It would be interesting to test a higher learning rate next. If it improves accuracy, this could suggest that the model benefits from larger weight updates within the limited training budget. However, a learning rate that is too high could also make training less stable.

<05/11/2026> <no_label_smoothing> (Track A)

- changed: Changed `label_smoothing` from `0.1` to `0.0` in the cross-entropy loss function while preserving the balanced recipe, learning rates, augmentations, and selection.
- why: I wanted to test whether removing label smoothing would improve validation accuracy by encouraging the model to make more confident predictions.
- validation: 0.5151 (before: 0.5132; change: +0.0019)
- per-city accuracy: Seoul 0.5368 (before: 0.5006, +0.0362); Busan 0.4662 (before: 0.4669, -0.0007); Tokyo 0.5125 (before: 0.5233, -0.0108); Osaka 0.4563 (before: 0.4615, -0.0052); Taipei 0.6037 (before: 0.6139, -0.0102)
- what it means: 

<05/11/20260> <Model_486_V3> (Track B)

<02/11/2026> <filter_military> (Track A)

<02/11/2026> <filter_indoors_seoul> (Track A)

<02/11/2026> <filter_indoors_osaka> (Track A)

<02/11/2026> <filter_indoors_taipei> (Track A)

<05/11/2026> <mobilev3_large_no_label_smoothing> (Track B)

- changed: Changed the architecture from the pretrained ResNet18 reference to pretrained MobileNetV3-Large. The 224×224 resolution, selected training photos, balanced sampling, augmentations, label smoothing `0.0`, AdamW optimizer, learning rate `3e-4`, weight decay, batch size, and approximately 249,984-image training budget were kept unchanged.
- why: I wanted to test whether a pretrained MobileNetV3-Large could improve on my best Track A configuration while keeping the training data and settings the same.
- validation: 0.5302 (before: 0.5151; change: +0.0151)
- per-city accuracy: Seoul 0.5220 (before: 0.5368, -0.0148); Busan 0.4777 (before: 0.4662, +0.0115); Tokyo 0.5669 (before: 0.5125, +0.0544); Osaka 0.4558 (before: 0.4563, -0.0005); Taipei 0.6286 (before: 0.6037, +0.0249)
- what it means: 

<31/10/2026> <balanced_crop_07_no_flip> (Track A)

<31/10/2026> <street_filter> (Track A) -- deleting some of the photos to test the consequences 

<31/10/2026> <jitter_01> (Track A)

<06/11/2026> <mobilev3_large_no_label_smoothing_384> (Track B)

- changed: Changed only the image resolution from 224x224 to 384x384. The pretrained MobileNetV3-Large architecture, selected training photos, balanced sampling, augmentations, label smoothing `0.0`, AdamW optimizer, learning rate `3e-4`, weight decay, batch size, scheduler, and 249,984-image training budget were kept unchanged.
- why: I wanted to test whether increasing the image resolution would improve the MobileNetV3-Large model while keeping the rest of the experiment identical.
- validation: 0.5663 (before: 0.5302; change: +0.0361)
- per-city accuracy: Seoul 0.5552 (before: 0.5220, +0.0332); Busan 0.4978 (before: 0.4777, +0.0201); Tokyo 0.6364 (before: 0.5669, +0.0695); Osaka 0.4920 (before: 0.4558, +0.0362); Taipei 0.6500 (before: 0.6286, +0.0214)
- what it means: 

