<#
   .DESCRIPTION
    Removes the current logged in user as admin. For this to take effect,
    the user must sign out and back into the device to refresh the token.

    .AUTHOR
    Tri Nguyen
#>

function Log{
    param(
        [string[]] $Out
    )

    $file = "admin-exec.log"
    $scriptName = $PSCommandPath.split("\")[-1]

    try{
        .\log.ps1 "$file" "$scriptName" "$Out" 
    }catch{
        echo "$Out"
    }
}

$user = (get-ciminstance -class win32_computersystem).username
$adminStr = (net localgroup administrators)

# required due to escape sequences
$userName = $user.split("\")[-1]

if("$user" -notmatch "azuread"){
    log "User $user is not AzureAD joined"
    exit 1
}
if("$adminStr" -notmatch "$userName"){
    log "Could not find $user in $adminStr"
    exit 0
}

log "Removing $user from local administrators"

try{
    net localgroup administrators /delete "$user"
}catch{
    log "Failed to remove admin: $_"
    exit 1
}
$adminStr = (net localgroup administrator $user)

if("$adminStr" -match "$userName"){
    log "Failed to remove user $user as admin"
    exit 1
}else{
    log "User $user has been removed as admin"
    exit 0
}