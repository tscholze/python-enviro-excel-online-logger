import config
import urllib
import requests
import datetime
from timer import RepeatingTimer
from adal import AuthenticationContext
from envirophat import light, weather


def get_session():
    """
    Gets a valid Microsoft Graph HTTP-Session.
    Will ask the user for permission.
    """

    # Create new authentication context which will be
    # used to have access to the user's information.
    auth_context = AuthenticationContext(
        config.AUTHORITY_URL, api_version=None)

    # Get the device code.
    device_code = auth_context.acquire_user_code(config.RESOURCE,
                                                 config.CLIENT_ID)

    # Print user call to action message.
    # This will lead the user to an Microsoft Login page.
    print('    {}'.format(device_code['message']))

    # Send the Wait for the process to complete.
    response = auth_context.acquire_token_with_device_code(config.RESOURCE,
                                                           device_code,
                                                           config.CLIENT_ID)
    # Check if all required attributes exists.
    if not response.get('accessToken', None):
        return None

    # Create and pre-configure session.
    session = requests.Session()
    token = response["accessToken"]
    session.headers.update({'Authorization': 'Bearer {}'.format(token),
                            'SdkVersion': '{}'.format(config.APP_NAME),
                            'x-client-SKU': '{}'.format(config.APP_NAME),
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'})

    # Return session instance.
    return session


def get_worksheet_id(session):
    """
    Gets the worksheet id of the given xlsx file by path.
    """
    url = 'https://graph.microsoft.com/v1.0/me/drive/special/approot:/measurements.xlsx'

    # Get the specified workbook information.
    response = session.get(url)

    # Only the id is important.
    return response.json()["id"]


def append_row(session, workbookItemId):
    """
    Appends a new row with current measurement values to the worksheet.
    """
    url = 'https://graph.microsoft.com/v1.0/me/drive/items/{}/workbook/worksheets(\'Sheet1\')/tables(\'Table1\')/rows/add'.format(
        workbookItemId)

    # Get column values
    now = formatted_now_long()
    tempC = str(weather.temperature())
    presHpa = str(weather.pressure(unit='hPa'))
    lum = str(light.light())

    # Build data string
    data = '{ "values": [["'+now+'", "'+tempC+'", "'+presHpa+'", "'+lum+'"]]}'

    # Post the new row to the Graph API.
    session.post(url, data=data)


def timer_tick(session, workbookItemId):
    """Raised each time the timer ticks."""

    # Log the current tick.
    print('Timer ticked at: {}. Will trigger sync.'.format(formatted_time_now()))

    # Add new measurements to the online file.
    append_row(session, workbookItemId)


def formatted_now_long():
    """
    Gets a long formatted now date as string.
    """
    now = datetime.datetime.now()
    return (now.strftime("%d.%m.%Y %H:%M"))


def formatted_time_now():
    """
    Gets a a short formatted time from now as string.
    """
    now = datetime.datetime.now()
    return (now.strftime("%H:%M:%S"))


def handle_error():
    """
    Handles the error case.
    Will terminate the script with code 1.
    """

    print(""""
    An error occured, please check your config.py
    Terminating.""")
    exit(1)


def main():
    """
    Entry point to the script.
    Will ask the user to allow the script access to their
    OneDrive Excel files.
    If this was successful, the function will start the repeating
    timer to send new measurements to the cloud.
    """

    # Step 0:
    # Print lovley greetings.
    print("""
    ------
    > Welcome to Værmelder!
    > Store your room climate into your OneDrive!
    ------""")

    # Step 1.
    # Get access token via device token
    print("""
    ------
    Step 1:
    Get user's code.
    ------""")
    session = get_session()
    if not session:
        handle_error()

    # Step 2.
    # Get worksheet from OneDrive.
    print("""
    ------
    Step 2:
    Get worksheet ID
    """)
    worksheet_id = get_worksheet_id(session)
    if not worksheet_id:
        handle_error()

    # Step 3.
    # Starting repeating timer.
    print("""
    ------
    Step 3:
    Starting timer with 10 minutes delay.
    """)
    timer = RepeatingTimer(timer_tick, 60 * 10, session, worksheet_id)
    timer.start()


# Entry point for module as app execution,
if __name__ == "__main__":
    main()
