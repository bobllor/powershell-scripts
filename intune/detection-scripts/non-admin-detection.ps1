<#
    .DESCRIPTION
    Checks for the current logged in user if they are a local admin.
    It will return 0 if the user is non-admin and 1 if the user is admin.

    .AUTHOR
    Tri Nguyen

    .NOTES
    This is a dynamic script and must be ran with the user logged in.
#>

$user = (get-ciminstance -class win32_computersystem).username
# must be split due to match regex
$userName = $user.split("\")[-1]

if("$(net localgroup administrators)" -match "$userName"){
    echo "User $user is admin"
    exit 1
}else{
    echo "User $user is not admin"
    exit 0
}