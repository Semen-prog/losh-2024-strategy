path=$(whiptail --title "Импорт стратегии" --inputbox "Введите путь до стратегии" 10 60 3>&1 1>&2 2>&3)
ln -s $(wslpath $path)