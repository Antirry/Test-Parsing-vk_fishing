from requests import Session


class Parsing_Group_VK:
    def __init__(self, params:dict) -> None:
        self.params = params
        self.session = Session()

    def _count_members(self) -> int:
        try:
            r = self.session.get('https://api.vk.com/method/groups.getMembers',
                                params=self.params)

            return r.json()['response']['count']
        except Exception as e:
            print(e)


    def _count_friends(self, user_id:int) -> int:
        try:
            params = self.params.copy()
            params.update({'user_id': user_id})
            r = self.session.get('https://api.vk.com/method/friends.get',
                                params=params, stream=True)

            return int(r.json()['response']['count'])
        except KeyError:
            return 0


    def members_from_group(self, offset:int) -> dict:
        """Выявляем параметр offset для групп, 1 смещение * 1000 id"""
        try:
            params = self.params.copy()
            params.update(
                        {
                            'fields': 'last_seen,contacts,city,bdate',
                            'offset': offset*1000
                        }
            )
            r = self.session.get('https://api.vk.com/method/groups.getMembers',
                                params=params)

            return r.json()['response']['items']
        except Exception as e:
            print(e)
