#!/bin/bash

port=3700

log_dir="logs"
if [ ! -d "$log_dir" ]; then
    mkdir "$log_dir"
fi

if [[ "$1" == "--debug" ]]; then
    debug=true
else
    debug=false
fi

print_color_message() {
    local message="$1"
    local color="$2"
    case "$color" in
        "red") echo -e "\e[31m$message\e[0m";;
        "green") echo -e "\e[32m$message\e[0m";;
        "yellow") echo -e "\e[33m$message\e[0m";;
        *) echo "$message";;
    esac
}

launch_uvicorn() {
    local folder="$1"
    cd "$folder"
    local uvicorn_command="uvicorn app:engine.app --host 0.0.0.0 --port $port"
    if [ "$debug" = true ]; then
        uvicorn_command+=" --reload"
    fi
    $uvicorn_command
    cd ..
}


for folder in */; do
    if [ "$folder" != "base_engine/" ] && [ "$folder" != "logs/" ]; then        
        log_file="$log_dir/${folder%/}.log"

        launch_uvicorn "$folder" &
        
        engine_name=$(print_color_message "${folder%/}" "green")
        port_number=$(print_color_message "$port" "red")
        url=$(print_color_message "http://localhost:$port" "yellow")
        echo "$engine_name started on port $port_number $url"

        ((port++))
    fi
done

wait