from applog import logger


def user_add_manager(ipa_users_file, ipa_usr, ipa_pwd, client):
    try:
        client.login(ipa_usr, ipa_pwd)
        logger.info(f'Authentificated user {ipa_usr}')
        with open(ipa_users_file, encoding='utf8') as f:
            user_login = user_manager = ''
            for line in f:
                try:
                    if line.split(': ')[0].lstrip() == 'User login':
                        user_login = line.split(': ')[1][:-1]
                    if line.split(': ')[0].lstrip() == 'Manager':
                        user_manager = line.split(': ')[1][:-1]
                    if line == '\n':
                        if user_manager:
                            client.user_add_manager(a_uid=user_login, 
                                                    o_user=user_manager)
                            logger.info(f'For user login: "{user_login}" added manager "{user_manager}"')
                except Exception as err:
                    logger.error(f'In managers processing error: {str(err)}')
    except Exception as err:
        logger.error(f'In function add_manager() error: {str(err)}')


def user_add_department(ipa_users_file, ipa_usr, ipa_pwd, client):
    try:
        client.login(ipa_usr, ipa_pwd)
        logger.info(f'Authentificated user {ipa_usr}')
        with open(ipa_users_file, encoding='utf8') as f:
            user_login = ''
            user_department_number = ''
            user_department_number_list = []
            for line in f:
                if line.split(': ')[0].lstrip() == 'User login':
                    user_login = line.split(': ')[1][:-1]
                if line.split(': ')[0].lstrip() == 'Department Number':
                    user_department_number = line.split(': ')[1][:-1]
                    user_department_number_list = [item.lstrip() for item in user_department_number.split(',')]
                if line == '\n':
                    user_find = client.user_find(o_uid=user_login)
                    try:
                        if user_find['count'] == 1:
                            if user_department_number:
                                client.user_mod(a_uid=user_login,
                                                o_delattr=f'departmentnumber={user_department_number}')
                                for dep_num in user_department_number_list:
                                    client.user_mod(a_uid=user_login, 
                                                    o_addattr=f'departmentnumber={dep_num}')
                                    logger.info(f'For user login: "{user_login}" added department "{dep_num}"')
                        user_login = ''
                        user_department_number = ''
                        user_department_number_list = []
                    except Exception as err:
                        logger.error(f'In department processing error: {str(err)}')
    except Exception as err:
        logger.error(f'In function user_department_mod() error: {str(err)}')


def user_passwdexp_mod(ipa_usr, ipa_pwd, client):
    try:
        client.login(ipa_usr, ipa_pwd)
        logger.info(f'Authentificated user {ipa_usr}')
        user = client.user_find()
        logger.info(f'Founded: {len(user["result"])} users')
        for usr in user['result']:
            try:
                if usr['krbpasswordexpiration'][0]['__datetime__'] != '20991231235959Z':
                    client.user_mod(a_uid=usr['uid'][0], 
                                    o_krbpasswordexpiration=f'20991231235959Z')
                    logger.info(f'Password exp changed for user: {usr["uid"][0]}')
                logger.info(f'Processed user: {usr["uid"][0]}')
            except Exception as err:
                logger.error(f'In user password processing error: {str(err)}')
    except Exception as err:
        logger.error(f'In function user_passwdexp_mod() error: {str(err)}')


def user_email_changer(ipa_usr, ipa_pwd, client):
    try:
        client.login(ipa_usr, ipa_pwd)
        logger.info(f'Authentificated user {ipa_usr}')
        user = client.user_find(a_criteria='@nprsrf.ru')
        logger.info(f'Founded: {len(user["result"])} users')
        counter = 0
        all_count = 0
        for usr in user['result']:
            try:
                all_count += 1
                logger.info(all_count)
                if usr.get('mail'):
                    email_lst = usr['mail'][0].split('@')
                    if email_lst[1] == 'nprsrf.ru':
                        new_mail = email_lst[0] + '@' + 'nprsrf.net'
                        client.user_mod(a_uid=usr['uid'][0],
                                        o_mail=new_mail)
                        counter += 1
                        logger.info(f'User counter: {counter} set email: {new_mail}')
                logger.info(f'Processed user: {usr["uid"][0]}')
            except Exception as err:
                logger.error(f'In user email processing error: {str(err)}')
    except Exception as err:
        logger.error(f'In function user_email_changer() error: {str(err)}')
