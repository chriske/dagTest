#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


# pylint: disable=missing-docstring
def print_stuff():  # noqa: D103
    print("annotated!")

def getExecutorConfig(pod_template, configmap, pvc, sa_name):
    return {
            "pod_template_file": pod_template,
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env_from=[
                                k8s.V1EnvFromSource(
                                    config_map_ref=k8s.V1ConfigMapEnvSource(name=configmap)
                                )
                            ]
                        )
                    ],
                    volumes=[
                            k8s.V1Volume(name="dag-temp", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name=pvc)),
                    ],
                    service_account_name=sa_name
                )
            ),
        }
