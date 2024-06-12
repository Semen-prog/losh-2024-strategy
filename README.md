# ЛОШ 2024 Стратегия

## Установка WSL

Пуск -> поиск -> включение или отключение компонентов Windows -> выбрать галочки Подсистема Windows для Linux и Платформа виртуальной машины -> ОК -> Перезагрузить сейчас

Microsoft Store -> Ubuntu 24.04 LTS - Install

В PowerShell выполнить wsl.exe --install, затем wsl.exe --update

Из меню Пуск запустить Ubuntu 24.04 LTS, выполнить установку

## Установка утилит

### Выполнить команду:

```bash
sudo apt install gcc g++ make python3 python3-tk git && git clone "https://github.com/Semen-prog/losh-2024-strategy" && cd losh-2024-strategy && make && cd binaries && ./interactor --help
```

### Либо выполнить установку вручную:

Установить GNU Make, gcc, g++ (`sudo apt install make gcc g++`)

Находясь в этой папке, выполнить команду `make`.

Перейти в папку binaries (`cd binaries`)

Запустить `./interactor --help`, запустить игру в соответствии с форматом, описанным в help.
