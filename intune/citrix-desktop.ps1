<#
    .DESCRIPTION
    Adds Citrix Workspace shortcut to the public desktop.

    .AUTHOR
    Tri Nguyen

    .UPDATED
    2/7/2026
#>

$startMenuFolder = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
$citrix = "Citrix Workspace.lnk"

# not going to fail this, as it is just a copy. since this is
# intended to be ran in system context, this will just fail the device ESP
if(!(test-path "$startMenuFolder\$citrix")){
    exit 0
}

$desktop = "C:\Users\Public\Desktop"

cp "$startMenuFolder\$citrix" "$desktop"