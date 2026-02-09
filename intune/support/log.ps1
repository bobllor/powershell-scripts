<#
    .DESCRIPTION
    Used for Intune logging. This is intended to be used with Intune applications, and by default
    it will log to C:\Windows\ProgramData\AppLogs.
    It is recommended to put this in a wrapper function to log different files.

    .PARAMETERS
        -OutFile <string>
            The file name of the log output. If the file name does not end in a .log, then
            it will automatically be converted to a .log file.
        
        -Script <string>
            The script file name.

        -Output <string[]>
            The output message to write to the log file.

        -SkipDir <switch>
            Skips the log directory creation if true.

    .AUTHOR
    Tri Nguyen
#>

# TODO: log levels

param(
    [Parameter(Mandatory=$true)]
    [string] $OutFile,
    [Parameter(Mandatory=$true)]
    [string] $Script,
    [string[]] $Output,
    [switch] $SkipDir
)

$outPath = "C:\Windows\ProgramData\AppLogs"

if(!(test-path $outPath) -and !($SkipDir)){
    mkdir $outPath | out-null
}

$splitFile = $OutFile.split(".")
$finalOutFile = "" # variable being used for the output file

if($splitFile[-1] -match "log"){
    $finalOutFile = $OutFile
}else{
    $finalOutFile = "$($splitFile[0]).log"
}

$date = (get-date -format "yyyy-MM-dd HH:mm:ss")

echo "[$date | $Script] $Output" | out-file -filepath "$outPath\$finalOutFile" -append