import logging
import random
import os
import numpy as np
from heapq import heappush, heappop
from ..server.config import Config
from ..Avatar.avatar import Avatar
from .WCR_caller import WCRCaller
from PIL import Image
from typing import List, Tuple, Optional
from multimethod import multimethod
import base64
import io


def is_pixel_eq(
	a: Tuple[int, int, int, int],
	b: Tuple[int, int, int, int],
):
	return  abs(a[0] - b[0]) < 8 and \
			abs(a[1] - b[1]) < 8 and \
			abs(a[2] - b[2]) < 8 and \
			abs(a[3] - b[3]) < 8


class ImageProcessor:
	def __init__(
		self,
		logger: logging.Logger,
		config: Config,
	):
		self.logger = logger
		self.caller = WCRCaller(
			logger=self.logger,
			wcr_server_host=config.wcr_server_host,
			wcr_server_protocol=config.wcr_server_protocol,
			wcr_server_port=config.wcr_server_port,
			retry_num=config.wcr_caller_retry_num,
			timeout=config.wcr_caller_timeout,
			backoff=config.wcr_caller_backoff,
		)
		self.item_code_list = []

	async def _naive_approach(
		item_coord,
	):
		# TODO:
		"""
		SAMPLE_SIZE = 500
		AVATAR_COORD_RATIO = 1

		sample_pix_coord = random.sample(item_coord, min(len(item_coord), SAMPLE_SIZE))

		prob_compare = []
		for rows in sample_row_coord:
			cnt = 0
			for cols in sample_col_coord:
				cnt = 0
				for compare_rows, compare_cols in sample_pix_coord:
					av_rgba = image_avatar.getpixel((rows + compare_rows, cols + compare_cols))
					item_rgba = image_item.getpixel((compare_rows, compare_cols))
					if (
						(av_rgba[0] == item_rgba[0])
						and (av_rgba[1] == item_rgba[1])
						and (av_rgba[2] == item_rgba[2])
					):
						cnt += 1
				else:
					prob = cnt / len(sample_pix_coord)
					prob_compare.append(prob)
		else:
			maximum = max(prob_compare)
			print("accuracy : ", maximum)
		return maximum
		"""

	def _correct_visualize(self, base_image: Image.Image, test_image: Image.Image):
		base_uri = os.path.dirname(__file__)

		acc, px, py = self.is_contain(base_image, test_image)
		test_format = base_image.copy()
		(h, w) = test_image.size
		pixels = test_format.load()
		for x in range(h):
			for y in range(w):
				ax, ay = (px + x, py + y)
				pa = base_image.getpixel((ax, ay))
				ta = test_image.getpixel((x, y))
				if not is_pixel_eq(pa, ta):
					# pixels[ax, ay] = (255 - pixels[ax, ay][0] , 255 - pixels[ax, ay][1], 255 - pixels[ax, ay][2], pixels[ax, ay][3])
					pixels[ax, ay] = (100, 100, 100, pixels[ax, ay][3])

		visualize_path = os.path.join(base_uri, "correct_visualize", "visualize.png")

		test_format.save(visualize_path)
		print(f"original - made acc: {acc}")
		return acc

	def _get_pixel_list(
		self,
		pixel_data: List[Tuple[int, int, int, int]],
		height: int,
		width: int,
	):
		item_coord = [(idx % height, idx // height, pixel) for idx, pixel in enumerate(pixel_data) if pixel[3] != 0]
		num_item_pixel = len(item_coord)
		if num_item_pixel < 2:
			return []

		assert num_item_pixel > 0
		return item_coord

	def _get_ratio(
		self,
		pivot_row: int,
		pivot_col: int,
		avatar_pixel_data: List[Tuple[int, int, int, int]],
		avatar_height: int,
		avatar_width: int,
		xy_list: List[Tuple[int, int, Tuple[int, int, int, int]]],
	):
		correct_count = 0
		for dx, dy, item_pixel in xy_list:
			x = pivot_row + dx
			y = pivot_col + dy
			if x >= avatar_height or y >= avatar_width:
				continue
			avatar_pixel = avatar_pixel_data[y * avatar_height + x]
			if is_pixel_eq(avatar_pixel, item_pixel):
				correct_count += 1
			
		ratio = correct_count / len(xy_list)
		return ratio

	@multimethod
	def is_contain(
		self,
		avatar_pixel_data: List[Tuple[int, int, int, int]],
		avatar_height: int,
		avatar_width: int,
		item_pixel_data: List[Tuple[int, int, int, int]],
		item_height: int,
		item_width: int,
	) -> Tuple[int, int, int]:
		SAMPLE_SIZE = 10
		VALIDATE_SAMPLE_NUM = 3

		all_item_pixel_xy_list = self._get_pixel_list(item_pixel_data, item_height, item_width)

		if len(all_item_pixel_xy_list) == 0:
			return (0, 0, 0)

		sample_idx = random.sample(range(len(all_item_pixel_xy_list)), min(SAMPLE_SIZE, len(all_item_pixel_xy_list)))
		sample_item_pixel_xy_list = [all_item_pixel_xy_list[i] for i in sorted(sample_idx)]


		data = []
		for pivot_col in range(avatar_width):
			for pivot_row in range(avatar_height):
				ratio = self._get_ratio(
					pivot_row=pivot_row,
					pivot_col=pivot_col,
					avatar_pixel_data=avatar_pixel_data,
					avatar_height=avatar_height,
					avatar_width=avatar_width,
					xy_list=sample_item_pixel_xy_list,
				)
				heappush(data, (ratio, pivot_row, pivot_col))
				if len(data) > VALIDATE_SAMPLE_NUM:
					heappop(data)

		result = (0, 0, 0)
		for ratio, pivot_row, pivot_col in data:
			correct_ratio = self._get_ratio(
				pivot_row=pivot_row,
				pivot_col=pivot_col,
				avatar_pixel_data=avatar_pixel_data,
				avatar_height=avatar_height,
				avatar_width=avatar_width,
				xy_list=all_item_pixel_xy_list,
			)
			result = max(result, (correct_ratio, pivot_row, pivot_col))
		return result

	@multimethod
	def is_contain(
		self,
		avatar_image: Image.Image,
		item_image: Image.Image,
	) -> Tuple[int, int, int]:
		"""
		image_avatar:
		image_item:
		"""
		[item_height, item_width] = item_image.size
		[avatar_height, avatar_width] = avatar_image.size

		avatar_pixel_data = list(avatar_image.getdata())
		item_pixel_data = list(item_image.getdata())

		return self.is_contain(
			avatar_pixel_data,
			avatar_height,
			avatar_width,
			item_pixel_data,
			item_height,
			item_width,
		)

	async def infer_sub(self, image: Image.Image, avatar: Avatar, code: str) -> Tuple[Tuple[int, int, int], int]:

		wcr_response = await self.caller.get_image(avatar=avatar)
		if wcr_response is None:
			return ((0, 0, 0), 0)

		image_data = base64.b64decode(wcr_response)
		item_image = Image.open(io.BytesIO(image_data))
		acc = self.is_contain(avatar_image=image, item_image=item_image), code
		return acc

	async def max_acc_code(self, acc_list: List[Tuple[Tuple[int, int, int], int]]) -> int:
		max_acc = 0
		for acc in acc_list:
			if acc[0][0] >= max_acc:
				max_acc = acc[0][0]
				max_idx_acc = acc[1]
		return max_idx_acc

	async def infer(self, image: Image, item_list: Optional[List[Tuple[int, str]]] = None) -> Avatar:
		# TODO: implement

		avatar = Avatar()

		if item_list is not None:
			acc_lists = [[] for _ in range(4)]
			for idx, code in item_list:
				avatar.add_parts(idx, code)
				acc = await self.infer_sub(image=image, avatar=avatar, code=code)
				acc_lists[idx].append(acc)
				avatar.reset()
			for idx, acc_list in enumerate(acc_lists):
				max_acc = await self.max_acc_code(acc_list)
				avatar.add_parts(idx, max_acc)
			return avatar

		# TODO: 모든코드
