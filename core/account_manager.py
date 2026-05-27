import json
import os
import uuid
import shutil


class AccountManager:

    CONFIG_PATH = 'config/accounts.json'

    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):

        if not os.path.exists(self.CONFIG_PATH):
            return []

        with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_accounts(self):

        with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(
                self.accounts,
                f,
                ensure_ascii=False,
                indent=2
            )

    def add_account(self):

        account_id = str(uuid.uuid4())

        account = {
            'id': account_id,
            'name': f'账号{len(self.accounts)+1}',
            'user_data_dir': f'userdata/{account_id}'
        }

        self.accounts.append(account)

        self.save_accounts()

        return account

    def delete_account(self, account_id):

        target = None

        for acc in self.accounts:

            if acc['id'] == account_id:

                target = acc

                break

        if not target:
            return

        # 删除用户目录
        user_data_dir = target['user_data_dir']

        if os.path.exists(user_data_dir):

            shutil.rmtree(user_data_dir)

        # 删除账号
        self.accounts.remove(target)

        self.save_accounts()