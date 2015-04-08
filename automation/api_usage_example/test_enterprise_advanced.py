import argparse
import logging
import os

from automation_api_base import AutomationApiBase

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

class TestAutomationApi(AutomationApiBase):

    def __init__(self, base_url, agent_hostname, group_id, api_user, api_key, config_name):
        AutomationApiBase.__init__(self, base_url, agent_hostname, group_id, api_user, api_key)
        self.config_name = config_name

    def clean(self):
        self.post_automation_config("configs/api_0_clean.json")

    def run(self):
        self.post_automation_config("configs/%s.json" % self.config_name)

        if os.path.exists("configs/%s_monitoring_agent.json" % self.config_name):
            self.post_monitoring_agent_config("configs/%s_monitoring_agent.json" % self.config_name)

        if os.path.exists("configs/%s_backup_agent.json" % self.config_name):
            self.post_backup_agent_config("configs/%s_backup_agent.json" % self.config_name)

        #self.wait_for_goal_state()


if __name__ == '__main__':

    # python test_enterprise_advanced.py http://ec2-54-69-72-157.us-west-2.compute.amazonaws.com:8080/ ec2-52-5-159-56.compute-1.amazonaws.com 541ed2009436399a1f54e01b cailin.nelson@10gen.com 786da787-2403-4021-9cac-5a0f170a9e1a
    parser = argparse.ArgumentParser(description='Automation API Demo')
    parser.add_argument('base_url', help="Base URL")
    parser.add_argument('agent_hostname', help="Agent Hostname")
    parser.add_argument('group_id', help="Group ID")
    parser.add_argument('api_user', help="API User")
    parser.add_argument('api_key', help="API Key")
    parser.add_argument('config_name', help="ConfigName")
    parser.add_argument('--clean', action='store_true', required=False)
    args = parser.parse_args()

    test = TestAutomationApi(
        args.base_url,
        args.agent_hostname,
        args.group_id,
        args.api_user,
        args.api_key,
        args.config_name
    )

    if args.clean:
        test.clean()
    else:
        test.run()

