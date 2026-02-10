<#
    .DESCRIPTION
    Checks for the current logged in user if they are a local admin. If the user is admin,
    then it will return 0. If the user is not admin or an error occurs, then a non-zero will be returned.

    .PARAMETERS
        -User <string>
            The user of the device to check for. The name will be matched to the list of members of the
            Administrators group.
    
    .NOTES
        RETURN CODES:
            - 0: User is admin
            - 1: User is not admin
            - 2: No argument was given for the user

    .AUTHOR
    Tri Nguyen
#>

param(
    [string]$User
)

if(($User -eq $null) -or ($User.trim() -eq "")){
    write-error "Missing required argument -User"
    exit 2
}

# must be split due to match regex
$userName = $User.split("\")[-1]

if("$(net localgroup administrators)" -match "$userName"){
    echo "User $user is admin"
    exit 0
}else{
    echo "User $user is not admin"
    exit 1
}