from pycfhelpers.node.net import CFNodeAddress
from pycfhelpers.node import CFNet
from pycfhelpers.node.crypto import CFGUUID
from pycfhelpers.node.logging import CFLog
from pycfhelpers.node.gdb import CFGDBCluster
import threading

log = CFLog()

BACKBONE_NET = CFNet("Backbone")
MY_CLUSTER_ID = 0x6370756E6B
ROOT_NODES = [CFNodeAddress("D966::0711::935E::EE5E"),
              CFNodeAddress("D8DB::FF73::9F46::9DC4")]

def setup_cluster():
    try:
        log.notice(f"Starting cluster setup ({MY_CLUSTER_ID})...")
        net = BACKBONE_NET
        cluster = CFGDBCluster("CPUNK",
                                 CFGUUID.compose(net.id.long, MY_CLUSTER_ID),
                                 "cpunk.*",
                                  24,
                                  True,
                                  CFGDBCluster.MemberRole.NOBODY,
                                  CFGDBCluster.ClusterRole.AUTONOMIC)

        cluster.add_net_associate(net)
        for member in ROOT_NODES:
            log.notice(f"Adding {member} as root node to the cluster...")
            cluster.member_add(member, CFGDBCluster.MemberRole.ROOT) # Loop through the list and add the root nodes
    except Exception as e:
        log.error(f"Failed to setup cluster: {e}")

def init():
    t = threading.Thread(target=setup_cluster)
    log.notice("Starting cluster thread...")
    t.start() # Start it!
    log.notice("Thread started!")
    return 0

def deinit():
    return 0