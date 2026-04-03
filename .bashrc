run_powershell(){
    first_arg=$1

    if [[ -z "$first_arg" ]]; then
        echo "error: must provide an argument"
        return 1
    fi 

    shift
    if [[ "$first_arg" =~ ".ps1" ]]; then
        # required to run the file
        first_arg="./$first_arg" 
    fi

    args=""
    for arg in $@; do
        args="$args $arg"
    done

    powershell -executionpolicy bypass "$first_arg" "$args"
}

alias pse=run_powershell