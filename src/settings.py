from typing import Dict, List, Literal, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "HRSCD"
PROJECT_NAME_FULL: str = "HRSCD: High Resolution Semantic Change Detection"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_NC_SA_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Domain.Geospatial(),
    Industry.SearchAndRescue(is_used=False),
    Industry.Environmental(is_used=False),
]
CATEGORY: Category = Category.Aerial(extra=[Category.Environmental(), Category.Satellite()])

CV_TASKS: List[CVTask] = [CVTask.SemanticSegmentation()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.SemanticSegmentation()]

RELEASE_DATE: Optional[str] = "2019-08-28"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://rcdaudt.github.io/hrscd/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 16540212
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/semantic-change-detection"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = (
    "https://www.kaggle.com/datasets/javidtheimmortal/high-resolution-semantic-change-detection-dataset/download?datasetVersionNumber=1"
)

# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]] or Literal["predefined"]] = {
    "water": [230, 25, 75],
    "wetlands": [60, 180, 75],
    "forests": [255, 225, 25],
    "agricultural areas": [0, 130, 200],
    "artificial surfaces": [245, 130, 48],
    "no information": [145, 30, 180],
    "change": [70, 240, 240],
    "no change": [240, 50, 230],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
PAPER: Optional[Union[str, List[str]]] = "https://rcdaudt.github.io/files/2018cviu-hrscd.pdf"
BLOGPOST: Optional[Union[str, List[str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {
    "Kaggle": "https://www.kaggle.com/datasets/javidtheimmortal/high-resolution-semantic-change-detection-dataset"
}

CITATION_URL: Optional[str] = None
AUTHORS: Optional[List[str]] = [
    "Rodrigo Caye Daudt",
    "Bertrand Le Saux",
    "Alexandre Boulch",
    "Yann Gousseau",
]
AUTHORS_CONTACTS: Optional[List[str]] = [
    "rodrigo.cayedaudt@geod.baug.ethz.ch",
    "bertrand.le_saux@onera.fr",
    "alexandre.boulch@valeo.com",
    "yann.gousseau@telecom-paris.fr",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "Universite Paris-Saclay, France",
    "Telecom ParisTech, France",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://www.universite-paris-saclay.fr/",
    "https://www.telecom-paris.fr/",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with value:str to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = None
TAGS: Optional[
    List[
        Literal[
            "multi-view",
            "synthetic",
            "simulation",
            "multi-camera",
            "multi-modal",
            "multi-object-tracking",
            "keypoints",
            "egocentric",
        ]
    ]
] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
