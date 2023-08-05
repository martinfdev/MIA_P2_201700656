from src.CLI import cli_command
from src.Exec import Exec
import src.Functions as fn

if __name__ == "__main__":
    while True:
        command = input(">> ")
        if command == "exit":
            break
        content = cli_command(command)
        if content != "":
            print(cli_command(content))