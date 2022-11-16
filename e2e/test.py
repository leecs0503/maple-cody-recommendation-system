from src.AvatarServer.server.config import Config
from src.AvatarServer.AvatarProcessor.avatar_processor import AvatarProcessor
import logging
import os
import asyncio
from aiohttp import web
from PIL import Image, ImageChops


def main():
    config = Config(
        wcr_server_host="localhost",
        wcr_server_port=7209,
        wcr_server_protocol="https",
        base_wz_code_path="./data/base_wz.json",
        wcr_caller_backoff=1,
        wcr_caller_retry_num=-1,
        wcr_caller_timeout=2.5,
    )
    avatar_processor = AvatarProcessor(
        logger=logging.getLogger(__file__),
        config=config,
    )
    packed_character_info = avatar_processor.infer("LBDGMFNKHKPCFEIKMLCAECJDBELMLLADNFHDAJPIHJAJBKFCLMKKLDLDFNPBOGEAODPEMPCBIPCCGBIOFPCCKGIKKDLILAOACAHHIKACLAKLKKNPFILHBLIPKKMHGAFEADKBHCIPDBJHOKFGCGFHFAKMOHCDBPJKPHNGBGCLMOLDJHHFFEBKEJFNKBJMEJNFPLDEOLKCALAGNADDIDPACEPGMLMCBHHAGKOFFPKKNHKJOJPELKPFKODNDFPBHCBF")  # noqa: E501
    avatar = packed_character_info.get_avatar()

    avatar.shield = "0"

    loop = asyncio.get_event_loop()
    try:
        image = loop.run_until_complete(
            avatar_processor.process_image(avatar)
        )
        image.save(os.path.join("e2e", "test.png"))
        assert ImageChops.difference(image, Image.open(os.path.join("e2e", "test.png"))).getbbox() is None
    except web.HTTPBadRequest as e:
        print(e.text)


if __name__ == "__main__":
    main()
