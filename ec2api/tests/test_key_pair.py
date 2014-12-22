# Copyright 2014
# The Cloudscaling Group, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64

from novaclient import exceptions as nova_exception

from ec2api.tests import base
from ec2api.tests import fakes
from ec2api.tests import matchers
from ec2api.tests import tools


class KeyPairCase(base.ApiTestCase):

    def test_create_key_pair(self):
        self.nova_key_pairs.create.return_value = (
            fakes.NovaKeyPair(fakes.OS_KEY_PAIR))
        resp = self.execute('CreateKeyPair', {'KeyName': 'keyname'})
        self.assertEqual(200, resp['status'])
        self.assertThat(fakes.EC2_KEY_PAIR, matchers.DictMatches(
            tools.purge_dict(resp, {'status'})))
        self.nova_key_pairs.create.assert_called_once_with('keyname')

    def test_create_key_pair_invalid(self):
        self.nova_key_pairs.create.side_effect = (
            nova_exception.Conflict(409))
        resp = self.execute('CreateKeyPair', {'KeyName': 'keyname'})
        self.assertEqual(400, resp['status'])
        self.assertEqual('InvalidKeyPair.Duplicate', resp['Error']['Code'])
        resp = self.execute('CreateKeyPair', {'KeyName': 'k' * 256})
        self.assertEqual(400, resp['status'])
        self.assertEqual('InvalidParameterValue', resp['Error']['Code'])
        self.nova_key_pairs.create.side_effect = (
            nova_exception.OverLimit(413))
        resp = self.execute('CreateKeyPair', {'KeyName': 'keyname'})
        self.assertEqual(400, resp['status'])
        self.assertEqual('ResourceLimitExceeded', resp['Error']['Code'])

    def test_import_key_pair(self):
        self.nova_key_pairs.create.return_value = (
            fakes.NovaKeyPair(fakes.OS_KEY_PAIR))
        resp = self.execute('ImportKeyPair',
                            {'KeyName': 'keyname',
                             'PublicKeyMaterial': base64.b64encode(
                                fakes.PUBLIC_KEY)})
        self.assertEqual(200, resp['status'])
        self.assertThat(tools.purge_dict(fakes.EC2_KEY_PAIR, {'keyMaterial'}),
            matchers.DictMatches(tools.purge_dict(resp, {'status'})))
        self.nova_key_pairs.create.assert_called_once_with('keyname',
                                                           fakes.PUBLIC_KEY)

    def test_import_key_pair_invalid(self):
        self.nova_key_pairs.create.side_effect = (
            nova_exception.OverLimit(413))
        resp = self.execute('ImportKeyPair',
                            {'KeyName': 'keyname',
                             'PublicKeyMaterial': base64.b64encode(
                                fakes.PUBLIC_KEY)})
        self.assertEqual(400, resp['status'])
        self.assertEqual('ResourceLimitExceeded', resp['Error']['Code'])

    def test_delete_key_pair(self):
        self.nova_key_pairs.delete.return_value = True
        resp = self.execute('DeleteKeyPair', {'KeyName': 'keyname'})
        self.assertEqual(200, resp['status'])
        self.nova_key_pairs.delete.assert_called_once_with('keyname')
        self.nova_key_pairs.delete.side_effect = nova_exception.NotFound(404)
        resp = self.execute('DeleteKeyPair', {'KeyName': 'keyname1'})
        self.assertEqual(200, resp['status'])
        self.nova_key_pairs.delete.assert_any_call('keyname1')

    def test_describe_key_pair(self):
        self.nova_key_pairs.list.return_value = [fakes.NovaKeyPair(
                                                    fakes.OS_KEY_PAIR)]
        resp = self.execute('DescribeKeyPairs', {})
        self.assertEqual(200, resp['status'])
        self.assertThat(resp['keySet'],
                        matchers.ListMatches([
                            tools.purge_dict(fakes.EC2_KEY_PAIR,
                                             {'keyMaterial'})]))
        self.nova_key_pairs.list.assert_called_once()

    def test_describe_key_pair_invalid(self):
        self.nova_key_pairs.list.return_value = [fakes.NovaKeyPair(
                                                    fakes.OS_KEY_PAIR)]
        resp = self.execute('DescribeKeyPairs', {'KeyName': 'badname'})
        self.assertEqual(404, resp['status'])
        self.assertEqual('InvalidKeyPair.NotFound', resp['Error']['Code'])
        self.nova_key_pairs.list.assert_called_once()
