# from social.backends.facebook import FacebookOAuth2

# def save_profile(backend, user, response, *args, **kwargs):
#     if isinstance(backend, FacebookOAuth2):
#         if response.get('image') and response['image'].get('url'):
#             url = response['image'].get('url')
#             user.url = url
#             user.save()