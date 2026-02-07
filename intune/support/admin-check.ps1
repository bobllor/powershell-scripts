<#
    .DESCRIPTION
    Checks for the current logged in user if they are a local admin.
    It will return 0 if the user is admin and 1 if the user is not admin.

    .AUTHOR
    Tri Nguyen

    .UPDATED
    2/7/2026
#>

# must be split otherwise we have an escape sequence error (maybe)
# better safe than sorry to just target the last name anyways
$user = (get-ciminstance -class win32_computersystem).username

$isAdmin = (net localgroup administrators) -contains "$user"

if($isAdmin){
    echo "User $user is admin"
    exit 0
}else{
    echo "User $user is not admin"
    exit 1
}