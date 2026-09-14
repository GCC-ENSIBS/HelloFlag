import hashlib
import logging
import os
from base64 import b64decode
from datetime import datetime

from tornado.options import options

from libs.ValidationError import ValidationError
from libs.XSSImageCheck import image_format, is_xss_image

# shipped fallbacks used when the admin has not uploaded an image of their own
DEFAULT_IMAGES = {
    "game_icon": "/static/images/icon.png",
    "home_background": "/static/images/home-background.png",
}


def config_image(name):
    """Return the uploaded image for a config option, or the shipped default"""
    configured = options[name]
    if configured:
        return configured
    default = DEFAULT_IMAGES.get(name, "")
    if default and os.path.isfile(default.lstrip("/")):
        return default
    return ""


def save_config():
    logging.info("Saving current config to: %s" % options.config)
    with open(options.config, "w") as fp:
        fp.write("##########################")
        fp.write(" Root the Box Config File ")
        fp.write("##########################\n")
        fp.write(
            "# Documentation: %s\n"
            % "https://github.com/moloch--/RootTheBox/wiki/Configuration-File-Details"
        )
        fp.write("# Last updated: %s\n" % datetime.now())
        for group in options.groups():
            # Shitty work around for Tornado 4.1
            if "rootthebox.py" in group.lower() or group == "":
                continue
            fp.write("\n# [ %s ]\n" % group.title())
            opt = list(options.group_dict(group).items())
            for key, value in opt:
                if isinstance(value, str):
                    # Str/Unicode needs to have quotes
                    fp.write('%s = "%s"\n' % (key, value))
                else:
                    # Int/Bool/List use __str__
                    fp.write("%s = %s\n" % (key, value))


def save_config_image(b64_data):
    image_data = bytearray(b64decode(b64_data))
    if len(image_data) < (2048 * 2048):
        ext = image_format(image_data)
        file_name = "/story/%s.%s" % (hashlib.sha1(image_data).hexdigest(), ext)
        if ext in ["png", "jpeg", "gif", "bmp"] and not is_xss_image(image_data):
            with open("files" + file_name, "wb") as fp:
                fp.write(image_data)
            return file_name
        else:
            raise ValidationError(
                "Invalid image format, avatar must be: .png .jpeg .gif or .bmp"
            )
    else:
        raise ValidationError("The image is too large")


def save_config_upload(upload):
    """Store an uploaded configuration image and return its public path"""
    image_data = bytearray(upload["body"])
    if len(image_data) > (2048 * 2048):
        raise ValidationError("The image is too large")
    ext = image_format(image_data)
    if ext not in ["png", "jpeg", "gif", "bmp"] or is_xss_image(image_data):
        raise ValidationError(
            "Invalid image format, image must be: .png .jpeg .gif or .bmp"
        )
    file_name = "/story/%s.%s" % (hashlib.sha1(image_data).hexdigest(), ext)
    with open("files" + file_name, "wb") as fp:
        fp.write(image_data)
    return file_name


def remove_config_image(path):
    """Delete an uploaded configuration image once it is no longer referenced"""
    if not path or not path.startswith("/story/"):
        return
    file_path = os.path.join("files", path.lstrip("/"))
    try:
        os.remove(file_path)
    except OSError:
        logging.info("Could not remove the previous config image: %s" % file_path)


def create_demo_user():
    from models import dbsession
    from models.GameLevel import GameLevel
    from models.Team import Team
    from models.User import User

    if Team.by_name("player") is None:
        user = User()
        user.handle = "player"
        user.password = "rootthebox"
        user.name = "player"
        user.email = "player@rootthebox.com"
        team = Team()
        team.name = "player"
        team.motto = "Don't hate the player"
        team.set_score("start", 0)
        team.game_levels.append(GameLevel.all()[0])
        team.members.append(user)
        dbsession.add(user)
        dbsession.add(team)
        dbsession.commit()
