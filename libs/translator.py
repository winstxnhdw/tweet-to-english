from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def translate_to_english(text):

    try:
        from api_keys.ibm import KEY, URL

    except ImportError:
        from os import environ as env
        KEY = env['IBM_KEY']
        URL = env['IBM_URL']
        
    auth = IAMAuthenticator(KEY)

    language_translator = LanguageTranslatorV3(version='2018-05-01', authenticator=auth)
    language_translator.set_service_url(URL)

    # Identify
    language = language_translator.identify(text).get_result()['languages'][0]['language']
    print("Detected language: {}".format(language))

    if language == 'en':
        return None

    # Translate
    translation = language_translator.translate(text=text, source=language, target='en').get_result()['translations'][0]['translation']

    return translation