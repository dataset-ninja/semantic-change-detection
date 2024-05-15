import os
import shutil

import supervisely as sly
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,dir_exists 
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive
from PIL import Image
import numpy as np


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    dataset_path = "/home/alex/DATASETS/IMAGES/HRSCD"
    images_path_12 = "/home/alex/DATASETS/IMAGES/HRSCD/images_2012/2012"
    images_path_06 = "/home/alex/DATASETS/IMAGES/HRSCD/images_2006/2006"
    masks_path_12 = "/home/alex/DATASETS/IMAGES/HRSCD/labels_land_cover_2012/2012"
    masks_path_06 = "/home/alex/DATASETS/IMAGES/HRSCD/labels_land_cover_2006/2006"
    change_path = "/home/alex/DATASETS/IMAGES/HRSCD/labels_change/change"

    images_ext = ".tif"
    batch_size = 1
    ds_name = "ds"

    year_to_pathes = {"2006": (images_path_06, masks_path_06), "2012": (images_path_12, masks_path_12)}

    group_tag_name = "im_id"

    ext_2006 = "-0M50-E080.tif"
    # 35-2006-0305-6780-LA93.tif
    # 35-2012-0305-6780-LA93-0M50-E080.tif

    # 14-2005-0415-6890-LA93.tif
    # 14-2012-0415-6890-LA93-0M50-E080.tif


    def create_ann(image_path):
        labels = []

        id_data = get_file_name(image_path)[9:24]
        group_id = sly.Tag(group_tag_meta, value=id_data)

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        mask_name = get_file_name_with_ext(image_path)
        if year == "2006":
            if subfolder == "D14":
                mask_name = get_file_name(image_path).replace("2005", "2012") + ext_2006
            else:
                mask_name = get_file_name(image_path).replace("2006", "2012") + ext_2006

        mask_path = os.path.join(curr_masks_path, mask_name)

        if file_exists(mask_path):
            tif_data = Image.open(mask_path)
            mask_np = np.array(tif_data)
            unique_pixels = np.unique(mask_np)
            for curr_pixel in unique_pixels:
                obj_class = idx_to_class.get(int(curr_pixel))
                if obj_class is not None:
                    mask = mask_np == curr_pixel
                    curr_bitmap = sly.Bitmap(mask)
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        change_path = os.path.join(curr_change_path, get_file_name_with_ext(image_path))

        if file_exists(change_path):
            tif_data = Image.open(mask_path)
            mask_np = np.array(tif_data)
            unique_pixels = np.unique(mask_np)
            for curr_pixel in unique_pixels:
                obj_class = change_idx_to_class.get(int(curr_pixel))
                if obj_class is not None:
                    mask = mask_np == curr_pixel
                    curr_bitmap = sly.Bitmap(mask)
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[tag_year, tag_subf, group_id]
        )


    obj_class_no = sly.ObjClass("no information", sly.Bitmap)
    obj_class_surfaces = sly.ObjClass("artificial surfaces", sly.Bitmap)
    obj_class_areas = sly.ObjClass("agricultural areas", sly.Bitmap)
    obj_class_forests = sly.ObjClass("forests", sly.Bitmap)
    obj_class_wetlands = sly.ObjClass("wetlands", sly.Bitmap)
    obj_class_water = sly.ObjClass("water", sly.Bitmap)


    idx_to_class = {
        0: obj_class_no,
        1: obj_class_surfaces,
        2: obj_class_areas,
        3: obj_class_forests,
        4: obj_class_wetlands,
        5: obj_class_water,
    }

    obj_class_change = sly.ObjClass("change", sly.Bitmap)
    obj_class_no_change = sly.ObjClass("no change", sly.Bitmap)
    change_idx_to_class = {0: obj_class_no_change, 1: obj_class_change}

    # project_id = 3946

    # meta_json = api.project.get_meta(project_id)
    # meta = sly.ProjectMeta.from_json(meta_json)

    # already_in_ds_names = []


    subfolder_meta = sly.TagMeta(
        "subfolder", sly.TagValueType.ONEOF_STRING, possible_values=["D14", "D35"]
    )
    year_meta = sly.TagMeta("year", sly.TagValueType.ONEOF_STRING, possible_values=["2006", "2012"])
    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    meta = sly.ProjectMeta(
        obj_classes=list(idx_to_class.values()) + list(change_idx_to_class.values()),
        tag_metas=[subfolder_meta, year_meta, group_tag_meta],
    )

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)


    for subfolder in ["D14", "D35"]:

        curr_change_path = os.path.join(change_path, subfolder)

        tag_subf = sly.Tag(subfolder_meta, value=subfolder)

        # dataset_id = 6978

        # ds_info = api.image.get_list(dataset_id)
        # for curr_ds_info in ds_info:
        #     already_in_ds_names.append(get_file_name(curr_ds_info.name))

        for year in ["2012", "2006"]:

            tag_year = sly.Tag(year_meta, value=year)

            images_path, masks_path = year_to_pathes[year]

            curr_images_path = os.path.join(images_path, subfolder)
            curr_masks_path = os.path.join(masks_path, subfolder)
            if dir_exists(curr_images_path):
                images_names = os.listdir(curr_images_path)

                progress = sly.Progress("Create dataset {}".format(subfolder), len(images_names))

                for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                    print(images_names_batch)
                    images_pathes_batch = [
                        os.path.join(curr_images_path, im_name) for im_name in images_names_batch
                    ]

                    img_infos = api.image.upload_paths(
                        dataset.id, images_names_batch, images_pathes_batch
                    )
                    img_ids = [im_info.id for im_info in img_infos]

                    anns = [create_ann(image_path) for image_path in images_pathes_batch]
                    api.annotation.upload_anns(img_ids, anns)

                    progress.iters_done_report(len(images_names_batch))

    return project
