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
from libs.helper import print_stuff2
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from kubernetes import client, config

from airflow.utils.email import send_email_smtp

def new_email_alert(self, **kwargs):
    title = "TEST MESSAGE: THIS IS A MODIFIED TEST"    
    body = ("This is the text "
    "That appears in the email body..<br>")      
    send_email_smtp('krisztian.inotay@ext.otpbank.hu', title, body)

args = {
    'owner': 'TulajdonosCsoport',
    'email': ['krisztian.inotay@ext.otpbank.hu'],
    'retries': 1,
    'email_on_failure': True,
    'email_on_retry': True,
    #'on_success_callback': new_email_alert,
}

from kubernetes.client import models as k8s

with DAG(
    dag_id='00-demo-DAG',
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['demo', 'demo-dag'],

) as dag:
        
    def readSecret():
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        secret = v1.read_namespaced_secret("super-secret", "airflow")
        print(secret.data['super-secret'])

    
    start_task = PythonOperator(
        task_id="start_task",
        python_callable=print_stuff2,
        executor_config={
            "pod_template_file": "/opt/airflow/pod_template/pod_template_default.yaml",
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env_from=[
                                k8s.V1EnvFromSource(
                                    config_map_ref=k8s.V1ConfigMapEnvSource(name="demo-log-config-demo00")
                                )
                            ]
                        )
                    ],
                    volumes=[
                            k8s.V1Volume(name="dag-temp", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="dag-temp")),
                    ],
                    service_account_name="dag-test-runner"
                )
            ),
        },
    )

    
    one_task = PythonOperator(
        task_id="one_task",
        python_callable=print_stuff2,
        executor_config={
            "pod_template_file": "/opt/airflow/pod_template/pod_template_default.yaml",
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env_from=[
                                k8s.V1EnvFromSource(
                                    config_map_ref=k8s.V1ConfigMapEnvSource(name="demo-log-config-demo00")
                                )
                            ]
                        )
                    ],
                    volumes=[
                            k8s.V1Volume(name="dag-temp", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="dag-temp")),
                    ],
                    service_account_name="dag-test-runner"
                )
            ),
        },
    )

   
    two_task = PythonOperator(
        task_id="two_task",
        python_callable=print_stuff2,
        executor_config={
            "pod_template_file": "/opt/airflow/pod_template/pod_template_default.yaml",
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env_from=[
                                k8s.V1EnvFromSource(
                                    config_map_ref=k8s.V1ConfigMapEnvSource(name="demo-log-config-demo00")
                                )
                            ]
                        )
                    ],
                    volumes=[
                            k8s.V1Volume(name="dag-temp", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="dag-temp")),
                    ],
                    service_account_name="dag-test-runner"
                )
            ),
        },
    )

    
    three_task = PythonOperator(
        task_id="three_task",
        python_callable=readSecret,
        executor_config={
            "pod_template_file": "/opt/airflow/pod_template/pod_template_default.yaml",
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env_from=[
                                k8s.V1EnvFromSource(
                                    config_map_ref=k8s.V1ConfigMapEnvSource(name="demo-log-config-demo00")
                                )
                            ]
                        )
                    ],
                    volumes=[
                            k8s.V1Volume(name="dag-temp", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="dag-temp")),
                    ],
                    service_account_name="dag-test-runner"
                )
            ),
        },
    )

   
    four_task = PythonOperator(
        task_id="four_task",
        python_callable=print_stuff2,
        executor_config={
            "pod_template_file": "/opt/airflow/pod_template/pod_template_default.yaml",
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            env_from=[
                                k8s.V1EnvFromSource(
                                    config_map_ref=k8s.V1ConfigMapEnvSource(name="demo-log-config-demo00")
                                )
                            ]
                        )
                    ],
                    volumes=[
                            k8s.V1Volume(name="dag-temp", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="dag-temp")),
                    ],
                    service_account_name="dag-test-runner"
                )
            ),
        },        
    )

    start_task >> [one_task, two_task, three_task, four_task]
