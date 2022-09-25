import os

import pytest
from PIL import Image

from src.ImageServer.ImageProcessor.image_processor import ImageProcessor


@pytest.mark.asyncio
async def test_image_processor(image_processor: ImageProcessor):
    now_path = os.path.join(os.getcwd(), "tests", "test_image_server", "test_image_processor")
    data_path = os.path.join(now_path, "test_data", "data1.png")
    image = Image.open(data_path)

    result = await image_processor.infer(image)
    assert result.to_array() == ["1", "1", "1", "1"]
