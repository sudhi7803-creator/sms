import requests
import msal
from datetime import datetime

# Path to your local Excel file
file_path = "C:\Users\DELL\Desktop\TempPlazza\TempPlazza.xlsx"

# App registration details from Azure portal
CLIENT_ID = "63529227-9149-4ba0-bd63-aaf1090a036e"
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["User.Read", "Files.ReadWrite"]

# Create a public client app
app = msal.PublicClientApplication(CLIENT_ID, authority="https://login.microsoftonline.com/common")

# Try to acquire token interactively
result = None
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if not result:
    result = app.acquire_token_interactive(scopes=SCOPES)

# Upload file if token is available
if "access_token" in result:
    access_token = result["access_token"]

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"TempPlazza_{timestamp}.xlsx"

    # Upload URL (creates folder automatically if missing)
    upload_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/TempPlazzaFolder/{filename}:/content"

    try:
        with open(file_path, "rb") as f:
            response = requests.put(
                upload_url,
                headers={"Authorization": f"Bearer {access_token}"},
                data=f
            )
            if response.status_code in (200, 201):
                print("✅ Upload successful:", filename)
                # Log success
                with open("C:/Users/DELL/Desktop/TempPlazza/upload_log.txt", "a") as log:
                    log.write(f"{datetime.now()} - {filename} - SUCCESS {response.status_code}\n")
            else:
                print(f"⚠️ Upload failed: {response.status_code} - {response.text}")
                # Log failure
                with open("C:/Users/DELL/Desktop/TempPlazza/upload_log.txt", "a") as log:
                    log.write(f"{datetime.now()} - {filename} - FAILED {response.status_code}\n")
    except Exception as e:
        print("❌ Error opening file:", e)
        # Log exception
        with open("C:/Users/DELL/Desktop/TempPlazza/upload_log.txt", "a") as log:
            log.write(f"{datetime.now()} - {filename} - ERROR {e}\n")

else:
    print("❌ Authentication failed:", result.get("error_description"))
    # Log authentication failure
    with open("C:/Users/DELL/Desktop/TempPlazza/upload_log.txt", "a") as log:
        log.write(f"{datetime.now()} - AUTH FAILED - {result.get('error_description')}\n")
