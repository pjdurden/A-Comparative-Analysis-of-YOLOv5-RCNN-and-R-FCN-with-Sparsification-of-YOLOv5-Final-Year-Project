# Copyright (c) 2021 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

from sparseml.pytorch.sparsification import EpochRangeModifier
from tests.sparseml.pytorch.helpers import (
    LinearNet,
    create_optim_adam,
    create_optim_sgd,
)
from tests.sparseml.pytorch.sparsification.test_modifier import ScheduledModifierTest


from tests.sparseml.pytorch.helpers import (  # noqa isort:skip
    test_epoch,
    test_loss,
    test_steps_per_epoch,
)


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_PYTORCH_TESTS", False),
    reason="Skipping pytorch tests",
)
@pytest.mark.parametrize(
    "modifier_lambda",
    [lambda: EpochRangeModifier(0.0, 10.0), lambda: EpochRangeModifier(5.0, 15.0)],
    scope="function",
)
@pytest.mark.parametrize("model_lambda", [LinearNet], scope="function")
@pytest.mark.parametrize(
    "optim_lambda",
    [create_optim_sgd, create_optim_adam],
    scope="function",
)
class TestEpochRangeModifierImpl(ScheduledModifierTest):
    pass


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_PYTORCH_TESTS", False),
    reason="Skipping pytorch tests",
)
def test_epoch_range_yaml():
    start_epoch = 5.0
    end_epoch = 15.0
    yaml_str = """
    !EpochRangeModifier
        start_epoch: {start_epoch}
        end_epoch: {end_epoch}
    """.format(
        start_epoch=start_epoch, end_epoch=end_epoch
    )
    yaml_modifier = EpochRangeModifier.load_obj(yaml_str)  # type: EpochRangeModifier
    serialized_modifier = EpochRangeModifier.load_obj(
        str(yaml_modifier)
    )  # type: EpochRangeModifier
    obj_modifier = EpochRangeModifier(start_epoch=start_epoch, end_epoch=end_epoch)

    assert isinstance(yaml_modifier, EpochRangeModifier)
    assert (
        yaml_modifier.start_epoch
        == serialized_modifier.start_epoch
        == obj_modifier.start_epoch
    )
    assert (
        yaml_modifier.end_epoch
        == serialized_modifier.end_epoch
        == obj_modifier.end_epoch
    )
