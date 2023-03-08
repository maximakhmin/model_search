# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""blocks_builder module.

This module contains that class `Blocks`, which is a helper class to build any
`BlockType` defined in the enum 'BlockType` below.
"""

import enum

from model_search import block
from model_search import registry
from model_search.hparams import hyperparameters as ms_hparameters


enum_dict = registry.get_base_enum(block.Block)
enum_dict.update({'EMPTY_BLOCK': 0})

BlockType = enum.IntEnum('BlockType', enum_dict)  # pylint: disable=invalid-name


FLATTEN_TYPES = (
    BlockType.FLATTEN,
    BlockType.DOWNSAMPLE_FLATTEN,
    BlockType.PLATE_REDUCTION_FLATTEN,
)


_block_builders = dict()


class Blocks(object):
  """Blocks class to help creating the blocks."""

  def __init__(self):
    """Initializes (constructs) the `Blocks` class."""
    if not _block_builders:
      for block_type in BlockType:
        if block_type == BlockType.EMPTY_BLOCK:
          continue
        _block_builders.update(
            {block_type: registry.lookup(block_type.name, block.Block)})

  def __getitem__(self, block_type):
    return _block_builders[block_type]

  def get_new(self, block_type, override_name=None):
    return registry.lookup(
        block_type.name, block.Block, override_name=override_name)

  @staticmethod
  def search_space(blocks_to_use=None):
    """Returns required search space for all blocks."""
    search_space = ms_hparameters.Hyperparameters()
    for block_type in BlockType:
      if block_type == BlockType.EMPTY_BLOCK:
        continue
      if blocks_to_use is None or block_type.name in blocks_to_use:
        target = registry.lookup(block_type.name, block.Block)
        hps = target.requires_hparams()
        if hps:
          search_space.merge(hps, name_prefix=(block_type.name + '_'))

    return search_space
#branch2
