<#
	.DESCRIPTION
	Enables automatic time zone setup through the registry. This will fail if used
	on the device group during ESP, this should only be used on the user group.
	A restart is required in order to get it started.
#>

$path = "HKLM:\SYSTEM\CurrentControlSet\Services\tzautoupdate"
$key = "Start"

set-itemproperty -path "$path" -name "$key" -value 3