def upload_product_image(instance, filename):
    return f"product/{instance.name}/{filename}"


def upload_producer_logo_image(instance, filename):
    return f"producer-logo/{instance.producer_name}/{filename}"


def upload_category_image(instance, filename):
    return f"category/{instance.name}/{filename}"
