The **High Resolution Semantic Change Detection** (HRSCD) dataset was introduced to the scientific community as a benchmark for evaluating semantic change detection algorithms. Its aim is to facilitate the application of cutting-edge deep learning techniques in this domain. In addition to pinpointing areas of change, the dataset also provides detailed semantic information about the terrain depicted in all its images.

## Motivation

Remote sensing serves a critical role in monitoring land evolution through satellite and aerial imaging. This technology allows researchers to track changes worldwide, from densely populated regions to remote and inaccessible areas. Consequently, change detection has become a focal point in remote sensing studies. It involves identifying alterations on the Earth's surface by comparing multiple registered images, which can result from various factors such as natural disasters, urbanization, or deforestation.

The quest for precise change detection stems from the importance of surveying extensive land areas and analyzing their transformations over time. Manual detection of changes is painstakingly slow, prompting decades-long research into automated methods using image pairs or sequences. Over the years, advancements in computer vision and image processing have greatly influenced change detection techniques. Recent breakthroughs in machine learning have particularly revolutionized image understanding tasks.

This surge in machine learning owes its momentum to several factors. Firstly, the affordability and increased power of hardware facilitate the extensive computational requirements of machine learning algorithms. Secondly, novel methodologies are continually emerging to leverage data in innovative ways. Lastly, the expanding availability of data is indispensable for training and deploying machine learning models effectively.

## Dataset description

The dataset comprises 291 RGB image pairs, each measuring 10,000 by 10,000 pixels. These composite images are constructed from aerial photographs captured by the French National Institute of Geographical and Forest Information (IGN). Specifically, they originate from the BD ORTHO database, which archives orthorectified aerial images spanning various years and regions of France, each with a resolution of 50 centimeters per pixel.

Each image pair consists of one snapshot taken either in 2005 or 2006 and another acquired in 2012. These images capture diverse landscapes encompassing both urban and rural areas surrounding the French cities of Rennes and Caen. Additionally, the dataset provides detailed labels disclosing the types of changes observed and the land cover characteristics depicted in the images.

The dataset's labels are sourced from the European Environment Agency’s (EEA) Copernicus Land Monitoring initiative, which furnishes "accurate, comparable, high-resolution land use maps" for functional urban areas across Europe hosting over 50,000 residents. These meticulously crafted maps depict land use dynamics for the years 2006 and 2012, with an additional map detailing changes occurring within that timeframe.

These land cover maps are categorized into various semantic classes, organized across different hierarchical levels. By aggregating labels at varying hierarchical tiers, it becomes feasible to generate maps with varying levels of granularity. For instance, condensing labels at the broadest hierarchical level produces five classes (alongside a "no information" category). These maps are openly accessible in vector format online.

To align the vector maps with the BD ORTHO images, the authors have translated them into raster format. This alignment ensures that each pixel in the dataset is accurately annotated with ground truth information. It's noteworthy that there are subtle discrepancies between the semantic classes featured in Urban Atlas 2006 and those in Urban Atlas 2012.

<img src="https://github.com/dataset-ninja/hrscd/assets/120389559/1d1e7675-a16a-4959-87f9-09376a81dceb" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Examples of image pairs, land cover maps (LCM) and associated pixel-wise change maps from the HRSCD dataset. In the depicted LCMs, blue represents the ”artificial surfaces” class, and orange represents the ”agricultural areas” class.</span>

In this section, the authors candidly address the limitations and hurdles inherent in the dataset, despite its remarkable scale and attributes. Nonetheless, they emphasize that despite these constraints, the dataset serves as a catalyst for pushing the boundaries of state-of-the-art semantic change detection through machine learning.

One notable issue pertains to the precision of the labels within the Urban Atlas vector maps concerning the BD ORTHO images. The authors lack access to the original images used to construct the Urban Atlas vector maps, as well as their acquisition dates. Consequently, discrepancies arise between the information depicted in the vector maps and the BD ORTHO images. Moreover, the European Environment Agency (EEA) only guarantees a minimum label accuracy ranging from 80% to 85%, contingent on the specific class considered. While the majority of the available data is accurate, it's crucial to acknowledge that the labels within the dataset are not devoid of imperfections. It is also worth noting that the labels have been created using previously known vector maps, mostly by labelling correctly each of the known regions. This means a single label was given to each region, and this led to inaccurate borders in some cases.

<img src="https://github.com/dataset-ninja/hrscd/assets/120389559/98c0eeff-ef5c-451a-9aee-5af2023563df" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Examples of: ((a)-\(c\)) overly large change markings, ((d)-(f)) failure to mark changes, ((g)-(i)) false positive.</span>

A significant challenge associated with utilizing this dataset for supervised learning lies in its pronounced label imbalance. Remarkably, 99.232% of all pixels are designated as "no change," with the largest class transition being from agricultural areas to artificial surfaces (i.e., from class 2 to class 1), representing a mere 0.653% of all pixels. Together, these two classes encompass 99.885% of all pixels, leaving a scant 0.115% for all other types of changes combined. Moreover, several potential change types lack any examples across the dataset's images.

Addressing this imbalance is crucial when working with this dataset. Furthermore, employing overall accuracy as a performance metric is ill-advised, as it predominantly reflects the correct classification of "no change" pixels. Instead, metrics such as Cohen’s kappa coefficient or the Sørensen-Dice coefficient should be favored. This class imbalance mirrors real-world scenarios, where changes occur infrequently compared to unchanged surfaces. Consequently, this dataset offers a pragmatic evaluation tool for assessing change detection methods, contrasting with meticulously curated image pairs featuring extensive changed regions.
