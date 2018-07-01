# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](http://pythonhosted.org/airflow/tutorial.html)
"""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta


# these args will get passed on to each operator
# you can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
    #'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

dag = DAG(
    'MNIST-edp',
    catchup=False,
    default_args=default_args,
    description='MNIST - execute data pipeline',
    #schedule_interval=timedelta(days=1))
    schedule_interval='0 0 * * *')


# t1, t2 and t3 are examples of tasks created by instantiating operators
sdate = """{{ execution_date }}"""
path_base = "/root/mnt/dfs/notebooks-skp/mnist"
path_data = "/root/mnt/dfs/data/mnist"

def get_cmd(path_base, nb_file):
    cmd = 'SDATE="{}" PATH_BASE="{}" PATH_DATA="{}" '.format(sdate, path_base, path_data)
    cmd += "jupyter nbconvert --to markdown --execute {}/src/backend/{} --stdout ".format(path_base, nb_file)
    cmd += "--ExecutePreprocessor.startup_timeout=600 "
    cmd += "--ExecutePreprocessor.timeout=600 "
    cmd += "--ExecutePreprocessor.kernel_name=python3" 
    return cmd

crd_cmd = get_cmd(path_base, "crd.ipynb")
crd = BashOperator(
    task_id = 'crd',
    bash_command = crd_cmd,
    dag = dag)

crd.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""

dag.doc_md = __doc__

# DNN
etl_dnn_cmd = get_cmd(path_base, "etl-dnn.ipynb")
etl_dnn = BashOperator(
    task_id = 'etl-dnn',
    depends_on_past = False,
    bash_command = etl_dnn_cmd,
    dag = dag)

etl_dnn.set_upstream(crd)

fdm_dnn_cmd = get_cmd(path_base, "fdm-dnn.ipynb")
fdm_dnn = BashOperator(
    task_id = 'fdm-dnn',
    depends_on_past = False,
    bash_command = fdm_dnn_cmd,
    dag = dag)


fdm_dnn.set_upstream(etl_dnn)

# CNN
etl_cnn_cmd = get_cmd(path_base, "etl-cnn.ipynb")
etl_cnn = BashOperator(
    task_id = 'etl-cnn',
    depends_on_past = False,
    bash_command = etl_cnn_cmd,
    dag = dag)

etl_cnn.set_upstream(crd)

fdm_cnn_cmd = get_cmd(path_base, "fdm-cnn.ipynb")
fdm_cnn = BashOperator(
    task_id = 'fdm-cnn',
    depends_on_past = False,
    bash_command = fdm_cnn_cmd,
    dag = dag)


fdm_cnn.set_upstream(etl_cnn)
