// Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#include <string>

#include "paddle/phi/core/compat/op_utils.h"
#include "paddle/utils/small_vector.h"

namespace phi {

KernelSignature AdamaxOpArgumentMapping(const ArgumentMappingContext& ctx) {
  paddle::small_vector<const char*> in_names = {"Param",
                                                "Grad",
                                                "LearningRate",
                                                "Moment",
                                                "InfNorm",
                                                "Beta1Pow",
                                                "MasterParam"};
  paddle::small_vector<const char*> out_names = {
      "ParamOut", "MomentOut", "InfNormOut", "MasterParamOut"};
  paddle::small_vector<const char*> attr_names;
  attr_names.emplace_back("beta1");
  attr_names.emplace_back("beta2");
  attr_names.emplace_back("epsilon");
  attr_names.emplace_back("multi_precision");

  if (ctx.IsDenseTensorInput("Grad")) {
    return KernelSignature("adamax",
                           std::move(in_names),
                           std::move(attr_names),
                           std::move(out_names));
  } else {
    return KernelSignature("unregistered", {}, {}, {});
  }
}

}  // namespace phi

PD_REGISTER_ARG_MAPPING_FN(adamax, phi::AdamaxOpArgumentMapping);
