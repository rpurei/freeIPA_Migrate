from applog import logger


def ipa_search_all_groups(ipa_users_file, ipa_usr, ipa_pwd, client):
    groups_set = set()
    try:
        client.login(ipa_usr, ipa_pwd)
        logger.info(f'Authentificated user {ipa_usr}')
        with open(ipa_users_file, encoding='utf8') as f:
            for line in f:
                if line.split(': ')[0].lstrip() == 'Member of groups':
                    groups_list = [item.lstrip() for item in line.split(': ')[1].split(',')]
                    for index, element in enumerate(groups_list):
                        if 'aim2me' in element:
                            groups_list[index] = groups_list[index].replace('aim2me', 'nprsrf')
                        if 'aoamt' in element:
                            groups_list[index] = groups_list[index].replace('aoamt', 'nprs')
                        if element.endswith('\n'):
                            groups_list[index] = groups_list[index].replace('\n', '')
                    groups_set.update(groups_list)
        logger.info(f'Founded groups: {groups_set}')
        return groups_set
    except Exception as err:
        logger.error(f'In function search_all_groups() error: {str(err)}')


def ipa_add_groups(group_list, ipa_usr, ipa_pwd, client):
    try:
        client.login(ipa_usr, ipa_pwd)
        logger.info(f'Authentificated user {ipa_usr}')
        for group_name in group_list:
            group = client.group_find(o_cn=group_name)
            if group['count'] == 0:
                client.group_add(a_cn=group_name)
                logger.info(f'Group {group_name} added to IPA')
            else:
                logger.info(f'Group {group_name} founded on IPA')
    except Exception as err:
        logger.error(f'In function add_groups() error: {str(err)}')
