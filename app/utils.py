from PIL import Image
from fastapi import UploadFile

def save_avatar(avatar: UploadFile, user_id: int) -> str:
    """
    save user avatar photo

    Args:
        avatar: uploaded image
        user_id: user id

    Returns:
        Url for image
    """

    # Check file type
    if not avatar.content_type.startswith("image/"):
        raise ValueError("Invalid image file")

    # generate file type
    filename = f"{user_id}_{avatar.filename}"

    # save file
    with open(f"uploads/avatars/{filename}", "wb") as f:
        f.write(avatar.file.read())

    # generate thumbnail
    thumb_filename = f"{filename}_thumb.png"
    with Image.open(f"uploads/avatars/{filename}") as img:
        img.thumbnail((128, 128))
        img.save(f"uploads/avatars/{thumb_filename}")

    # return url for avatar photo
    return f"/uploads/avatars/{filename}"
