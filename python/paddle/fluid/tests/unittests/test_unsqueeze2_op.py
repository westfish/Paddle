# Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
from op_test import OpTest

import paddle
import paddle.fluid as fluid

paddle.enable_static()


# Correct: General.
class TestUnsqueezeOp(OpTest):
    def setUp(self):
        self.init_test_case()
        self.op_type = "unsqueeze2"
        self.python_api = paddle.unsqueeze
        self.python_out_sig = ["Out"]
        self.inputs = {"X": np.random.random(self.ori_shape).astype("float64")}
        self.init_attrs()
        self.outputs = {
            "Out": self.inputs["X"].reshape(self.new_shape),
            "XShape": np.random.random(self.ori_shape).astype("float64"),
        }
        self.prim_op_type = "comp"

    def test_check_output(self):
        self.check_output(
            no_check_set=["XShape"], check_eager=True, check_prim=True
        )

    def test_check_grad(self):
        self.check_grad(["X"], "Out", check_eager=True)

    def init_test_case(self):
        self.ori_shape = (3, 40)
        self.axes = (1, 2)
        self.new_shape = (3, 1, 1, 40)

    def init_attrs(self):
        self.attrs = {"axes": self.axes}


# Correct: Single input index.
class TestUnsqueezeOp1(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (-1,)
        self.new_shape = (20, 5, 1)


# Correct: Mixed input axis.
class TestUnsqueezeOp2(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (0, -1)
        self.new_shape = (1, 20, 5, 1)


# Correct: There is duplicated axis.
class TestUnsqueezeOp3(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = (10, 2, 5)
        self.axes = (0, 3, 3)
        self.new_shape = (1, 10, 2, 1, 1, 5)


# Correct: Reversed axes.
class TestUnsqueezeOp4(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = (10, 2, 5)
        self.axes = (3, 1, 1)
        self.new_shape = (10, 1, 1, 2, 5, 1)


class TestUnsqueezeOp_ZeroDim1(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = ()
        self.axes = (-1,)
        self.new_shape = 1
        self.enable_cinn = False


class TestUnsqueezeOp_ZeroDim2(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = ()
        self.axes = (-1, 1)
        self.new_shape = (1, 1)
        self.enable_cinn = False


class TestUnsqueezeOp_ZeroDim3(TestUnsqueezeOp):
    def init_test_case(self):
        self.ori_shape = ()
        self.axes = (0, 1, 2)
        self.new_shape = (1, 1, 1)
        self.enable_cinn = False


# axes is a list(with tensor)
class TestUnsqueezeOp_AxesTensorList(OpTest):
    def setUp(self):
        self.init_test_case()
        self.op_type = "unsqueeze2"
        self.python_out_sig = ["Out"]
        self.python_api = paddle.unsqueeze

        axes_tensor_list = []
        for index, ele in enumerate(self.axes):
            axes_tensor_list.append(
                ("axes" + str(index), np.ones((1)).astype('int32') * ele)
            )

        self.inputs = {
            "X": np.random.random(self.ori_shape).astype("float64"),
            "AxesTensorList": axes_tensor_list,
        }
        self.init_attrs()
        self.outputs = {
            "Out": self.inputs["X"].reshape(self.new_shape),
            "XShape": np.random.random(self.ori_shape).astype("float64"),
        }

    def test_check_output(self):
        self.check_output(no_check_set=["XShape"], check_eager=True)

    def test_check_grad(self):
        self.check_grad(["X"], "Out", check_eager=True)

    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (1, 2)
        self.new_shape = (20, 1, 1, 5)

    def init_attrs(self):
        self.attrs = {}


class TestUnsqueezeOp1_AxesTensorList(TestUnsqueezeOp_AxesTensorList):
    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (-1,)
        self.new_shape = (20, 5, 1)


class TestUnsqueezeOp2_AxesTensorList(TestUnsqueezeOp_AxesTensorList):
    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (0, -1)
        self.new_shape = (1, 20, 5, 1)


class TestUnsqueezeOp3_AxesTensorList(TestUnsqueezeOp_AxesTensorList):
    def init_test_case(self):
        self.ori_shape = (10, 2, 5)
        self.axes = (0, 3, 3)
        self.new_shape = (1, 10, 2, 1, 1, 5)


class TestUnsqueezeOp4_AxesTensorList(TestUnsqueezeOp_AxesTensorList):
    def init_test_case(self):
        self.ori_shape = (10, 2, 5)
        self.axes = (3, 1, 1)
        self.new_shape = (10, 1, 1, 2, 5, 1)


# axes is a Tensor
class TestUnsqueezeOp_AxesTensor(OpTest):
    def setUp(self):
        self.init_test_case()
        self.op_type = "unsqueeze2"
        self.python_out_sig = ["Out"]
        self.python_api = paddle.unsqueeze

        self.inputs = {
            "X": np.random.random(self.ori_shape).astype("float64"),
            "AxesTensor": np.array(self.axes).astype("int32"),
        }
        self.init_attrs()
        self.outputs = {
            "Out": self.inputs["X"].reshape(self.new_shape),
            "XShape": np.random.random(self.ori_shape).astype("float64"),
        }

    def test_check_output(self):
        self.check_output(no_check_set=["XShape"], check_eager=True)

    def test_check_grad(self):
        self.check_grad(["X"], "Out", check_eager=True)

    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (1, 2)
        self.new_shape = (20, 1, 1, 5)

    def init_attrs(self):
        self.attrs = {}


class TestUnsqueezeOp1_AxesTensor(TestUnsqueezeOp_AxesTensor):
    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (-1,)
        self.new_shape = (20, 5, 1)


class TestUnsqueezeOp2_AxesTensor(TestUnsqueezeOp_AxesTensor):
    def init_test_case(self):
        self.ori_shape = (20, 5)
        self.axes = (0, -1)
        self.new_shape = (1, 20, 5, 1)


class TestUnsqueezeOp3_AxesTensor(TestUnsqueezeOp_AxesTensor):
    def init_test_case(self):
        self.ori_shape = (10, 2, 5)
        self.axes = (0, 3, 3)
        self.new_shape = (1, 10, 2, 1, 1, 5)


class TestUnsqueezeOp4_AxesTensor(TestUnsqueezeOp_AxesTensor):
    def init_test_case(self):
        self.ori_shape = (10, 2, 5)
        self.axes = (3, 1, 1)
        self.new_shape = (10, 1, 1, 2, 5, 1)


# test api
class TestUnsqueezeAPI(unittest.TestCase):
    def setUp(self):
        self.executed_api()

    def executed_api(self):
        self.unsqueeze = paddle.unsqueeze

    def test_api(self):
        input = np.random.random([3, 2, 5]).astype("float64")
        x = paddle.static.data(name='x', shape=[3, 2, 5], dtype="float64")
        positive_3_int32 = fluid.layers.fill_constant([1], "int32", 3)
        positive_1_int64 = fluid.layers.fill_constant([1], "int64", 1)
        axes_tensor_int32 = paddle.static.data(
            name='axes_tensor_int32', shape=[3], dtype="int32"
        )
        axes_tensor_int64 = paddle.static.data(
            name='axes_tensor_int64', shape=[3], dtype="int64"
        )

        out_1 = self.unsqueeze(x, axis=[3, 1, 1])
        out_2 = self.unsqueeze(x, axis=[positive_3_int32, positive_1_int64, 1])
        out_3 = self.unsqueeze(x, axis=axes_tensor_int32)
        out_4 = self.unsqueeze(x, axis=3)
        out_5 = self.unsqueeze(x, axis=axes_tensor_int64)

        exe = paddle.static.Executor(place=paddle.CPUPlace())
        res_1, res_2, res_3, res_4, res_5 = exe.run(
            paddle.static.default_main_program(),
            feed={
                "x": input,
                "axes_tensor_int32": np.array([3, 1, 1]).astype("int32"),
                "axes_tensor_int64": np.array([3, 1, 1]).astype("int64"),
            },
            fetch_list=[out_1, out_2, out_3, out_4, out_5],
        )

        assert np.array_equal(res_1, input.reshape([3, 1, 1, 2, 5, 1]))
        assert np.array_equal(res_2, input.reshape([3, 1, 1, 2, 5, 1]))
        assert np.array_equal(res_3, input.reshape([3, 1, 1, 2, 5, 1]))
        assert np.array_equal(res_4, input.reshape([3, 2, 5, 1]))
        assert np.array_equal(res_5, input.reshape([3, 1, 1, 2, 5, 1]))

    def test_error(self):
        def test_axes_type():
            x2 = paddle.static.data(name="x2", shape=[2, 25], dtype="int32")
            self.unsqueeze(x2, axis=2.1)

        self.assertRaises(TypeError, test_axes_type)


class TestUnsqueezeInplaceAPI(TestUnsqueezeAPI):
    def executed_api(self):
        self.unsqueeze = paddle.unsqueeze_


class TestUnsqueezeAPI_ZeroDim(unittest.TestCase):
    def test_dygraph(self):
        paddle.disable_static()

        x = paddle.rand([])
        x.stop_gradient = False

        out = paddle.unsqueeze(x, [-1])
        out.retain_grads()
        out.backward()
        self.assertEqual(out.shape, [1])
        self.assertEqual(x.grad.shape, [])
        self.assertEqual(out.grad.shape, [1])

        out = paddle.unsqueeze(x, [-1, 1])
        out.retain_grads()
        out.backward()
        self.assertEqual(out.shape, [1, 1])
        self.assertEqual(x.grad.shape, [])
        self.assertEqual(out.grad.shape, [1, 1])

        out = paddle.unsqueeze(x, [0, 1, 2])
        out.retain_grads()
        out.backward()
        self.assertEqual(out.shape, [1, 1, 1])
        self.assertEqual(x.grad.shape, [])
        self.assertEqual(out.grad.shape, [1, 1, 1])

        paddle.enable_static()


if __name__ == "__main__":
    unittest.main()
