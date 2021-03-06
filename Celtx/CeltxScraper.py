import requests
from lxml import html as lxml_html


class LoginError(Exception):
    pass


class AuthSession:
    def __init__(self, url, username, password):
        super(AuthSession, self).__init__()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36', 'content-type': 'application/json'}
        self.login_data = {'username': username, 'password': password}
        self.url = url
        self.session = None
        self.token_id_form = []

    def login(self):
        with requests.Session() as s:
            self.session = s
            r = s.post(self.url, json=self.login_data, headers=self.headers)
            if r.status_code == 401:
                raise LoginError
            self.session = s

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    def get_content_disposition(self, r):
        return r.headers['Content-disposition']


class CeltxHook:
    def __init__(self, login_callback):
        self.session = None
        self.login_callback = login_callback
        self.login_url = "https://www.celtx.com/auth/signin"
        self.scripts_url = "https://www.celtx.com/feeds/default/private/full"

    def get_celtx_scripts(self):
        try:
            return self.get_all_scripts_from_raw_items(self.get_raw_script_json())
        except AttributeError:
            self.login()
            return self.get_celtx_scripts()

    def get_raw_script_json(self):
        r = self.session.get(self.scripts_url)
        return r.json()['items']

    @staticmethod
    def get_all_scripts_from_raw_items(items):
        for item in items:
            if item['kind'] == 'script' and item['type'] == 'application/x-celtx-script+xml; celtxType=screenplay':
                yield item

    def get_script_html(self, script):
        return self.try_to_get_from_session(script['content']).content

    def try_to_get_from_session(self, to_get):
        try:
            return self.session.get(to_get)
        except AttributeError:
            self.login()
            return self.try_to_get_from_session(to_get)

    def login(self):
        try:
            self.session.login()
        except AttributeError:
            login_data = self.login_callback()
            self.session = AuthSession(self.login_url, *login_data[0])


def get_scenes_and_sounds_from_html(html):
    root = lxml_html.fromstring(html)
    p_elements = root.xpath("//p")
    scenes_and_sounds = []
    for p_element in p_elements:
        try:
            p_class = p_element.get('class')
            p_text = p_element.text.upper()
            if p_class == 'sceneheading':
                scene = {'type': "scene_header", 'content': p_text, 'scene_number': p_element.get('scenenumber')}
                scenes_and_sounds.append(scene)
            elif p_class == 'action' and p_text[:6].lower() == 'sound:':
                sound = {'type': 'sound', 'content': p_text}
                scenes_and_sounds.append(sound)
        except (AttributeError, TypeError):
            continue
    return scenes_and_sounds


def format_script_title(title: str):
    digit_groups = get_groups_of_digits_from_string(title)
    new_title = title
    if len(digit_groups) > 0:
        digit = int("".join(digit_groups[0]))
        new_title = title.replace(str(digit), f"{digit:03}")
    return new_title.upper()


def get_groups_of_digits_from_string(string):
    number_groups = []
    last_character_was_digit = False
    for character in string:
        if character.isdigit():
            if last_character_was_digit:
                number_groups[-1].append(character)
            else:
                number_groups.append([character])
                last_character_was_digit = True
        else:
            last_character_was_digit = False
    return number_groups


# try:
#     celtx = CeltxHook()
#     scripts = celtx.get_celtx_scripts()
#     for script in scripts:
#         script_html = celtx.get_script_html(script)
#         get_scenes_and_sounds_from_html(script_html)
# except LoginError:
#     print("Wrong Auth")
