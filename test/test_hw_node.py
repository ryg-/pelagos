import unittest
import os
import shutil

import pxelinux_cfg
import network_manager
import hw_node


class pxelinux_cfg_test(unittest.TestCase):

    def test_hw_node_ipmitool(self):
        network_manager.data_file = 'test/test_network_cfg.json'
        hw_node.ipmi_user = network_manager.get_option('ipmi_user')
        hw_node.ipmi_pass = network_manager.get_option('ipmi_pass')


        node = network_manager.get_node_by_name('test_node')

        cmd = hw_node.get_ipmi_cycle_cmd('1.2.3.4', 'user', 'password')
        self.assertEqual(cmd,
                         "ipmitool -H 1.2.3.4 -U user -P password -I lanplus power cycle"
                         )
        hw_node.ipmitool_bin = 'echo'
        hw_node.power_cycle(node)

    def test_hw_node_salt_ssh(self):
        network_manager.data_file = 'test/test_hw_node.json'
        hw_node.init()
        cmd  = hw_node.get_salt_cmd('test_sls', 'test_node')
        self.assertEqual(cmd,
        'salt-ssh -i --roster-file deploy.roster -c . --no-host-keys --key-deploy --passwd ssh_pass "test_node"  state.apply test_sls -l debug')

    def test_read_last_meaningful_line(self):
        line = hw_node.read_last_meaningful_line('test/conman_file.1')
        print("\n line1 = " + line + "\n")
        self.assertEqual(0,line.index(
            '2020-01-29 16:57:47 ^[[19;1HSATA^[[19;6HPort^'))
        line = hw_node.read_last_meaningful_line('test/conman_file.2')
        print("\n line2 = " + line + "\n")
        self.assertEqual(0,line.index(
            '2020-01-29 21:20:32 Welcome to openSUSE'))



    #TODO should be used when conman suppot added to teuthology
    #def test_hw_conman(self):
    #    network_manager.data_file = 'test/test_network_cfg.json'
    #    node = network_manager.get_node_by_name('test_node')
    #    cmd = hw_node.get_conman_cmd('1.2.3.4', 'test_node')
    #    self.assertEqual(cmd,
    #                     "conman -d 1.2.3.4 -j test_node"
    #                     )
    #    hw_node.conman_bin = 'echo  login: '
    #    hw_node.wait_node_is_ready(node)
    # comment it because it is should do activity on a node
    #def test_salt_rub(self):
    #    network_manager.data_file = 'test/test_hw_node.json'
    #    node = network_manager.get_node_by_name('ses-client-8')
    #    hw_node.minimal_needed_configuration(node)

if __name__ == '__main__':
    unittest.main()
