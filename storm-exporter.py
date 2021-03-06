#!/usr/bin/python3
import time
import sys
import requests
from prometheus_client import start_http_server, Gauge, Enum

# CLUSTER/SUMMARY METRICS
STORM_CLUSTER_STORM_VERSION = Gauge(
    "cluster_storm_version",
    "Storm version",
)
STORM_CLUSTER_SUPERVISORS_TOTAL = Gauge(
    "cluster_supervisor_total",
    "Number of supervisors running",
)
STORM_CLUSTER_TOPOLOGIES_TOTAL = Gauge(
    "cluster_topology_total",
    "Number of topologies running",
)
STORM_CLUSTER_TOTAL_WORKER_SLOTS = Gauge(
    "cluster_total_worker_slots",
    "Total number of total worker slots",
)
STORM_CLUSTER_USED_WORKER_SLOTS = Gauge(
    "cluster_used_worker_slots",
    "Total number of used worker slots",
)
STORM_CLUSTER_FREE_WORKER_SLOTS = Gauge(
    "cluster_free_worker_slots",
    "Total number of free worker slots",
)
STORM_CLUSTER_EXECUTORS_TOTAL = Gauge(
    "cluster_executor_total",
    "Total number of executors",
)
STORM_CLUSTER_TASKS_TOTAL = Gauge(
    "cluster_task_total",
    "Total number of tasks",
)
STORM_CLUSTER_MEMORY_TOTAL = Gauge(
    "cluster_mem_total",
    "The total amount of memory in the cluster in MB",
)
STORM_CLUSTER_MEMORY_AVAIL = Gauge(
    "cluster_mem_avail",
    "The amount of available memory in the cluster in MB",
)
STORM_CLUSTER_MEMORY_ASSIGNED_PERCENT_UTIL = Gauge(
    "cluster_mem_assigned_per_util",
    "The percent utilization of assigned memory resources in cluster",
)
STORM_CLUSTER_CPU_TOTAL = Gauge(
    "cluster_cpu_total",
    "The total amount of CPU in the cluster",
)
STORM_CLUSTER_CPU_AVAIL = Gauge(
    "cluster_cpu_avail",
    "The amount of available CPU in the cluster",
)
STORM_CLUSTER_CPU_ASSIGNED_PERCENT_UTIL = Gauge(
    "cluster_cpu_assigned_per_util",
    "The percent utilization of assigned CPU resources in cluster",
)

# NIMBUS/SUMMARY METRICS
STORM_NIMBUS_STATUS = Enum(
    "nimbus_status",
    "Nimbus Status, Possible values are Leader, Not a Leader, Dead",
    ["Nimbus"],
    states=["Leader", "Not a Leader", "Dead"],
)

# SUPERVISOR/SUMMARY METRICS
STORM_SUPERVISOR_UPTIME_SECOND = Gauge(
    "supervisor_uptime_second",
    "Shows how long the supervisor is running in seconds",
    ["Supervisor"],
)
STORM_SUPERVISOR_SLOTS_TOTAL = Gauge(
    "supervisor_slots_total",
    "Total number of available worker slots for this supervisor",
    ["Supervisor"],
)
STORM_SUPERVISOR_SLOTS_USED = Gauge(
    "supervisor_slots_used",
    "Number of worker slots used on this supervisor",
    ["Supervisor"],
)
STORM_SUPERVISOR_MEM_TOTAL = Gauge(
    "supervisor_memory_total",
    "Total memory capacity on this supervisor",
    ["Supervisor"],
)
STORM_SUPERVISOR_MEM_USED = Gauge(
    "supervisor_memory_used",
    "Used memory capacity on this supervisor",
    ["Supervisor"],
)
STORM_SUPERVISOR_CPU_TOTAL = Gauge(
    "supervisor_cpu_total",
    "Total CPU capacity on this supervisor",
    ["Supervisor"],
)
STORM_SUPERVISOR_CPU_USED = Gauge(
    "supervisor_cpu_used",
    "Used CPU capacity on this supervisor",
    ["Supervisor"],
)

# TOPOLOGY/SUMMARY METRICS
STORM_TOPOLOGY_UPTIME_SECONDS = Gauge(
    "uptime_seconds",
    "Shows how long the topology is running in seconds",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_TASKS_TOTAL = Gauge(
    "tasks_total",
    "Total number of tasks for this topology",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_WORKERS_TOTAL = Gauge(
    "workers_total",
    "Number of workers used for this topology",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_EXECUTORS_TOTAL = Gauge(
    "executors_total",
    "Number of executors used for this topology",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_REPLICATION_COUNT = Gauge(
    "replication_count",
    "Number of nimbus hosts on which this topology code is replicated",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_REQUESTED_MEM_ON_HEAP = Gauge(
    "requested_mem_on_heap",
    "Requested On-Heap Memory by User (MB)",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_REQUESTED_MEM_OFF_HEAP = Gauge(
    "requested_mem_off_heap",
    "Requested Off-Heap Memory by User (MB)",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_REQUESTED_TOTAL_MEM = Gauge(
    "requested_total_mem",
    "Requested Total Memory by User (MB)",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_REQUESTED_CPU = Gauge(
    "requested_cpu", "Requested CPU by User (%)", ["TopologyName", "TopologyId"]
)
STORM_TOPOLOGY_ASSIGNED_MEM_ON_HEAP = Gauge(
    "assigned_mem_on_heap",
    "Assigned On-Heap Memory by Scheduler (MB)",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_ASSIGNED_MEM_OFF_HEAP = Gauge(
    "assigned_mem_off_heap",
    "Assigned Off-Heap Memory by Scheduler (MB)",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_ASSIGNED_TOTAL_MEM = Gauge(
    "assigned_total_mem",
    "Assigned Total Memory by Scheduler (MB)",
    ["TopologyName", "TopologyId"],
)
STORM_TOPOLOGY_ASSIGNED_CPU = Gauge(
    "assigned_cpu", "Assigned CPU by Scheduler (%)", ["TopologyName", "TopologyId"]
)

# TOPOLOGY/STATS METRICS:
TOPOLOGY_STATS_TRASFERRED = Gauge(
    "topology_stats_trasferred",
    "Number messages transferred in given window",
    ["TopologyName", "TopologyId", "window"],
)
TOPOLOGY_STATS_EMITTED = Gauge(
    "topology_stats_emitted",
    "Number of messages emitted in given window",
    ["TopologyName", "TopologyId", "window"],
)
TOPOLOGY_STATS_COMPLETE_LATENCY = Gauge(
    "topology_stats_complete_latency",
    "Total latency for processing the message",
    ["TopologyName", "TopologyId", "window"],
)
TOPOLOGY_STATS_ACKED = Gauge(
    "topology_stats_acked",
    "Number of messages acked in given window",
    ["TopologyName", "TopologyId", "window"],
)
TOPOLOGY_STATS_FAILED = Gauge(
    "topology_stats_failed",
    "Number of messages failed in given window",
    ["TopologyName", "TopologyId", "window"],
)

# TOPOLOGY/ID WORKERS METRICS:
STORM_TOPOLOGY_WORKER_ASSIGNED_MEM_ON_HEAP = Gauge(
    "worker_mem_assigned_on_heap",
    "Assigned On-Heap Memory by Scheduler (MB)",
    ["TopologyName", "TopologyId", "Supervisor","Port"],
)
STORM_TOPOLOGY_WORKER_EXECUTORS = Gauge(
    "worker_executors",
    "Number of executors used by the topology in this worker",
    ["TopologyName", "TopologyId", "Supervisor","Port"],
)
STORM_TOPOLOGY_WORKER_ASSIGNED_CPU_ON_HEAP = Gauge(
    "worker_cpu_assigned_on_heap",
    "Assigned CPU",
    ["TopologyName", "TopologyId", "Supervisor","Port"],
)
STORM_TOPOLOGY_WORKER_COMPONENT_NUM_TASK = Gauge(
    "worker_component_num_task",
    "Components -> # of executing tasks",
    ["TopologyName", "TopologyId", "Supervisor","BoltId","Port"],
)

# TOPOLOGY/ID SPOUT METRICS:
STORM_TOPOLOGY_SPOUTS_EXECUTORS = Gauge(
    "spouts_executors",
    "Number of executors for the spout",
    ["TopologyName", "TopologyId", "SpoutId"],
)
STORM_TOPOLOGY_SPOUTS_EMITTED = Gauge(
    "spouts_emitted",
    "Number of messages emitted in given window",
    ["TopologyName", "TopologyId", "SpoutId"],
)
STORM_TOPOLOGY_SPOUTS_COMPLETE_LATENCY = Gauge(
    "spouts_complete_latency",
    "Total latency for processing the message",
    ["TopologyName", "TopologyId", "SpoutId"],
)
STORM_TOPOLOGY_SPOUTS_TRANSFERRED = Gauge(
    "spouts_transferred",
    "Total number of messages transferred in given window",
    ["TopologyName", "TopologyId", "SpoutId"],
)
STORM_TOPOLOGY_SPOUTS_TASKS = Gauge(
    "spouts_tasks",
    "Total number of tasks for the spout",
    ["TopologyName", "TopologyId", "SpoutId"],
)
STORM_TOPOLOGY_SPOUTS_ACKED = Gauge(
    "spouts_acked",
    "Number of messages acked",
    ["TopologyName", "TopologyId", "SpoutId"],
)
STORM_TOPOLOGY_SPOUTS_FAILED = Gauge(
    "spouts_failed",
    "Number of messages failed",
    ["TopologyName", "TopologyId", "SpoutId"],
)

# TOPOLOGY/ID BOLT METRICS:
STORM_TOPOLOGY_BOLTS_PROCESS_LATENCY = Gauge(
    "bolts_process_latency",
    "Average time of the bolt to ack a message after it was received",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_CAPACITY = Gauge(
    "bolts_capacity",
    "This value indicates number of messages executed * average execute latency / time window",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_EXECUTE_LATENCY = Gauge(
    "bolts_execute_latency",
    "Average time to run the execute method of the bolt",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_EXECUTORS = Gauge(
    "bolts_executors",
    "Number of executor tasks in the bolt component",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_TASKS = Gauge(
    "bolts_tasks",
    "Number of instances of bolt",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_ACKED = Gauge(
    "bolts_acked",
    "Number of tuples acked by the bolt",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_FAILED = Gauge(
    "bolts_failed",
    "Number of tuples failed by the bolt",
    ["TopologyName", "TopologyId", "BoltId"],
)
STORM_TOPOLOGY_BOLTS_EMITTED = Gauge(
    "bolts_emitted",
    "of tuples emitted by the bolt",
    ["TopologyName", "TopologyId", "BoltId"],
)




def getMetric(metric):
    if metric == None:
        return 0
    else:
        return metric


def statsMetric(stat, tn, tid):
    wd = stat["window"]
    TOPOLOGY_STATS_TRASFERRED.labels(tn, tid, wd).set(getMetric(stat["transferred"]))
    TOPOLOGY_STATS_EMITTED.labels(tn, tid, wd).set(getMetric(stat["emitted"]))
    TOPOLOGY_STATS_COMPLETE_LATENCY.labels(tn, tid, wd).set(
        getMetric(stat["completeLatency"])
    )
    TOPOLOGY_STATS_ACKED.labels(tn, tid, wd).set(getMetric(stat["acked"]))
    TOPOLOGY_STATS_FAILED.labels(tn, tid, wd).set(getMetric(stat["failed"]))


def workersMetric(worker, tn, tid):
    sphost=worker['host']
    wport=worker['port']
    STORM_TOPOLOGY_WORKER_ASSIGNED_MEM_ON_HEAP.labels(tn,tid,sphost,wport).set(getMetric(worker['assignedMemOnHeap']))
    STORM_TOPOLOGY_WORKER_EXECUTORS.labels(tn,tid,sphost,wport).set(getMetric(worker['executorsTotal']))
    STORM_TOPOLOGY_WORKER_ASSIGNED_CPU_ON_HEAP.labels(tn,tid,sphost,wport).set(getMetric(worker['assignedCpu']))
    for numTask in worker['componentNumTasks']:
        STORM_TOPOLOGY_WORKER_COMPONENT_NUM_TASK.labels(tn,tid,sphost,numTask,wport).set(getMetric(worker['componentNumTasks'][numTask]))



def spoutMetric(spout, tn, tid):
    sid = spout["spoutId"]
    STORM_TOPOLOGY_SPOUTS_EXECUTORS.labels(tn, tid, sid).set(
        getMetric(spout["executors"])
    )
    STORM_TOPOLOGY_SPOUTS_EMITTED.labels(tn, tid, sid).set(getMetric(spout["emitted"]))
    STORM_TOPOLOGY_SPOUTS_COMPLETE_LATENCY.labels(tn, tid, sid).set(
        getMetric(spout["completeLatency"])
    )
    STORM_TOPOLOGY_SPOUTS_TRANSFERRED.labels(tn, tid, sid).set(
        getMetric(spout["transferred"])
    )
    STORM_TOPOLOGY_SPOUTS_TASKS.labels(tn, tid, sid).set(getMetric(spout["tasks"]))
    STORM_TOPOLOGY_SPOUTS_ACKED.labels(tn, tid, sid).set(getMetric(spout["acked"]))
    STORM_TOPOLOGY_SPOUTS_FAILED.labels(tn, tid, sid).set(getMetric(spout["failed"]))


def boltMetric(bolt, tn, tid):
    bid = bolt["boltId"]
    STORM_TOPOLOGY_BOLTS_CAPACITY.labels(tn, tid, bid).set(
        getMetric(bolt["capacity"])
    )
    STORM_TOPOLOGY_BOLTS_PROCESS_LATENCY.labels(tn, tid, bid).set(
        getMetric(bolt["processLatency"])
    )
    STORM_TOPOLOGY_BOLTS_EXECUTE_LATENCY.labels(tn, tid, bid).set(
        getMetric(bolt["executeLatency"])
    )
    STORM_TOPOLOGY_BOLTS_EXECUTORS.labels(tn, tid, bid).set(
        getMetric(bolt["executors"])
    )
    STORM_TOPOLOGY_BOLTS_TASKS.labels(tn, tid, bid).set(getMetric(bolt["tasks"]))
    STORM_TOPOLOGY_BOLTS_ACKED.labels(tn, tid, bid).set(getMetric(bolt["acked"]))
    STORM_TOPOLOGY_BOLTS_FAILED.labels(tn, tid, bid).set(getMetric(bolt["failed"]))
    STORM_TOPOLOGY_BOLTS_EMITTED.labels(tn, tid, bid).set(getMetric(bolt["emitted"]))


def topologyMetric(topology):
    tn = topology["name"]
    tid = topology["id"]
    for stat in topology["topologyStats"]:
        statsMetric(stat, tn, tid)
    for worker in topology['workers']:
        workersMetric(worker, tn, tid)
    for spout in topology["spouts"]:
        spoutMetric(spout, tn, tid)
    for bolt in topology["bolts"]:
        boltMetric(bolt, tn, tid)
    

def clusterSummaryMetrics(cluster_summary):
    STORM_CLUSTER_MEMORY_TOTAL.set(cluster_summary['totalMem'])
    STORM_CLUSTER_FREE_WORKER_SLOTS.set(cluster_summary['slotsFree'])
    STORM_CLUSTER_MEMORY_ASSIGNED_PERCENT_UTIL.set(cluster_summary['memAssignedPercentUtil'])
    STORM_CLUSTER_TOPOLOGIES_TOTAL.set(cluster_summary['topologies'])
    STORM_CLUSTER_MEMORY_AVAIL.set(cluster_summary['availMem'])
    STORM_CLUSTER_CPU_TOTAL.set(cluster_summary['totalCpu'])
    STORM_CLUSTER_SUPERVISORS_TOTAL.set(cluster_summary['supervisors'])
    STORM_CLUSTER_CPU_ASSIGNED_PERCENT_UTIL.set(cluster_summary['cpuAssignedPercentUtil'])
    STORM_CLUSTER_TASKS_TOTAL.set(cluster_summary['tasksTotal'])
    STORM_CLUSTER_CPU_AVAIL.set(cluster_summary['availCpu'])
    STORM_CLUSTER_USED_WORKER_SLOTS.set(cluster_summary['slotsUsed'])
    STORM_CLUSTER_TOTAL_WORKER_SLOTS.set(cluster_summary['slotsTotal'])
    STORM_CLUSTER_EXECUTORS_TOTAL.set(cluster_summary['executorsTotal'])

def nimbusSummaryMetrics(nimbus_summary):
    nhost=nimbus_summary['host']
    STORM_NIMBUS_STATUS.labels(nhost).state(nimbus_summary['status'])

def supervisorSummaryMetrics(supervisor_summary):
    suphost = supervisor_summary['host']
    STORM_SUPERVISOR_UPTIME_SECOND.labels(suphost).set(supervisor_summary['uptimeSeconds'])
    STORM_SUPERVISOR_SLOTS_TOTAL.labels(suphost).set(supervisor_summary['slotsTotal'])
    STORM_SUPERVISOR_SLOTS_USED.labels(suphost).set(supervisor_summary['slotsUsed'])
    STORM_SUPERVISOR_MEM_TOTAL.labels(suphost).set(supervisor_summary['totalMem'])
    STORM_SUPERVISOR_MEM_USED.labels(suphost).set(supervisor_summary['usedMem'])
    STORM_SUPERVISOR_CPU_TOTAL.labels(suphost).set(supervisor_summary['totalCpu'])
    STORM_SUPERVISOR_CPU_USED.labels(suphost).set(supervisor_summary['usedCpu'])

def topologySummaryMetric(topology_summary, stormUiHost):
    tn = topology_summary["name"]
    tid = topology_summary["id"]
    STORM_TOPOLOGY_UPTIME_SECONDS.labels(tn, tid).set(topology_summary["uptimeSeconds"])
    STORM_TOPOLOGY_TASKS_TOTAL.labels(tn, tid).set(topology_summary["tasksTotal"])
    STORM_TOPOLOGY_WORKERS_TOTAL.labels(tn, tid).set(topology_summary["workersTotal"])
    STORM_TOPOLOGY_EXECUTORS_TOTAL.labels(tn, tid).set(
        topology_summary["executorsTotal"]
    )
    STORM_TOPOLOGY_REPLICATION_COUNT.labels(tn, tid).set(
        topology_summary["replicationCount"]
    )
    STORM_TOPOLOGY_REQUESTED_MEM_ON_HEAP.labels(tn, tid).set(
        topology_summary["requestedMemOnHeap"]
    )
    STORM_TOPOLOGY_REQUESTED_MEM_OFF_HEAP.labels(tn, tid).set(
        topology_summary["requestedMemOffHeap"]
    )
    STORM_TOPOLOGY_REQUESTED_TOTAL_MEM.labels(tn, tid).set(
        topology_summary["requestedTotalMem"]
    )
    STORM_TOPOLOGY_REQUESTED_CPU.labels(tn, tid).set(topology_summary["requestedCpu"])
    STORM_TOPOLOGY_ASSIGNED_MEM_ON_HEAP.labels(tn, tid).set(
        topology_summary["assignedMemOnHeap"]
    )
    STORM_TOPOLOGY_ASSIGNED_MEM_OFF_HEAP.labels(tn, tid).set(
        topology_summary["assignedMemOffHeap"]
    )
    STORM_TOPOLOGY_ASSIGNED_TOTAL_MEM.labels(tn, tid).set(
        topology_summary["assignedTotalMem"]
    )
    STORM_TOPOLOGY_ASSIGNED_CPU.labels(tn, tid).set(topology_summary["assignedCpu"])

    try:
        r = requests.get("http://" + stormUiHost + "/api/v1/topology/" + tid)
        topologyMetric(r.json())
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    

if len(sys.argv) != 4:
    print(
        "Missing arguments, Usage storm-metrics-consumer.py [StormUI Host] [HTTP port of the consumer] [Refresh Rate in Seconds]"
    )
    sys.exit(-1)

stormUiHost = str(sys.argv[1])
httpPort = int(sys.argv[2])
refreshRate = int(sys.argv[3])

start_http_server(httpPort)
while True:
    try:
        r = requests.get("http://" + stormUiHost + "/api/v1/topology/summary")
        resp_cluster_sum = requests.get("http://" + stormUiHost + "/api/v1/cluster/summary")
        resp_nimbus_sum = requests.get("http://" + stormUiHost + "/api/v1/nimbus/summary")
        resp_supervisor_sum = requests.get("http://" + stormUiHost + "/api/v1/supervisor/summary")
        for supervisor in resp_supervisor_sum.json()["supervisors"]:
            supervisorSummaryMetrics(supervisor)
        for nimbus in resp_nimbus_sum.json()["nimbuses"]:
            nimbusSummaryMetrics(nimbus)
        clusterSummaryMetrics(resp_cluster_sum.json())
        print("caught metrics")
        for topology in r.json()["topologies"]:
            topologySummaryMetric(topology, stormUiHost)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    time.sleep(refreshRate)
