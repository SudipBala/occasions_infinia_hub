from libs.utils import create_thumbnail_from_image


def create_thumbnail(sender, instance=None, **kwargs):
    if instance.image:
        try:
            thumbnailFile = create_thumbnail_from_image(instance.image, 400)
            instance.thumbnail = thumbnailFile.name
        except:
            instance.thumbnail = 'NA.png.120x120_q85_crop.jpg'
