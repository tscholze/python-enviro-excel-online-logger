"""
Configuration settings for the Værmelder Python console app.

See
 https://docs.microsoft.com/en-us/graph/auth-register-app-v2 
for further information and a tutorial.
"""

"""
Azure Active Directory app client id.

Caution:
    Changes required.

Edit this with your generated and secret id.
"""
CLIENT_ID = '<INSERT CLIENT ID>'

"""
App name.
No changes required.
"""
APP_NAME = 'vaermelder-python'

"""
Authority url.
No changes required.
"""
AUTHORITY_URL = 'https://login.microsoftonline.com/common'

"""
Resource identifier url.
No changes required.
"""
RESOURCE = 'https://graph.microsoft.com'
