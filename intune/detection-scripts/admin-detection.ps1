<#
    .DESCRIPTION
    Checks for the current logged in user if they are a local admin.
    It will return 0 if the user is admin and 1 if the user is not admin.

    .AUTHOR
    Tri Nguyen

    .UPDATED
    2/7/2026
#>

$user = (get-ciminstance -class win32_computersystem).username
# must be split due to match regex
$userName = $user.split("\")[-1]

if((net localgroup administrators) -match $userName){
    echo "User $user is admin"
    exit 0
}else{
    echo "User $user is not admin"
    exit 1
}