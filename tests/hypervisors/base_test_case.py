# Copyright 2013 Locaweb.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

import random


class HypervisorBaseTest(object):
    # debugging:
    # import sys; sys.stdout = sys.__stdout__; import ipdb; ipdb.set_trace()

    def test_pool_info(self):
        pool = self.stack.pool_info()
        self.assertNotEqual(pool.get("total_memory"), None)
        self.assertNotEqual(pool.get("used_memory"), None)
        self.assertNotEqual(pool.get("master"), None)

    def test_host_list(self):
        hosts = self.stack.host_list()
        self.assertNotEqual(len(hosts), 0)

    def test_host_info(self):
        hosts = self.stack.host_list()
        host = self.stack.host_info(hosts[0]["id"])
        self.assertTrue(host["name"])
        self.assertTrue(host["address"])

    def test_storage_list(self):
        storages = self.stack.storage_list()
        self.assertNotEqual(len(storages), 0)

    def test_storage_info(self):
        storages = self.stack.storage_list()
        storage = self.stack.storage_info(storages[0]["id"])
        self.assertTrue(storage["type"])
        self.assertTrue(type(storage["allocated_space"]), int)

    def test_guest_create(self):
        """
        This method is tested on every hypervisor setup!
        """
        pass

    def test_guest_list(self):
        guests = self.stack.guest_list()
        self.assertNotEqual(guests, [])

    def test_guest_info(self):
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["id"], self._get_vm_id())
        self.assertFalse(guest["tools_up_to_date"])
        self.assertFalse(guest["ip"])

    def test_guest_start(self):
        self._stop_vm()
        self.stack.guest_start(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_force_reboot(self):
        force = True
        self.stack.guest_reboot(self._get_vm_id(), force)
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_reboot(self):
        # The created vm should have the correct tool for this method
        return

        self.stack.guest_reboot(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_shutdown(self):
        force = True
        self.stack.guest_shutdown(self._get_vm_id(), force)
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STOPPED")

    def test_guest_suspend(self):
        self.stack.guest_suspend(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "PAUSED")

    def test_guest_resume(self):
        self.stack.guest_suspend(self._get_vm_id())
        self.stack.guest_resume(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_update(self):
        vm = "vm%f" % random.random()
        guest_data = {
            "memory": 128, "cpus": 2, "name": vm, "hdd": 50,
            "paravirtualized": "-- quiet console=hvc0"
        }
        self.stack.guest_shutdown(self._get_vm_id(), True)
        guest = self.stack.guest_update(self._get_vm_id(), guest_data)
        self.assertEqual(guest["memory"], guest_data["memory"])
        self.assertEqual(guest["cpus"], guest_data["cpus"])
        self.assertEqual(guest["name"], guest_data["name"])
        self.assertEqual(guest["hdd"], guest_data["hdd"])
        self.assertTrue(guest["paravirtualized"])

        guest_data = {
            "paravirtualized": False
        }
        guest = self.stack.guest_update(self._get_vm_id(), guest_data)
        self.assertFalse(guest["paravirtualized"])

    def test_disk_list(self):
        disks = self.stack.disk_list(self._get_vm_id())
        self.assertNotEqual(len(disks), 0)

    def test_disk_create(self):
        size = 1
        disk = self.stack.disk_create(self._get_vm_id(), {"size": size})
        self.assertEqual(disk["size"], 1)

    def test_disk_info(self):
        disks = self.stack.disk_list(self._get_vm_id())
        disk = self.stack.disk_info(
            self._get_vm_id(), disks[0]['id']
        )
        self.assertEqual(disk['id'], disks[0]['id'])

    def test_disk_update(self):
        name = "DISK"
        self.stack.guest_shutdown(self._get_vm_id(), True)
        disks = self.stack.disk_list(self._get_vm_id())
        disk = self.stack.disk_update(
            self._get_vm_id(), disks[0]['id'], {"name": name}
        )
        self.assertEqual(disk['name'], name)

    def test_media_unmount(self):
        self.stack.media_mount(self._get_vm_id(), {"name": None})
        media = self.stack.media_info(self._get_vm_id())
        self.assertEqual(media["name"], None)

    def test_media_mount(self):
        self.stack.media_mount(self._get_vm_id(), {"name": self._media_name()})
        media = self.stack.media_info(self._get_vm_id())
        self.assertEqual(media["name"], self._media_name())

    def test_network_interface_list(self):
        nw_interfaces = self.stack.network_interface_list(self._get_vm_id())
        self.assertNotEqual(len(nw_interfaces), 0)

    def test_network_interface_create(self):
        # TODO: change network
        self.stack.guest_shutdown(self._get_vm_id(), True)

        p = {"network": self._network_name()}
        created_nw = self.stack.network_interface_create(self._get_vm_id(), p)
        nw_interface = self.stack.network_interface_info(
            self._get_vm_id(),
            created_nw['id']
        )
        self.assertEqual(created_nw['id'], nw_interface['id'])

    def test_network_interface_info(self):
        nw_interfaces = self.stack.network_interface_list(self._get_vm_id())
        nw_interface = self.stack.network_interface_info(
            self._get_vm_id(), nw_interfaces[0]['id']
        )
        self.assertEqual(nw_interface['id'], nw_interfaces[0]['id'])

    def test_network_interface_update(self):
        # TODO: change network
        self.stack.guest_shutdown(self._get_vm_id(), True)
        nw_interfaces = self.stack.network_interface_list(self._get_vm_id())
        nw_interface = self.stack.network_interface_update(
            self._get_vm_id(), nw_interfaces[0]['id'],
            {"ratelimit": 10 * 1024 * 1024}
        )
        nw_interface = self.stack.network_interface_update(
            self._get_vm_id(), nw_interfaces[0]['id'], {"ratelimit": False}
        )
        self.assertEqual(nw_interface['id'], nw_interfaces[0]['id'])

    def test_network_interface_delete(self):
        self.stack.guest_shutdown(self._get_vm_id(), True)

        p = {"network": self._network_name()}
        created_nw = self.stack.network_interface_create(self._get_vm_id(), p)
        self.stack.network_interface_delete(
            self._get_vm_id(),
            created_nw['id']
        )
        nw_interfaces = self.stack.network_interface_list(self._get_vm_id())
        for nw_interface in nw_interfaces:
            self.assertNotEqual(created_nw['id'], nw_interface['id'])

    def test_snapshot_list(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        snaps = self.stack.snapshot_list(self._get_vm_id())
        self.assertIn(snap, snaps)

    def test_snapshot_create(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        self.assertEqual(snap["name"], snap_name)

    def test_snapshot_info(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        snap = self.stack.snapshot_info(self._get_vm_id(), snap["id"])
        self.assertEqual(snap["name"], snap_name)

    def test_snapshot_revert(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        self.stack.snapshot_revert(self._get_vm_id(), snap["id"])

    def test_snapshot_delete(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        self.stack.snapshot_delete(self._get_vm_id(), snap["id"])
        snaps = self.stack.snapshot_list(self._get_vm_id())
        self.assertNotIn(snap, snaps)

    def test_tag_list(self):
        tag_name = "v0.0.1"
        guest_tags = self.stack.tag_create(self._get_vm_id(), tag_name)
        tags_list = self.stack.tag_list(self._get_vm_id())
        self.assertEqual(guest_tags, tags_list)

    def test_tag_create(self):
        tag_name = "v0.0.1"
        guest_tags = self.stack.tag_create(self._get_vm_id(), tag_name)
        tags_list = self.stack.tag_list(self._get_vm_id())
        self.assertIn(tag_name, tags_list)

    def test_tag_delete(self):
        tag_name = "v0.0.1"
        self.stack.tag_create(self._get_vm_id(), tag_name)
        self.stack.tag_delete(self._get_vm_id(), tag_name)

        tags = self.stack.tag_list(self._get_vm_id())
        self.assertNotIn(tag_name, tags)
