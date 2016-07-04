
from ansible import errors


def validate_ruleset(ports, proto):
    '''
    check for emtpy values
    :param ports: should be list
    :param proto: should be list
    :raise: ansible error on failure
    '''
    if proto is None or len(proto) < 0:
        raise errors.AnsibleFilterError('proto is empty or missing')
    if ports is None or len(ports) < 0:
        raise errors.AnsibleFilterError('ports is empty or missing')


def rules_from_dict(rules, src_list=[]):
    '''
    rules:
      - ports: '22'
          proto: tcp
          src: (optional)

     ec2_group:
       rules: "{{ ruleslist | rules_from_dict() }}"

    :param rules: list of rule
    :src_list: src group/cidr list
    :return: list of rules
    '''

    if isinstance(rules, list):
        rule_list = []
        if len(rules) > 0:
            for rule in rules:
                if 'src' in rule.keys():
                    src_list = rule.get('src')
                if len(src_list) > 0 and isinstance(src_list, list):
                    rule_list += make_rules(src_list,rule['ports'], rule['proto'],('sg' in src_list[0]))
                else:
                    raise errors.AnsibleFilterError('src host or security group list empty or not a list')
            return rule_list
        return False
    else:
        raise errors.AnsibleFilterError('Rules data must be a list')


def make_rules(hosts, ports, proto, group=False):
    '''
    inspiration: https://gist.github.com/viesti/1febe79938c09cc29501

    :param hosts: list
    :param ports: comma separated string
    :param proto: string
    :param group: bool default false
    :return: rules as list of dicts
    '''
    if isinstance(hosts, list) and len(hosts) > 0:
        validate_ruleset(ports, proto)
        # print "{}".format(hosts)
        if group:
            return [{'proto': proto,
                 'from_port': port,
                 'to_port': port,
                 'group_id': sg} for sg in hosts for port in map(int, ports.split(','))]
        return [{'proto': proto,
             'from_port': port,
             'to_port': port,
             'cidr_ip': host} for host in hosts for port in map(int, ports.split(','))]
    else:
        raise errors.AnsibleFilterError('list of hosts or security groups must be a list')


def get_sg_result(result_list):
    if isinstance(result_list, list) and len(result_list) > 0:
        for result in result_list:
            if result.get('group_id'):
                return result
    else:
        raise errors.AnsibleFilterError('results list is empty or net a list')


def get_sg_id_result(result_list):
    if isinstance(result_list, list) and len(result_list) > 0:
        for result in result_list:
            if result.get('group_id'):
                return result.get('group_id')
    else:
        raise errors.AnsibleFilterError('results list is empty or net a list')

class FilterModule(object):
     def filters(self):
         filter_list = {
             'make_rules': make_rules,
             'rules_from_dict': rules_from_dict,
             'get_sg_result': get_sg_result,
             'get_sg_id_result': get_sg_id_result
         }
         return filter_list