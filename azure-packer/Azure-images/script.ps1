mkdir -p C:\Apps\target

# Blob URL
$BlobUri = 'https://xxxxxx.blob.core.windows.net/test/SQL ALERTS.zip'

# in prefix please Add ?
$Sas = '?sp=r&st=2020-06-16T02:56:30Z&se=2020-06-16T10:56:30Z&spr=https&sv=2019-10-10&sr8c%3D'
$OutputPath = 'C:\Apps\SQL ALERTS.zip'

# combine URL main and SAS token

$FullUri = "$BlobUri$Sas"
(New-Object System.Net.WebClient).DownloadFile($FullUri, $OutputPath)

# Unarchive
expand-archive -path "C:\Apps\SQL ALERTS.zip" -destinationpath "c:\Apps\target" -Force

# Environment Variable set
[System.Environment]::SetEnvironmentVariable('testpkg','c:\Apps\target',[System.EnvironmentVariableTarget]::Machine)
# Remove Zip DownloadFile
Remove-Item -Path 'C:\Apps\SQL ALERTS.zip' -Force