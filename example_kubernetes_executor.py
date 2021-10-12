#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distribuwith this work for additional information
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
"""
This is an example dag for using the Kubernetes Executor.
"""
import os

from airflow import DAG
from airflow.example_dags.libs.helper import print_stuff
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

from kubernetes.client import models as k8s

with DAG(
    dag_id='example_kubernetes_executor',
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example', 'example2'],
) as dag:

    affinity = {
        'podAntiAffinity': {
            'requiredDuringSchedulingIgnoredDuringExecution': [
                {
                    'topologyKey': 'kubernetes.io/hostname',
                    'labelSelector': {
                        'matchExpressions': [{'key': 'app', 'operator': 'In', 'values': ['airflow']}]
                    },
                }
            ]
        }
    }

    tolerations = [{'key': 'dedicated', 'operator': 'Equal', 'value': 'airflow'}]

    def assert_zip_binary():
        """
        Checks whether Zip is installed.

        :raises SystemError: if zip is not installed
        """
        return_code = os.system("zip")
        if return_code != 0:
            raise SystemError("The zip binary is not found")

    # You don't have to use any special KubernetesExecutor configuration if you don't want to
    start_task = PythonOperator(task_id="start_task", python_callable=print_stuff)

    # But you can if you want to
    one_task = PythonOperator(
        task_id="one_task",
        python_callable=print_stuff,
        executor_config={"KubernetesExecutor": {"image": "quay.io/inotaykrisztian/airflow:2.1.0-python3.8-2"}},
    )

    # Use the zip binary, which is only found in this special docker image
    two_task = PythonOperator(
        task_id="two_task",
        python_callable=assert_zip_binary,
        executor_config={"KubernetesExecutor": {"image": "quay.io/inotaykrisztian/airflow:2.1.0-python3.8-2"}},
    )

    # Limit resources on this operator/task with node affinity & tolerations
    three_task = PythonOperator(
        task_id="three_task",
        python_callable=print_stuff,
        executor_config={
            "pod_override": k8s.V1Pod(
                    spec=k8s.V1PodSpec(
                        containers=[
                            k8s.V1Container(
                                name="base",                                
                            )
                        ],
                        service_account_name="chriske"
                    )
                ),
        },
    )

    # Add arbitrary labels to worker pods
    four_task = PythonOperator(
        task_id="four_task",
        python_callable=print_stuff,
        executor_config={"KubernetesExecutor": {"labels": {"foo": "bar"}}},
    )

    start_task >> [one_task, two_task, three_task, four_task]
